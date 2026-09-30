#!/usr/bin/env python3
"""Prepare (but never execute) tdx query SQL from a small, approved CSV."""

import argparse
import csv
import datetime as dt
import os
import re
import sys
import tempfile
from pathlib import Path

DATABASE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
TABLE_RE = re.compile(r"^sample_id_[a-f0-9]{32}$")
COLUMN_RE = re.compile(r"^[a-z][a-z0-9_]*$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def fail(message):
    raise SystemExit(f"Error: {message}")


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def sql_string(value):
    if "\x00" in value:
        fail("NUL characters are not supported in CSV values")
    if "\r" in value or "\n" in value:
        fail("Multiline field values are not supported by this small-file SQL path")
    return "'" + value.replace("'", "''") + "'"


def sql_value(value, blank_policy):
    if value == "" and blank_policy == "null":
        return "NULL"
    return sql_string(value)


def read_csv(path, max_file_bytes, max_rows):
    path = Path(path)
    if not path.is_file():
        fail("CSV path is not a regular file")
    if path.stat().st_size > max_file_bytes:
        fail("CSV exceeds the approved file-size limit")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source, strict=True)
            headers = next(reader, None)
            if not headers:
                fail("CSV is empty or has no header row")
            if any(header != header.strip() for header in headers):
                fail("Headers with leading/trailing whitespace must be corrected explicitly")
            if any(not COLUMN_RE.fullmatch(header) for header in headers):
                fail("Headers must use lowercase SQL-safe names: letters, digits, and underscores")
            lowered = [header.lower() for header in headers]
            if len(set(lowered)) != len(lowered):
                fail("Duplicate headers are not supported")
            if "email" not in headers:
                fail("The CSV must contain the exact `email` header for an email campaign")

            rows = []
            ignored_blank_rows = 0
            for line_number, row in enumerate(reader, start=2):
                if not row or all(value.strip() == "" for value in row):
                    ignored_blank_rows += 1
                    continue
                if len(row) != len(headers):
                    fail(f"Row {line_number} has a different number of fields than the header")
                if len(rows) >= max_rows:
                    fail("CSV exceeds the approved row-count limit")
                rows.append(row)
    except UnicodeDecodeError:
        fail("CSV must be UTF-8 encoded")
    except csv.Error:
        fail("CSV quoting is malformed")

    if not rows:
        fail("CSV has no nonblank data rows")
    return headers, rows, ignored_blank_rows


def validate_key(headers, rows, key_column):
    if key_column not in headers:
        fail("The approved master-key column is not present in the CSV")
    index = headers.index(key_column)
    seen = set()
    email_index = headers.index("email")
    for row_number, row in enumerate(rows, start=2):
        raw_key = row[index]
        key_value = raw_key.strip()
        if raw_key != key_value:
            fail(f"Master key has leading/trailing whitespace on row {row_number}")
        if not key_value:
            fail(f"Master key is blank on row {row_number}")
        normalized = key_value.casefold() if key_column == "email" else key_value
        if normalized in seen:
            fail(f"Duplicate master key found on row {row_number}")
        seen.add(normalized)

        raw_email = row[email_index]
        email = raw_email.strip()
        if raw_email != email:
            fail(f"Email has leading/trailing whitespace on row {row_number}")
        if not EMAIL_RE.fullmatch(email):
            fail(f"Email value is missing or malformed on row {row_number}")


def write_private_file(directory, name, content):
    path = directory / name
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
        output.write(content)
    return path


def build_sql(database, table, headers, rows, key_column, blank_policy, time_mode, ingest_time):
    time_in_csv = "time" in headers
    if time_mode == "csv" and not time_in_csv:
        fail("`--time-mode csv` requires an exact `time` header")
    if time_mode == "ingest" and time_in_csv:
        fail("CSV already has a `time` header; use `--time-mode csv` after verifying its values")

    if time_in_csv:
        time_index = headers.index("time")
        for row_number, row in enumerate(rows, start=2):
            try:
                int(row[time_index])
            except ValueError:
                fail(f"`time` must be Unix epoch seconds on row {row_number}")
        columns = headers
    else:
        columns = ["time", *headers]

    target = f"{quote_identifier(database)}.{quote_identifier(table)}"
    definitions = [f"  {quote_identifier(column)} {'BIGINT' if column == 'time' else 'VARCHAR'}" for column in columns]
    create_sql = f"CREATE TABLE {target} (\n" + ",\n".join(definitions) + "\n);\n"

    insert_columns = ", ".join(quote_identifier(column) for column in columns)
    values = []
    for row in rows:
        if time_in_csv:
            typed_values = [
                str(int(value)) if column == "time" else sql_value(value, blank_policy)
                for column, value in zip(columns, row)
            ]
            values.append("(" + ", ".join(typed_values) + ")")
        else:
            values.append("(" + ", ".join([str(ingest_time), *[sql_value(value, blank_policy) for value in row]]) + ")")
    insert_sql = f"INSERT INTO {target} ({insert_columns})\nVALUES\n  " + ",\n  ".join(values) + ";\n"
    return create_sql, insert_sql


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Approved local CSV file with a header row")
    parser.add_argument("--database", default="agentic_world_demo")
    parser.add_argument("--table", required=True, help="Use sample_id_ followed by 32 lowercase hex digits")
    parser.add_argument("--key-column", required=True, help="Approved unique master key column")
    parser.add_argument("--max-file-bytes", type=int, required=True, help="Limit recorded in the readiness ledger")
    parser.add_argument("--max-rows", type=int, required=True, help="Limit recorded in the readiness ledger")
    parser.add_argument("--max-sql-bytes", type=int, required=True, help="Limit recorded in the readiness ledger")
    parser.add_argument("--blank-policy", choices=("null", "empty"), required=True)
    parser.add_argument("--time-mode", choices=("ingest", "csv"), default="ingest")
    parser.add_argument("--ingest-time", type=int, help="Unix epoch seconds; defaults to current UTC time")
    args = parser.parse_args()

    if args.database != "agentic_world_demo" or not DATABASE_RE.fullmatch(args.database):
        fail("This helper only targets the approved `agentic_world_demo` database")
    if not TABLE_RE.fullmatch(args.table):
        fail("Table name must match sample_id_<32 lowercase hexadecimal characters>")
    if min(args.max_file_bytes, args.max_rows, args.max_sql_bytes) <= 0:
        fail("Approved file, row, and SQL size limits must be positive")

    headers, rows, ignored_blank_rows = read_csv(args.csv_path, args.max_file_bytes, args.max_rows)
    validate_key(headers, rows, args.key_column)
    ingest_time = args.ingest_time
    if args.time_mode == "ingest":
        if ingest_time is None:
            ingest_time = int(dt.datetime.now(dt.timezone.utc).timestamp())
        if ingest_time < 0:
            fail("Ingest time must be a non-negative Unix timestamp")
    create_sql, insert_sql = build_sql(
        args.database, args.table, headers, rows, args.key_column,
        args.blank_policy, args.time_mode, ingest_time
    )
    if len(insert_sql.encode("utf-8")) > args.max_sql_bytes:
        fail("Generated INSERT SQL exceeds the approved SQL-size limit; do not split it without a verified batch/retry procedure")

    output_dir = Path(tempfile.mkdtemp(prefix="motion1-tdx-sql-"))
    os.chmod(output_dir, 0o700)
    create_path = write_private_file(output_dir, "create-table.sql", create_sql)
    insert_path = write_private_file(output_dir, "insert-rows.sql", insert_sql)

    print("Prepared SQL only; no TD command was executed")
    print(f"database={args.database}")
    print(f"table={args.table}")
    print(f"rows={len(rows)}")
    print(f"ignored_blank_rows={ignored_blank_rows}")
    print(f"master_key={args.key_column}")
    print(f"time_mode={args.time_mode}")
    if args.time_mode == "ingest":
        print(f"time_value={ingest_time}")
    print(f"insert_sql_bytes={len(insert_sql.encode('utf-8'))}")
    print(f"create_sql_file={create_path}")
    print(f"insert_sql_file={insert_path}")
    print("Warning: INSERT SQL contains CSV values and may be retained in query/job history; verify approval and retention before running tdx query")


if __name__ == "__main__":
    main()
