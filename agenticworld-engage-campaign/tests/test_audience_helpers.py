import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "scripts"
BUSINESS_FIELDS = [
    "customer_id",
    "email_address",
    "customer_status",
    "days_since_last_purchase",
    "expected_repurchase_days",
    "propensity_to_churn",
    "email_consent_status",
    "record_role",
]


class AudienceHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.business = self.directory / "business.csv"
        self.qa = self.directory / "qa.csv"

    def write_csv(self, path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def business_row(self, email="alex@example.test", consent="GRANTED"):
        return {
            "customer_id": "C1",
            "email_address": email,
            "customer_status": "active",
            "days_since_last_purchase": "200",
            "expected_repurchase_days": "90",
            "propensity_to_churn": "0.8",
            "email_consent_status": consent,
            "record_role": "business_customer",
        }

    def write_qa(self, email="alex@example.test"):
        self.write_csv(
            self.qa,
            BUSINESS_FIELDS,
            [{
                "customer_id": "WS-QA-1",
                "email_address": email,
                "email_consent_status": "GRANTED",
                "record_role": "workshop_self_test",
            }],
        )

    def run_prepare(self, source, qa):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "prepare_audience.py"),
                "--csv", str(source),
                "--email", "alex@example.test",
                "--first-name", "Alex",
                "--last-name", "Lee",
                "--participant-role", "workshop_self_test",
                "--self-test-output", str(qa),
            ],
            capture_output=True,
            text=True,
        )

    def run_analyzer(self, selected, delivery, report, participant="alex@example.test"):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "analyze_added_audience.py"),
                "--input", str(self.business),
                "--strategy", "higher-risk",
                "--qa", str(self.qa),
                "--participant-email", participant,
                "--approved-test-address", participant,
                "--selected-output", str(selected),
                "--delivery-output", str(delivery),
                "--report-output", str(report),
            ],
            capture_output=True,
            text=True,
        )

    def test_self_test_requires_an_existing_business_source(self):
        missing = self.directory / "missing-business.csv"
        result = self.run_prepare(missing, self.qa)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Business source CSV must exist", result.stderr)
        self.assertFalse(missing.exists())
        self.assertFalse(self.qa.exists())

    def test_prepare_rejects_case_or_whitespace_variants_of_denied_consent(self):
        for consent in ("denied", " DENIED "):
            with self.subTest(consent=consent):
                self.write_csv(self.business, BUSINESS_FIELDS, [self.business_row(consent=consent)])
                original = self.business.read_bytes()
                result = self.run_prepare(self.business, self.qa)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Existing DENIED consent", result.stderr)
                self.assertEqual(self.business.read_bytes(), original)
                self.assertFalse(self.qa.exists())

    def test_analyzer_blocks_qa_when_existing_business_consent_is_denied(self):
        self.write_csv(self.business, BUSINESS_FIELDS, [self.business_row(consent=" denied ")])
        self.write_qa()
        result = self.run_analyzer(
            self.directory / "selected.csv",
            self.directory / "delivery.csv",
            self.directory / "report.json",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA cannot bypass existing DENIED consent", result.stderr)
        self.assertFalse((self.directory / "delivery.csv").exists())

    def test_business_and_qa_role_overlap_is_counted_once_for_delivery(self):
        self.write_csv(self.business, BUSINESS_FIELDS, [self.business_row()])
        self.write_qa()
        selected = self.directory / "selected.csv"
        delivery = self.directory / "delivery.csv"
        report = self.directory / "report.json"
        result = self.run_analyzer(selected, delivery, report)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["participant_business_overlap"], 1)
        self.assertEqual(summary["business_delivery_rows"], 1)
        self.assertFalse(summary["business_delivery_empty"])
        self.assertEqual(summary["delivery_rows"], 1)
        with delivery.open(encoding="utf-8", newline="") as stream:
            delivered = list(csv.DictReader(stream))
        self.assertEqual(len(delivered), 1)
        self.assertEqual(delivered[0]["record_role"], "workshop_self_test")

    def test_failed_output_staging_preserves_existing_results(self):
        self.write_csv(self.business, BUSINESS_FIELDS, [self.business_row()])
        self.write_qa()
        selected = self.directory / "selected.csv"
        report = self.directory / "report.json"
        selected.write_text("previous selection\n", encoding="utf-8")
        report.write_text("previous report\n", encoding="utf-8")
        bad_parent = self.directory / "not-a-directory"
        bad_parent.write_text("file", encoding="utf-8")
        result = self.run_analyzer(selected, bad_parent / "delivery.csv", report)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(selected.read_text(encoding="utf-8"), "previous selection\n")
        self.assertEqual(report.read_text(encoding="utf-8"), "previous report\n")
        self.assertEqual(list(self.directory.glob(".selection-*.csv")), [])


if __name__ == "__main__":
    unittest.main()
