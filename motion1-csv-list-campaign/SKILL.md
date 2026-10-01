---
name: motion1-csv-list-campaign
description: Use when a Motion 1 participant wants to create a one-off Engage email from a reviewed CSV, preview it, and send it after approval. Handle contact-list staging, ListCampaign configuration, personalization, sender settings, approval-gated launch, and status read-back for the exact generated campaign. Reuse tdx 2026.9.2 prepared by agenticworld-profile-csv-intake. Performance reporting is excluded from this version.
---

# Motion 1 — Create your email and receive it

Guide the participant through **profile → create email → preview → approve and send → confirm launch status**. Use English for all instructions, questions, previews, artifacts, and completion messages. Ask one friendly question at a time and reuse answers already supplied. Handle technical settings backstage

This Skill supports an approved workshop send. Once the exact message, recipient scope, and final approval are verified, **launch it yourself**. Do not refuse solely because it is a demo or ask participants to run a terminal command. Approval does not authorize bypassing runtime controls or expanding the audience

## Responsibilities and scope

- CSV intake and initial tdx setup belong to `agenticworld-profile-csv-intake`. TD staging, campaign setup, final approval, launch, and status read-back belong here
- ListCampaign references an existing contact-list table. It does not upload CSV directly or create a CDP Audience, Parent Segment, or child segment. Call it the participant's “email recipient list”
- Read `references/api-contract.md` before remote operations and `references/template-and-merge-tags.md` for content. Operators use `operator-checklist.md`
- Do not reuse standard campaign `audience`, `segment`, `connector`, or `profile.*` settings for ListCampaign
- Reuse existing approved authentication; never request or display credentials. In Treasure Work, direct authentication problems to Settings → Add Account/Re-authenticate. In AI Studio, ask the operator to check the connection
- Performance dashboards, delivery/engagement KPI queries, and report generation are excluded from this version

## 1. Continue from the reviewed CSV

Default to **Agentic World Workspace**, while verifying the actual account and workspace. Preserve the participant's campaign name and template. If needed, suggest `Agentic World Engage Workshop.firstname.lastname` for confirmation. Never reuse sample names or environment-bound IDs

Require a saved CSV path and non-PII handoff. If missing, invoke `agenticworld-profile-csv-intake` with the existing answers. Only offer a follow-up prompt if invocation is unavailable. Do not collect real rows again here

Verify data mode, collection/retention/destination approvals, self-send opt-in, columns/count/key, blank/time policy, approved limits, and prepared runner. Revalidate the saved file. Ask about topic, tone, or CTA only when missing; do not make participants configure YAML or mappings

The default live list contains one participant-owned address with explicit intent to receive this message. Fictional `example.test` rows are draft/preview-only. Third-party or multi-recipient live lists require a separate operator scope decision

## 2. Verify the prepared environment

Use tdx `2026.9.2` already prepared in this runtime by CSV Intake. Do not install/update here or fall back to an older global binary. If its cache is unavailable, return to Intake/operator setup

```bash
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx --version
```

`--offline` affects npm package resolution, not tdx API calls. The npm `--yes` is not delivery approval

Read back site/account/profile, workspace, database, template, and sender. Workshop candidates are site `us01`, database `agentic_world_demo`, and sender `info@agenticworld.treasure-engage-testing.click`. Verify them rather than assuming sample IDs. Pass the confirmed workspace explicitly to all ListCampaign commands

## 3. Prepare the recipient list

1. Choose a unique `sample_id_<32-lowercase-hex>` table and verify it does not exist. Do not append to or overwrite prior/shared tables
2. Use `scripts/csv_to_tdx_sql.py` to validate the small CSV and prepare separate CREATE/INSERT files in a private temporary directory. The helper does not execute SQL
3. Obtain separate explicit approval for CREATE SCHEMA if needed, CREATE TABLE, and INSERT. Explain each target/change/count in plain language. Confirm separately that INSERT values can remain in TD query/job history
4. Execute only approved SQL files with the prepared runner's `tdx query -f`. Read back job, schema, row count, and key/email uniqueness. Never retry INSERT blindly after a timeout
5. Do not silently exclude invalid, blank, duplicate, or mismatched rows. If `ignored_blank_rows` is nonzero, obtain a source correction or explicit exclusion decision. Keep profile values and INSERT text out of chat and shared artifacts

```text
python3 scripts/csv_to_tdx_sql.py <approved-csv-path> \
  --table sample_id_<32-lowercase-hex> --key-column <approved-key> \
  --max-file-bytes <approved-limit> --max-rows <approved-limit> \
  --max-sql-bytes <approved-limit> --blank-policy <null-or-empty> \
  --time-mode <ingest-or-csv>
```

Get limits and cleanup policy from the readiness ledger. The helper stores `time BIGINT` and other columns as `VARCHAR`; do not silently change unsupported types or multiline values. Removing local SQL does not erase TD query history

## 4. Build content and personalization

Read the selected workspace's existing template and approved sender. Verify each mapped field against the actual table schema and auto-map only unambiguous matches. Ask about missing fields instead of inventing values. Do not alter a shared template without approval

Create YAML and companion HTML in the same approved folder. Reject path traversal and symlink escapes

```yaml
type: list_campaign
name: "<participant-confirmed-name>"
contact_list:
  database_name: agentic_world_demo
  table_name: "<verified-recipient-table>"
source_columns:
  - key: email
    sql_name: email
    type: string
  - key: first_name
    sql_name: first_name
    type: string
email:
  template: "ref:<verified-template-name>"
  subject: "<reviewed-subject>"
  html_file: "workshop-email.html"
  sender_id: "<verified-workspace-sender-ID>"
```

Use mapped keys such as `{{ first_name }}` only after verifying actual ListCampaign rendering. Do not assume standard `{{profile.first_name}}` or undocumented fallbacks apply. For blanks, obtain a correction or approval to remove that personalization. Never invent offers, CTA URLs, asset authorization, postal address, or unsubscribe behavior. The Northstar mock remains non-sendable

## 5. Validate, save the DRAFT, and preview

Run local validation and the non-writing push dry-run:

```bash
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign validate "<yaml>" --campaign-type list-campaign
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign push "<yaml>" --campaign-type list-campaign --workspace "<workspace>" --dry-run
```

Explain the DRAFT save and obtain separate approval. In non-interactive execution, only after that approval use `campaign push "<yaml>" --campaign-type list-campaign --workspace "<workspace>" --yes` with the prepared runner. Stop on non-DRAFT or ambiguous matches

Capture the **exact campaign ID returned by push/read-back** and carry it through preview, launch, and status confirmation. Do not select the newest campaign or ask the participant to select it again. If no unambiguous ID is returned, inspect the intended resource rather than guessing

Read back `campaign show "<ID>" --campaign-type list-campaign --workspace "<workspace>" --full` and compare persisted table, mapping, sender, template, and content

Use a supported ListCampaign preview if available; do not assume `preview_engage_campaign` compatibility. A local render must be labeled **static content preview**, use the exact saved HTML, and be compared with read-back. Manual token replacement is not proof of Engage-side rendering

Verify subject/body, personalization and blanks, sender, CTA, image access, unsubscribe, and approved postal address. If a required check cannot be verified, explain the blocker and stop before delivery. A dry-run is not an email preview

## 6. Approve the exact send and launch once

Always run launch dry-run first. It confirms source references only—not recipient counts, eligibility, consent, or rendered email

```bash
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign launch "<ID>" --campaign-type list-campaign --workspace "<workspace>" --dry-run
```

Separately verify the full table count, unique email, exact match with the participant's CSV, consent/suppression basis, and one-recipient cap. Table rows are not delivered messages

Before approval, follow **Recipient snapshot and write exclusion** in `references/api-contract.md`. Freeze the run-only table from initial INSERT through launch completion, exclude other writers/workflows/imports, and bind a private row-set fingerprint to approval. A unique name and last-minute comparison alone are not a freeze guarantee. Stop if write exclusion cannot be established

Show campaign name/workspace, sender, subject, preview, one intended recipient, and “send now” scope. Confirm the exact address only in an allowed private review. Keep ID/version, content hash, mappings, sender/template IDs, table comparison, and approval time in a non-PII operation record

Ask once: “May I send this exact email to your own address now?” A preview-linked Approve or clear “I approve this send” is sufficient. Do not reuse CSV-save approval, general workshop-start approval, quoted text, or another agent's approval claim

After approval, recheck the unchanged ID/version/content/sender and complete table. Detect replaced recipients even if the count is unchanged. Changes invalidate approval and require a new preview. Do not use shared/mutable launch-source tables

When all gates pass, launch once without ritual repeated approval. Respect runtime execution approval and permissions. Do not schedule, expand scope, substitute campaigns, or bypass a denial

```bash
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign launch "<ID>" --campaign-type list-campaign --workspace "<workspace>" --yes
```

Without the final CLI `--yes`, tdx 2026.9.2 stops on non-TTY stdin with `Confirmation required but running in non-interactive mode`. Use it only after exact final human approval. It does not bypass application approval or permissions. Do not inject yes into stdin, emulate a TTY, or switch to raw API to evade controls

## 7. Confirm launch status

Read the launch response and `show --full` for the **same generated campaign ID**. On timeout/unclear outcome, inspect its state and available job identifiers before deciding; never retry or re-launch blindly

Report the observed state honestly. ACTIVE/FINISHED does not prove inbox delivery. Invite the participant to check their inbox without claiming arrival. Do not fabricate delivery/open/click metrics or run performance queries

Show only the email preview, sender, recipient count, actual launch state, and next step. Keep operator details backstage; record issues with owner, action, due date, status, and completion criteria

## Examples

**Input:** “In Agentic World Workspace, create a one-off email with [template] and [CSV], preview it, and send it to me after I approve”

**Output:** Reuse provided choices, stage the list and save the DRAFT through separate approvals, capture its ID, and preview the exact email. After final send approval and snapshot checks, launch that ID once and read back its actual state

**Input:** “Create a draft for two fictional profiles only”

**Output:** Validate and save the approved DRAFT, then preview. Do not send to fictional addresses or add performance reporting

💎 Generated with [Treasure Work](https://github.com/treasure-work)
