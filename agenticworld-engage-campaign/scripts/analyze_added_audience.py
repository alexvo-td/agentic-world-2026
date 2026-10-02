#!/usr/bin/env python3
"""Analyze a conference list and prepare workshop recipients; never send/import.

Baseline overlap is exact normalized-email overlap, not identity unification.
QA is explicit and separate from business targeting and persona evidence.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import statistics
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)) or 'email_address' not in fields:
            raise ValueError('Unique headers including email_address are required')
        rows = list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError('Inconsistent CSV cell count')
    return fields, rows


def number(row, field, positive=False, score=False):
    try:
        value = float(row.get(field, ''))
    except (ValueError, TypeError):
        return None
    if not math.isfinite(value) or value < 0 or (positive and value == 0) or (score and value > 1):
        return None
    return value


def reason(row, strategy):
    if row.get('record_role') == 'workshop_self_test':
        return 'confirmation_record_not_business_customer'
    if row.get('customer_status') != 'active':
        return 'inactive_or_unknown_status'
    if row.get('email_consent_status') != 'GRANTED':
        return 'denied_or_unknown_email_consent'
    days = number(row, 'days_since_last_purchase')
    expected = number(row, 'expected_repurchase_days', positive=True)
    if days is None or expected is None:
        return 'missing_or_invalid_purchase_history'
    if days <= expected:
        return 'not_overdue'
    if strategy == 'higher-risk':
        churn = number(row, 'propensity_to_churn', score=True)
        if churn is None:
            return 'missing_or_invalid_churn'
        if churn < .70:
            return 'below_workshop_churn_threshold'
    return None


def median(rows, field, **kwargs):
    values = [v for row in rows if (v := number(row, field, **kwargs)) is not None]
    return {'value': statistics.median(values) if values else None, 'known': len(values), 'total': len(rows)}


def stage_output(path, prefix, newline, write):
    path = Path(path)
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f'Output must be a regular file: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=prefix, suffix=path.suffix)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline=newline) as stream:
            write(stream)
        return Path(temp)
    except Exception:
        if os.path.exists(temp):
            os.unlink(temp)
        raise


def stage_csv(path, fields, rows):
    def write(stream):
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    return stage_output(path, '.selection-', '', write)


def stage_json(path, report):
    def write(stream):
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')

    return stage_output(path, '.analysis-', None, write)


def publish_outputs(outputs):
    staged = []
    backups = []
    installed = []
    committed = False
    rollback_failed = False
    try:
        for path, build in outputs:
            staged.append((Path(path), build()))
        for path, _ in staged:
            if path.exists():
                fd, backup = tempfile.mkstemp(dir=path.parent, prefix='.backup-', suffix=path.suffix)
                os.close(fd)
                os.unlink(backup)
                backups.append((path, Path(backup)))
                os.replace(path, backup)
        for path, temp in staged:
            os.replace(temp, path)
            installed.append(path)
        committed = True
    except Exception:
        for path in reversed(installed):
            try:
                if path.exists():
                    path.unlink()
            except OSError:
                rollback_failed = True
        for path, backup in reversed(backups):
            try:
                if backup.exists():
                    os.replace(backup, path)
            except OSError:
                rollback_failed = True
        raise
    finally:
        for _, temp in staged:
            if temp.exists():
                temp.unlink()
        if committed or not rollback_failed:
            for _, backup in backups:
                if backup.exists():
                    backup.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--strategy', choices=['all-overdue', 'higher-risk'], required=True)
    parser.add_argument('--baseline', help='Verified original selected cohort CSV; omit when unavailable')
    parser.add_argument('--qa', required=True)
    parser.add_argument('--participant-email', required=True)
    parser.add_argument('--ses-verified', action='store_true', help='Host has verified the selected route is SES')
    parser.add_argument('--approved-test-address', action='append', default=[])
    parser.add_argument('--selected-output', required=True)
    parser.add_argument('--delivery-output', required=True)
    parser.add_argument('--report-output', required=True)
    args = parser.parse_args()
    try:
        sources = [args.input, args.qa] + ([args.baseline] if args.baseline else [])
        outputs = [args.selected_output, args.delivery_output, args.report_output]
        resolved = [Path(p).resolve() for p in outputs]
        if len(set(resolved)) != len(resolved) or set(resolved) & {Path(p).resolve() for p in sources}:
            raise ValueError('Use distinct output paths and preserve all sources')
        fields, rows = read_csv(args.input)
        ids = [r.get('customer_id', '') for r in rows if r.get('customer_id')]
        if len(ids) != len(set(ids)):
            raise ValueError('Duplicate customer IDs; reconcile before customer counts')
        email_keys = [r['email_address'].strip().casefold() for r in rows]
        if len(email_keys) != len(set(email_keys)):
            raise ValueError('Duplicate list emails; reconcile before selection')
        baseline = None
        if args.baseline:
            _, base_rows = read_csv(args.baseline)
            baseline = {r['email_address'].strip().casefold() for r in base_rows if r.get('record_role') != 'workshop_self_test'}
        exclusions = Counter()
        selected = []
        for row in rows:
            exclusion = reason(row, args.strategy)
            if exclusion:
                exclusions[exclusion] += 1
            else:
                selected.append(row)
        cohort_keys = {r['email_address'].strip().casefold() for r in selected}
        overlap = len(cohort_keys & baseline) if baseline is not None else None
        business_delivery = []
        delivery_exclusions = Counter()
        approved = {a.strip().casefold() for a in args.approved_test_address}
        for row in selected:
            key = row['email_address'].strip().casefold()
            if not re.fullmatch(r'[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+', key):
                delivery_exclusions['invalid_email'] += 1
            elif baseline is not None and key in baseline:
                delivery_exclusions['already_in_original_audience'] += 1
            elif key in approved or (args.ses_verified and re.fullmatch(r'success(?:\+[A-Za-z0-9_-]+)?@simulator\.amazonses\.com', key)):
                business_delivery.append(row)
            else:
                delivery_exclusions['unverified_workshop_destination'] += 1
        qa_fields, qa_rows = read_csv(args.qa)
        participant = args.participant_email.strip().casefold()
        if not re.fullmatch(r'[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+', participant) or participant.endswith('@simulator.amazonses.com'):
            raise ValueError('Participant must supply their own valid email')
        if len(qa_rows) != 1 or qa_rows[0]['email_address'].strip().casefold() != participant or qa_rows[0].get('record_role') != 'workshop_self_test' or qa_rows[0].get('email_consent_status') != 'GRANTED':
            raise ValueError('Require exactly one explicitly authorized participant QA record')
        if any(r['email_address'].strip().casefold() == participant and (r.get('email_consent_status') or '').strip().casefold() == 'denied' for r in rows):
            raise ValueError('QA cannot bypass existing DENIED consent')
        # A destination is sent only once; preserve the business artifact and
        # disclose the participant/business collision separately in the report.
        qa_overlap = sum(r['email_address'].strip().casefold() == participant for r in business_delivery)
        business_delivery = [r for r in business_delivery if r['email_address'].strip().casefold() != participant]
        business_delivery_count = len(business_delivery) + qa_overlap
        all_fields = list(dict.fromkeys(fields + qa_fields + ['record_role']))
        deliver_rows = [{**r, 'record_role': 'business_customer'} for r in business_delivery] + qa_rows
        report = {
            'schema_version': 1,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'source_sha256': hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),
            'baseline_sha256': hashlib.sha256(Path(args.baseline).read_bytes()).hexdigest() if args.baseline else None,
            'qa_sha256': hashlib.sha256(Path(args.qa).read_bytes()).hexdigest(),
            'strategy': args.strategy, 'list_rows': len(rows), 'business_cohort': len(selected),
            'cohort_exclusions': dict(exclusions), 'overlap_with_original': overlap,
            'additional_business_profiles': len(selected) - overlap if overlap is not None else None,
            'overlap_method': 'exact normalized email; plus labels preserved' if baseline is not None else 'unavailable',
            'business_delivery_rows': business_delivery_count, 'qa_delivery_rows': 1,
            'delivery_rows': len(deliver_rows), 'participant_business_overlap': qa_overlap,
            'participant_business_cohort_overlap': participant in cohort_keys,
            'delivery_exclusions': dict(delivery_exclusions),
            'days_since_purchase': median(selected, 'days_since_last_purchase'),
            'churn_score': median(selected, 'propensity_to_churn', score=True),
            'business_audience_empty': not selected,
            'business_delivery_empty': business_delivery_count == 0,
            'status': 'locally_prepared_not_imported_or_launch_ready',
        }
        # Stage every result before publishing any of them.
        publish_outputs([
            (args.selected_output, lambda: stage_csv(args.selected_output, fields, selected)),
            (args.delivery_output, lambda: stage_csv(args.delivery_output, all_fields, deliver_rows)),
            (args.report_output, lambda: stage_json(args.report_output, report)),
        ])
        print(json.dumps(report, allow_nan=False))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
