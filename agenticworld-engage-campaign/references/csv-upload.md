# CSV preparation and upload contract

Adapted from the participant-supplied agenticworld-profile-csv-intake reference. Use its CSV validation, approved destination and handoff conventions. The user specifies the actual import mechanism: generate Trino INSERT INTO SQL from the selected CSV and execute it through tdx query. Do not use bulk-import or an invented upload API.

## Prepare

Save a new UTF-8 CSV with standard quoting in the personal run folder, preserving original files. Use a unique name. Preparation and saving are already authorized; do not ask whether to save or continue. Use the participant's supplied identity and 30 distinct SES success test profiles with preserved plus labels. The reusable rich profile CSV may retain email_address; the campaign import must use lowercase email, first_name, last_name and other SQL-safe lowercase headers. Use prepare_recipient_import.py on the selected send data for the required email column.

Keep the complete 31-profile dataset distinct from the selected business cohort and delivery CSV. The selected campaign row count may be smaller because of the participant's strategy and existing consent criteria; explain exclusions and never silently remove approved test addresses for being simulator recipients. Do not bypass chosen targeting or DENIED consent to force 31 sends.

Validate email syntax, required fields/blanks, consistent cell counts, duplicate email keys, recipient classes, exact actual row counts and plus-label preservation. Do not silently repair real values. Request only needed corrections. Reject duplicate recipient emails rather than discarding rows. Mask identity in shared technical summaries; do not put profile rows or credentials in state/handoff records.

## Types and ingest time

The supplied helper convention imports non-time columns as text. Preserve numbers and scores as CSV text; parse them for local targeting when needed. Verify actual imported types before YAML mapping: use string for text fields rather than assuming numeric/date inference. Normally omit time in the CSV and add a fixed Unix-second ingest time when generating INSERT SQL. If time is supplied, require Unix seconds. Do not promise multiline-cell support, large/batched upload, or richer types without a verified helper contract.

## Fixed database and unique table allocation

Always use `agentic_world_demo` for this workshop's new recipient tables. Do not prompt for a database or substitute another database. Before table creation or INSERT, generate an identifier-safe name using `aw_recipients_<UTC timestamp>_<uuid4 hex>` (for example, prefix plus YYYYMMDD_HHMMSS and a full UUID without hyphens). Do not include participant email or other personal values in table names.

Persist the name and run ID before execution; use that exact table consistently for schema creation, INSERT, validation SELECTs and campaign YAML `contact_list.table_name`. Confirm the name is absent using documented read-only table discovery. If it exists before this run creates it, generate a fresh name and check again; never reuse, overwrite or append to that unrelated table. If creation reports a collision, allocate a new name only after determining this is a different table, rather than an ambiguous successful creation by the current run.

New requests allocate fresh names. Continuation and retries reconcile the persisted current-run table rather than generating another name on every command. No table-name approval is needed. Random uniqueness supplements, rather than replaces, the existence check.

## Upload

Confirm the writable workshop database and create a new, empty run-owned recipient table using the documented table/schema operation. Verify its schema first: physical email and other CSV fields are strings; time is a Unix-second integer. Table creation is a prerequisite, not evidence of inserted rows. Respect higher-priority database permissions; if writes are blocked, preserve drafts and report the specific host restriction.

Generate a private SQL file with the bundled script after selecting eligible recipients:

```bash
python3 scripts/csv_to_insert.py --csv recipient-import.csv --table <new-run-table> --output recipient-insert.sql
```

The generator emits a single INSERT INTO with an explicit column list and VALUES rows. It restricts the database to agentic_world_demo, validates identifiers/cell counts/emails, escapes single quotes, preserves plus labels, treats non-time fields as text, and adds ingest time. It does not create a table, select recipients or execute SQL. Validate identifiers and schema before use; reject unsupported size/multiline requirements rather than inventing batching.

Run the SQL file directly:

```bash
tdx query --database agentic_world_demo --file recipient-insert.sql
```

Reference: https://tdx.treasuredata.com/commands/query.html . tdx query uses Trino and accepts SQL files. INSERT syntax reference: https://trino.io/docs/current/sql/insert.html . Keep values out of shell arguments and participant-facing logs. The SQL file and TD query/job history contain recipient values; use the established workshop handling scope without a redundant consent question. Do not commit this generated file into skill/source repositories.

Persist the SQL/CSV hash, run table, fixed ingest time and returned job identifier/status before considering retries. Reconcile an ambiguous outcome through job status and table rows; never blindly rerun INSERT, since it appends and can duplicate recipients. No automatic DELETE/TRUNCATE cleanup. Wait for actual completion, then use SELECT to verify expected row count, unique email count, required values and preserved simulator labels. Verify schema again before YAML mapping. Only then mark imported and continue automatically to campaign creation. Local SQL generation is not a successful TD import.

## Handoff and participant summary

Record non-secret file path, field names/types, dataset/cohort/delivery counts, participant/test counts, recipient authorization classes, validation result, account/region, destination table, import/job status, observed runtime version and check time. Include no profile values or credentials. Existing scope/handling approvals are reused.

Show a concise summary with filename, destination, actual participant/test row counts and validation/upload status. Continue the requested campaign journey without asking whether to continue. For a CSV-only request, stop after saving and validation; it does not authorize sending. Retain the single final Launch action after the campaign preview.
