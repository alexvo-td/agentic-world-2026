---
name: stage-table
description: 'Use when an Agentic World 2026 attendee runs /stage-table or asks to stage or normalize a retail_raw identity table, including "Help me stage this table: retail_raw.raw_dw_customer_snapshot". Use the pinned fast-path recipe for raw_dw_customer_snapshot; inspect, propose direct SQL, wait for approval, create one table, and validate. Never use for workflows, unification, fact/event staging, or production data.'
---

# Stage One Identity Table

Stage **one** `retail_raw.raw_*` identity table into an attendee-assigned staging database using direct SQL. Work in two phases: **inspect and propose**, then **create and validate only after explicit approval**. For `retail_raw.raw_dw_customer_snapshot`, use the fast path below — run 3 safeguard checks and present the pre-built SQL; do not run exploratory field-distribution queries. For other identity tables, use the generic fallback. This is a workshop skill; do not assume that a successful proposal has been executed.

## Inputs and routing

- Accept a natural-language request such as "Help me stage this table: retail_raw.raw_dw_customer_snapshot" or `/stage-table <source_table> <assigned_staging_database>`. If the assigned staging database is not provided, ask for it before naming a target or running checks. Never guess the attendee's database or use shared `retail_stage` as a fallback. Confirm the active instance/account; do not switch silently.
- If the source is `retail_raw.raw_dw_customer_snapshot`, use **Fast path** below. Propose `<assigned_staging_database>.stg_dw_customer_snapshot` and confirm the exact target.
- If it is another `retail_raw.raw_*` **identity** table, use **Other identity sources** below; do not transplant the DW key, counts, ordering, or SQL. For a fact/event table or another database, stop and clarify scope.
- Read-only inspection may proceed without write approval. A general request to stage data is **not** approval to execute unseen SQL.

## Fast path: `retail_raw.raw_dw_customer_snapshot`

Transformation decisions for this table are **already made and validated** (rehearsal: 2026-09-28). Do not run exploratory field-distribution queries. Run 3 fast safeguard checks, substitute the staging database name into the pre-built SQL below, and ask for approval.

### Pre-validated findings

| Finding | Value |
|---|---|
| Schema | 16 columns — all `varchar` except `time` (`bigint`) |
| Total raw rows | 2,787 |
| NULL/blank `dw_customer_key` | 0 |
| Distinct `dw_customer_key` | 2,687 |
| Same-key retries (identical business fields) | 100 |
| Business conflicts (same key, differing business fields) | 0 |
| Dedup order column | `connector_record_id` ASC — zero-padded, lexicographic = numeric order |
| Originals | `DW-LOAD-0000001`–`DW-LOAD-0002687` (`warehouse_20260923_01`) |
| Replays | `DW-LOAD-0002688`–`DW-LOAD-0002787` (`warehouse_20260923_replay`) |
| Email missing | 571 (20.5%) · malformed: 7 · need lower/trim: ~755 |
| Phone missing | 855 (30.7%) · 11-digit +1 prefix: 243 · 10-digit clean: 1,689 |
| Postal non-standard (`NNN-NN` pattern) | 238 (8.9%) — flagged `trfm_postal_invalid` |
| `marketing_opt_in` distinct values | `Y`, `true`, `N`, `false` only — 0 NULL |
| `lifetime_value` | All parseable as DOUBLE — 0 missing, 0 unparseable |
| `snapshot_date` | ISO `YYYY-MM-DD` — all TRY_CAST-valid (`2026-09-21/22/23`) |

Fields preserved verbatim (no derived transform): `first_name`, `last_name`, `city`, `state`, `loyalty_status`, `connector_record_id`, `source_batch`, `time`.

### Phase 1 — Three safeguard checks and proposal

**Step 1 — DB and target check.** Confirm the assigned staging database exists and `stg_dw_customer_snapshot` does not exist in it. If the database is missing, the target exists, or permissions block visibility, explain the specific issue and **do not write**. A missing database may still allow a `NOT EXECUTED` proposal; never create a database, overwrite a table, or choose a substitute.

**Step 2 — Schema check.** Run `tdx describe retail_raw.raw_dw_customer_snapshot`. Confirm exactly 16 columns match the expected list: `dw_customer_key`, `first_name`, `last_name`, `email_address`, `phone_number`, `address_line1`, `city`, `state`, `postal_code`, `loyalty_status`, `lifetime_value`, `marketing_opt_in`, `snapshot_date`, `connector_record_id`, `source_batch`, `time`. If the schema differs, stop and investigate before proceeding.

**Steps 3a and 3b — Run in parallel.** Run both queries simultaneously.

**3a — Safeguard query:**

```sql
SELECT
  COUNT(*)                                                             AS total_rows,
  COUNT(CASE WHEN dw_customer_key IS NULL
               OR TRIM(dw_customer_key) = '' THEN 1 END)              AS null_blank_keys,
  COUNT(DISTINCT dw_customer_key)                                      AS distinct_keys,
  (
    SELECT COUNT(*) FROM (
      SELECT dw_customer_key
      FROM (
        SELECT DISTINCT dw_customer_key,
          first_name, last_name, email_address, phone_number,
          address_line1, city, state, postal_code,
          loyalty_status, lifetime_value, marketing_opt_in, snapshot_date
        FROM retail_raw.raw_dw_customer_snapshot
      ) t
      GROUP BY dw_customer_key HAVING COUNT(*) > 1
    )
  )                                                                    AS conflicting_keys
FROM retail_raw.raw_dw_customer_snapshot
```

**Expected:** `total_rows = 2787`, `null_blank_keys = 0`, `distinct_keys = 2687`, `conflicting_keys = 0`. If counts differ materially or `conflicting_keys > 0`, stop and investigate — do not proceed with the pre-built SQL.

**3b — Ordering evidence query** (3 retry pairs = 6 rows):

```sql
SELECT dw_customer_key, connector_record_id, source_batch
FROM retail_raw.raw_dw_customer_snapshot
WHERE dw_customer_key IN (
  SELECT dw_customer_key
  FROM retail_raw.raw_dw_customer_snapshot
  GROUP BY dw_customer_key HAVING COUNT(*) > 1
)
ORDER BY dw_customer_key, connector_record_id
LIMIT 6
```

Use the result to show 3 concrete original/replay pairs in the proposal.

**Step 4 — Build and present the full proposal.** If all checks pass, substitute the attendee's database name into the SQL template below and present **all six sections**. Each is required.

**Section 1 — Preflight status:** Table of all check results (DB exists, target absent, schema columns, safeguard counts vs. expected).

**Section 2 — Source key & ordering evidence:** Show the live 3-pair table from query 3b. Then state the ordering rule: originals (`DW-LOAD-0000001`–`DW-LOAD-0002687`, batch `warehouse_20260923_01`) always sort before replays (`DW-LOAD-0002688`–`DW-LOAD-0002787`, batch `warehouse_20260923_replay`) under `ORDER BY connector_record_id ASC`. Note that `ROW_NUMBER()` alone does not prevent conflict records from being discarded — the `conflicting_keys = 0` check is the mandatory gate (it passed).

**Section 3 — Business field inventory:** Present as a table using the pre-validated counts below — do not re-query these fields. Columns: Field | Finding | Transformation | Flags produced.

| Field | Finding (pre-validated) | Transformation | Flags |
|---|---|---|---|
| `first_name`, `last_name`, `city`, `state`, `loyalty_status` | Preserved verbatim | None | None |
| `email_address` | 571 missing · 7 malformed · ~755 need lower/trim | `LOWER(TRIM(...))` → NULL if missing or fails `^[^\s@]+@[^\s@]+\.[^\s@]+$` | `trfm_email_changed`, `trfm_email_missing`, `trfm_email_invalid` |
| `phone_number` | 855 missing · 1,689 clean 10-digit · 243 with `+1` prefix | Strip non-digits; drop leading `1` from 11-digit; NULL if not 10-digit result | `trfm_phone_changed`, `trfm_phone_missing`, `trfm_phone_invalid` — ⚠️ US assumption |
| `address_line1` | Present; trim only | `TRIM(...)` | `trfm_address_missing`, `trfm_address_changed` |
| `postal_code` | 0 missing · 2,549 standard · 238 `NNN-NN` non-standard | `TRIM(...)` only; flag outside `^[0-9]{5}(-[0-9]{4})?$` | `trfm_postal_missing`, `trfm_postal_changed`, `trfm_postal_invalid` — ⚠️ US assumption |
| `marketing_opt_in` | `Y`, `true`, `N`, `false` only — 0 NULL | Map `Y`/`true` → `'true'`, `N`/`false` → `'false'` | `trfm_opt_in_missing`, `trfm_opt_in_invalid` |
| `lifetime_value` | 0 missing · 0 unparseable | `TRY_CAST(... AS DOUBLE)` | `trfm_ltv_missing`, `trfm_ltv_invalid` |
| `snapshot_date` | ISO `YYYY-MM-DD` · all TRY_CAST-valid | `TRIM(...)` as VARCHAR | `trfm_snapshot_date_missing`, `trfm_snapshot_date_invalid` |
| `connector_record_id`, `source_batch`, `time` | Ingestion metadata | Preserved verbatim | None |

**Section 4 — Projected counts:** Present this table (counts are on the 2,687 staged rows):

| Metric | Count |
|---|---|
| Raw rows | 2,787 |
| Identical same-key retries excluded | 100 |
| **Staged rows** | **2,687** |
| `trfm_email_missing = 1` | ~571 (21%) |
| `trfm_email_invalid = 1` | ~7 |
| `trfm_email_changed = 1` | up to ~755 |
| `trfm_phone_missing = 1` | ~855 (32%) |
| `trfm_phone_changed = 1` | phones with punctuation or `+1` prefix |
| `trfm_phone_invalid = 1` | 0 (all present phones are 10 or 11 digits) |
| `trfm_postal_invalid = 1` | ~238 (9%) — `NNN-NN` format |
| `trfm_ltv_missing` + `trfm_ltv_invalid` | 0 |
| `trfm_snapshot_date_invalid` | 0 |
| `trfm_opt_in_invalid` | 0 |

**Section 5 — Proposed SQL:** The pre-built SQL below with the staging DB name substituted, labeled `NOT EXECUTED`.

**Section 6 — Before/after examples and US-format approval questions:** Show the examples table, then ask the two ⚠️ US-format questions as explicit yes/no items. End with a single approval question covering source, target, transformations, and SQL.

Then wait for explicit approval before executing anything.

### ⚠️ US-format assumptions — always ask for attendee approval

1. **Phone:** 243 phones are 11-digit starting with `1` (e.g. `+1 000 555 8255`). The SQL strips the leading country code, producing a 10-digit result. This is a US-only rule. If non-US numbers are present, they would be incorrectly normalized.

2. **Postal code:** 238 postal codes follow a `NNN-NN` pattern (e.g. `100-42`) that does not match the US 5-digit or ZIP+4 format. The SQL flags them `trfm_postal_invalid = 1` using the pattern `^[0-9]{5}(-[0-9]{4})?$`. This is a US-centric validity rule.

Present both as explicit questions. If either is declined, revise the relevant section of the SQL and obtain renewed approval.

### Before/after examples (include in proposal)

| Key | Field | Raw | Transformed | Flag set |
|---|---|---|---|---|
| DW-000024 | email | `KENDALL.PATEL.F49565493B@MAIL.NORTHSTAR.EXAMPLE` | `kendall.patel.f49565493b@mail.northstar.example` | `trfm_email_changed=1` |
| DW-000024 | phone | `+1 000 555 8255` | `0005558255` | `trfm_phone_changed=1` |
| DW-000013 | email | `jules.baker.e33a0021af@mail.northstar.example` | same | `trfm_email_changed=0` |
| DW-000013 | phone | `0005555571` | same | `trfm_phone_changed=0` |
| DW-000013 | postal | `100-42` | `100-42` (preserved) | `trfm_postal_invalid=1` |
| DW-000042 | opt_in | `true` | `'true'` | — |

### Pre-built SQL template

Replace `<assigned_staging_database>` with the attendee's database name. Do not execute without explicit approval.

```sql
CREATE TABLE <assigned_staging_database>.stg_dw_customer_snapshot AS
WITH deduped AS (
  SELECT
    dw_customer_key,
    first_name, last_name, email_address, phone_number,
    address_line1, city, state, postal_code,
    loyalty_status, lifetime_value, marketing_opt_in, snapshot_date,
    connector_record_id, source_batch, time,
    ROW_NUMBER() OVER (
      PARTITION BY dw_customer_key
      ORDER BY connector_record_id ASC
    ) AS _rn
  FROM retail_raw.raw_dw_customer_snapshot
),
normed AS (
  SELECT *,
    -- email: lower+trim; NULL if missing or fails basic format check
    CASE
      WHEN email_address IS NULL OR TRIM(email_address) = ''
        THEN NULL
      WHEN NOT REGEXP_LIKE(LOWER(TRIM(email_address)), '^[^\s@]+@[^\s@]+\.[^\s@]+$')
        THEN NULL
      ELSE LOWER(TRIM(email_address))
    END AS _trfm_email,
    -- phone: strip non-digits; drop leading 1 from 11-digit +1 numbers; else NULL
    CASE
      WHEN phone_number IS NULL OR TRIM(phone_number) = ''
        THEN NULL
      WHEN LENGTH(REGEXP_REPLACE(phone_number, '[^0-9]', '')) = 11
           AND SUBSTR(REGEXP_REPLACE(phone_number, '[^0-9]', ''), 1, 1) = '1'
        THEN SUBSTR(REGEXP_REPLACE(phone_number, '[^0-9]', ''), 2, 10)
      WHEN LENGTH(REGEXP_REPLACE(phone_number, '[^0-9]', '')) = 10
        THEN REGEXP_REPLACE(phone_number, '[^0-9]', '')
      ELSE NULL
    END AS _trfm_phone
  FROM deduped
  WHERE _rn = 1
)
SELECT
  -- 16 raw columns
  dw_customer_key,
  first_name, last_name, email_address, phone_number,
  address_line1, city, state, postal_code,
  loyalty_status, lifetime_value, marketing_opt_in, snapshot_date,
  connector_record_id, source_batch, time,

  -- email
  _trfm_email                                                           AS trfm_email_address,
  CASE
    WHEN email_address IS NULL OR TRIM(email_address) = ''              THEN 0
    WHEN NOT REGEXP_LIKE(LOWER(TRIM(email_address)),
         '^[^\s@]+@[^\s@]+\.[^\s@]+$')                                 THEN 0
    WHEN _trfm_email IS DISTINCT FROM email_address                     THEN 1
    ELSE 0
  END                                                                    AS trfm_email_changed,
  CASE WHEN email_address IS NULL OR TRIM(email_address) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_email_missing,
  CASE
    WHEN email_address IS NOT NULL AND TRIM(email_address) != ''
         AND NOT REGEXP_LIKE(LOWER(TRIM(email_address)),
             '^[^\s@]+@[^\s@]+\.[^\s@]+$')                             THEN 1
    ELSE 0
  END                                                                    AS trfm_email_invalid,

  -- phone (US format — requires attendee approval)
  _trfm_phone                                                            AS trfm_phone_number,
  CASE
    WHEN phone_number IS NOT NULL AND TRIM(phone_number) != ''
         AND _trfm_phone IS NOT NULL
         AND _trfm_phone IS DISTINCT FROM phone_number                  THEN 1
    ELSE 0
  END                                                                    AS trfm_phone_changed,
  CASE WHEN phone_number IS NULL OR TRIM(phone_number) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_phone_missing,
  CASE
    WHEN phone_number IS NOT NULL AND TRIM(phone_number) != ''
         AND _trfm_phone IS NULL                                        THEN 1
    ELSE 0
  END                                                                    AS trfm_phone_invalid,

  -- address_line1
  TRIM(address_line1)                                                    AS trfm_address_line1,
  CASE WHEN address_line1 IS NULL OR TRIM(address_line1) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_address_missing,
  CASE WHEN TRIM(address_line1) IS DISTINCT FROM address_line1 THEN 1 ELSE 0 END
                                                                         AS trfm_address_changed,

  -- postal_code (US format — requires attendee approval)
  TRIM(postal_code)                                                      AS trfm_postal_code,
  CASE WHEN postal_code IS NULL OR TRIM(postal_code) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_postal_missing,
  CASE WHEN TRIM(postal_code) IS DISTINCT FROM postal_code THEN 1 ELSE 0 END
                                                                         AS trfm_postal_changed,
  CASE
    WHEN postal_code IS NOT NULL AND TRIM(postal_code) != ''
         AND NOT REGEXP_LIKE(TRIM(postal_code), '^[0-9]{5}(-[0-9]{4})?$') THEN 1
    ELSE 0
  END                                                                    AS trfm_postal_invalid,

  -- marketing_opt_in
  CASE
    WHEN marketing_opt_in IN ('Y', 'true')  THEN 'true'
    WHEN marketing_opt_in IN ('N', 'false') THEN 'false'
    ELSE NULL
  END                                                                    AS trfm_marketing_opt_in,
  CASE WHEN marketing_opt_in IS NULL OR TRIM(marketing_opt_in) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_opt_in_missing,
  CASE
    WHEN marketing_opt_in IS NOT NULL AND TRIM(marketing_opt_in) != ''
         AND marketing_opt_in NOT IN ('Y', 'true', 'N', 'false')       THEN 1
    ELSE 0
  END                                                                    AS trfm_opt_in_invalid,

  -- lifetime_value
  TRY_CAST(lifetime_value AS DOUBLE)                                     AS trfm_lifetime_value,
  CASE WHEN lifetime_value IS NULL OR TRIM(lifetime_value) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_ltv_missing,
  CASE
    WHEN lifetime_value IS NOT NULL AND TRIM(lifetime_value) != ''
         AND TRY_CAST(lifetime_value AS DOUBLE) IS NULL                 THEN 1
    ELSE 0
  END                                                                    AS trfm_ltv_invalid,

  -- snapshot_date
  TRIM(snapshot_date)                                                    AS trfm_snapshot_date,
  CASE WHEN snapshot_date IS NULL OR TRIM(snapshot_date) = '' THEN 1 ELSE 0 END
                                                                         AS trfm_snapshot_date_missing,
  CASE
    WHEN snapshot_date IS NOT NULL AND TRIM(snapshot_date) != ''
         AND TRY_CAST(snapshot_date AS TIMESTAMP) IS NULL               THEN 1
    ELSE 0
  END                                                                    AS trfm_snapshot_date_invalid,

  -- provenance
  CAST(to_unixtime(CURRENT_TIMESTAMP) AS BIGINT)                         AS stg_loaded_at

FROM normed
```

**ROW_NUMBER() caveat:** `ROW_NUMBER()` alone does not prevent conflicting records from being silently discarded. The `conflicting_keys = 0` safeguard check is the mandatory precondition. If it fails, do not proceed.

## TD SQL column type constraints

`CREATE TABLE AS SELECT` in Treasure Data supports only a limited set of output column types. Proposing an unsupported type causes a `[NOT_SUPPORTED]` error before any rows are written. Apply these rules when writing and reviewing staging SQL:

| Intended type | Use instead | Notes |
|---|---|---|
| `DECIMAL(p, s)` | `DOUBLE` | `DECIMAL` is unsupported; `DOUBLE` is the correct type for monetary and other decimal values |
| `DATE` | `VARCHAR` | `DATE` is unsupported as a column type; store the validated date string as `VARCHAR`. Use `TRY_CAST(... AS TIMESTAMP)` inside a `CASE` expression to test format validity, but return the original `VARCHAR` value as the column |
| `TIMESTAMP` / `TIMESTAMP(3)` | `BIGINT` or `VARCHAR` | `TIMESTAMP` is unsupported; for provenance columns (e.g. `stg_loaded_at`), use `CAST(to_unixtime(CURRENT_TIMESTAMP) AS BIGINT)` to store unix seconds |
| `CURRENT_TIMESTAMP` as a direct column | `CAST(to_unixtime(CURRENT_TIMESTAMP) AS BIGINT)` | `CURRENT_TIMESTAMP` returns `TIMESTAMP(3)`, which cannot be stored as a column |

**Important:** `TRY_CAST(... AS TIMESTAMP)` or `TRY_CAST(... AS DATE)` *can* be used inside `CASE` expressions to validate date-string format — the constraint applies to the *output column type*, not to expressions used within conditions.

## Approval and execution

- Ask for explicit approval of the **exact source, target, transformations, assumptions, and SQL**. Invite corrections and revise the proposal as needed. A change to the target or SQL requires renewed approval. A general request to "stage this" is not approval of an unseen write.
- After approval, recheck the account, source schema, source key, missing keys, business conflicts, deterministic ordering, database existence, and target absence immediately before execution. If any prerequisite fails or the source changed materially, **stop** and show an updated proposal; do not use `IF NOT EXISTS`, `CREATE OR REPLACE`, drop, truncate, insert into an existing table, or bypass the check.
- Create **only the one approved staging table**, once. Never modify `retail_raw` or any other existing table. Do not run or push workflows, run unification, create a Parent Segment, activate anything, or publish a dashboard. If execution fails or creates a partial target, report what happened; do not retry or overwrite automatically.

## Phase 2 — Read-only validation after creation

- Verify actual raw rows = staged rows + excluded **identical same-key** retries; staged rows equal distinct source keys; each staged source key occurs exactly once; and retained raw fields and provenance match the chosen source row. Report missing or unexplained rows rather than smoothing discrepancies.
- Measure the transformations and flags on **staged rows**, using explicit denominators. Check that missing and invalid flags do not overlap, that changed flags match raw-versus-transformed comparisons, and that missing/malformed match signals are NULL. Show a few actual before/after examples traceable by source key.
- Report the executed SQL, actual counts, validations that passed or failed, and any assumptions still open. Distinguish source-data findings, SQL failures, permission errors, missing setup, and unsupported requirements. Never claim validation when only SQL or an HTML file was generated.

## Response format

**Before approval (fast path):** Section 1 Preflight status → Section 2 Source key & ordering evidence (live retry pairs + ordering rule) → Section 3 Business field inventory (from pre-validated findings) → Section 4 Projected counts → Section 5 Proposed SQL (`NOT EXECUTED`, DB substituted) → Section 6 Before/after examples + US-format approval questions + single approval question. If any safeguard fails or the database is missing, label the plan `NOT EXECUTED` and identify the blocker.

**Before approval (other identity sources):** Preflight status → source key and retry/ordering evidence → transformation inventory with flags and examples → projected counts → exact SQL → assumptions and approval question. If blocked, label the plan `NOT EXECUTED` and identify the blocker.

**After execution:** Exact target and executed SQL → actual reconciliation and flag counts → actual before/after examples → exceptions or failed checks. Do not present projected figures as measured staged results.

## Other identity sources (generic fallback)

Inspect only the specified table and attendee target. Do not reuse `dw_customer_key`, the 2,787/2,687/100 totals, US-format rules, or the DW SQL without verifying them for this source.

1. Check that the assigned staging database exists and the target table does not. If the database is missing, the target exists, or visibility is blocked by permissions, explain the distinct issue and **do not write**. A missing database may still allow a read-only proposal clearly labeled `NOT EXECUTED`; never create a database, overwrite a table, or choose a substitute target.
2. Inspect the actual source schema, bounded samples, row count, null/blank key count, distinct source-key count, and duplicate-key groups. Identify the source key from the schema and data; `dw_customer_key`, `marketing_contact_id`, `shopper_id`, and `loyalty_member_id` are possibilities, not universal defaults. Stop if the key is absent, ambiguous, null, or blank. Keep different source keys separate even when email or phone matches.
3. Classify business fields versus ingestion metadata **for this source** and show the classification. Check same-key business variants with a null-safe, field-by-field comparison: conceptually, `SELECT DISTINCT source_key, <all business fields>` followed by a count of variants per source key. Do not concatenate fields with delimiters, coalesce NULL to empty, or assume `COUNT(DISTINCT field) = 1` means all values agree (an all-NULL field yields 0). If any key has conflicting business variants, stop for review; never pick a winner based on time.
4. Identify a reliable ingestion-order column and deterministic tiebreaker. Verify ordering on sample retry pairs and check uniqueness or ties. Use the **earliest ingested** record per source key, not the latest by default. A `time` column may represent an event, partition, or tied replay time; do not assume it alone orders ingestion. If ordering is ambiguous, stop and ask.
5. Inventory **every business field**, proposing useful, conservative, deterministic transformations where supported by observed data. Keep raw fields unchanged and add `trfm_*` values and relevant `trfm_*_changed`, `trfm_*_missing`, and `trfm_*_invalid` flags. Explain any inapplicable flag instead of fabricating a rule. Define changed with null-safe comparison; distinguish missing/blank from present-but-malformed so they are not both flagged invalid. Show a few projected before/after examples with source keys.
   - For email/phone used as match signals, make the match-ready normalized value NULL when missing or failing the approved format rule; retain the raw value and reason flag. A valid format is not proof of a person match. Do not assume country-specific phone rules without evidence and approval.
   - For postal codes, preserve leading zeroes and do not rewrite an unusual format into a guessed code. Label format anomalies for review; use a country-specific validity rule only when supported and approved.
   - For consent, map observed encodings only when unambiguous. A normalized opt-in is a **source observation**, not a settled contact-eligibility decision.
   - For monetary strings, use `DOUBLE` with `TRY_CAST`; use a safe cast and report invalid values. (`DECIMAL` is unsupported as a column type in TD's `CREATE TABLE AS SELECT` — see TD SQL column type constraints above.)
   - If a field needs no useful transformation, state why; do not add a pointless derived column. Keep staging/provenance metadata distinct from transformation columns.
6. Show the exact source-to-target mapping, projected counts, proposed SQL, flag definitions, and any assumptions requiring approval. Use direct Treasure Data SQL appropriate to the active engine, not a workflow. Make clear that `ROW_NUMBER()` alone does **not** prevent conflicting records from being discarded; the conflict check is a mandatory precondition. Follow the same approval and execution rules above.

If the table does not fit this one-key identity-staging pattern, stop and discuss scope.

## Example

**Input:** `/stage-table retail_raw.raw_dw_customer_snapshot retail_stg_user001_test`

**Expected behavior:** Confirm the proposed `retail_stg_user001_test.stg_dw_customer_snapshot`; run the 3 safeguard checks (schema, combined row/conflict query); substitute the DB name into the pre-built SQL; show the US-format approval questions and before/after examples; ask for approval. If the assigned database is missing, provide only a `NOT EXECUTED` plan. Do not carry this source's key, counts, ordering column, or SQL over to a different identity table without verifying them again.

> Draft for rehearsal. The pinned recipe and CTAS type observations come from prior Studio rehearsal. Test one approved create-and-validate cycle before distributing to attendees; skill instructions are not a substitute for database permissions.
