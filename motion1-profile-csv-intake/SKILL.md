---
name: motion1-profile-csv-intake
description: Use when a Motion 1 workshop participant wants to add themselves to a sample audience, create a profile CSV, or try personalized email with synthetic data. Collect email, first name, last name, and only fields needed for personalization; save a reviewed CSV in the approved Work Folder. Bootstrap tdx 2026.9.2 here when continuing to campaign setup. Hand campaign creation and delivery to motion1-csv-list-campaign.
---

# Motion 1 — Make your workshop email personal

Help the participant prepare the profile for their personalized email. Use English for all instructions, questions, previews, and completion messages. Ask one friendly question at a time, reuse answers already supplied, and keep technical settings backstage

## Participant journey

1. Ask whether they want to receive one email at their own address or try a fictional profile without sending
2. Collect email, first name, and last name. Request additional fields only if the selected email needs them
3. Prepare the workshop runtime backstage when continuing to campaign setup
4. Review the fields, row count, and save destination. Save a new CSV after explicit approval
5. Hand the saved path to the campaign Skill. Explain that the completed email will be previewed and sent only after a separate final approval

Ask “What name would you like the email to use?” or “Would you like to personalize anything else? You can skip this.” Do not make participants choose SQL types, merge-tag syntax, mappings, or CLI flags

## Data handling

- Confirm operator-approved purpose, chat collection/retention, Work Folder access, and downstream TD query/job-history exposure. Ask the operator once if missing; do not repeat approved setup questions for each participant
- For self-send, confirm the participant's own address and intent to receive this one email. The default live list contains exactly one participant. CSV-save approval is not delivery approval
- For third-party real data, require data-owner approval for purpose, collection, retention, and destination. Without it, collect field names only and request an approved local CSV instead of real rows in chat
- Use fictional `example.test` addresses for synthetic profiles. They are **preview-only**, not deliverable recipients
- Do not collect credentials, tokens, government IDs, payment data, or unrelated sensitive information
- Do not infer, normalize, repair, or silently exclude real values. Ask about ambiguity, blanks, and duplicates
- Keep full addresses and profile rows out of shared artifacts, handoffs, and shell arguments. Mask summaries; use a private participant review only when policy permits

## Prepare the pinned tdx runner

This Skill owns initial tdx pre-release setup. The campaign Skill must not install or update it. Skip setup for a CSV-only or fictional-preview-only request

Run this in the same approved runtime that will execute the campaign. The first invocation may download the exact package into its local cache. Never install globally or silently switch to the latest release

```bash
npx --yes --package=@treasuredata/tdx@2026.9.2 tdx --version
```

- Confirm successful execution and version `2026.9.2`; do not reuse another environment's check
- Confirm `npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx --version` also succeeds so campaign commands need no package download
- Record verified runtime, version, runner, and check time in the non-PII handoff
- npm `--yes` confirms package preparation only; it does not approve TD writes or sends
- Distinguish compatibility warnings from execution failures. If setup fails, explain that the operator must check the workshop runtime. Do not bypass denied permissions or safety controls
- Version checks are the only tdx operations here. Do not authenticate, query TD, inspect tables, prepare SQL, create campaigns, or launch/send

## Build the CSV backstage

- Require lowercase `email`. Use `first_name`, `last_name`, and SQL-safe lowercase names for optional columns
- Use approved key/blank policy and file/row/SQL limits from the readiness ledger. Self-send is one row; synthetic fixtures may contain multiple rows
- The downstream helper stores non-time fields as text and `time` as Unix seconds. Normally omit `time` so it can add ingest time later
- Do not promise unsupported numeric/date types, multiline cells, or large/batched processing
- Use UTF-8 and standard CSV quoting. Validate required values, email format, field counts, duplicates, and blanks. Ask about errors instead of silently dropping rows

When adding someone to a sample CSV, preserve the original and save a new version. The live self-send version contains only that participant—not fictional addresses or other participants. Explain and confirm this distinction

## Review and save

Show purpose, field names, data mode, row count, new filename, approved destination, and validation result. Mask real values in shared summaries. Ask for explicit save approval and explain that this action does not start delivery

Save only a new file. If the destination is unknown, unauthorized, over-shared, or already exists, stop and confirm another path. Never save real profiles inside a Skill or source repository

## Internal handoff

Tell the participant “Your CSV is saved. Let’s create the email and preview it.” Keep this technical handoff backstage; include no profile values or credentials

```text
CSV file: <approved absolute path>
Data mode: synthetic | participant-self | owner-approved-real
Collection/retention/destination approval: confirmed | missing | not-applicable
Workshop self-send opt-in: confirmed | missing | not-applicable
Columns/types: <names and types only>
Rows: <count>
Unique key: <column>
Blank/time policy: <approved policy>
Limits: <approved file/row/SQL limits>
TDX runner: 2026.9.2 verified | not-prepared | blocked
Runtime/checked at: <runtime and check time>
Campaign brief: <purpose, tone, workspace/template/name; no profile values>
Validation: passed | blocked <aggregate counts and reasons>
Next: motion1-csv-list-campaign
```

When asked to continue, invoke `motion1-csv-list-campaign` with existing answers and the CSV path. Offer a follow-up prompt only if invocation is unavailable. The campaign Skill revalidates the saved file

## Examples

**Input:** “Create a workshop email with my name and send it to me after I approve”

**Output:** Verify data handling and the participant's intent to receive one email. Collect needed fields, prepare tdx backstage, review the one-row destination, and ask before saving. Continue to email creation without sending from this Skill

**Input:** “Try two fictional profiles without sending anything”

**Output:** Create a preview-only `example.test` CSV and ask before saving. Prepare tdx only when continuing to campaign operations. Do not apply the one-recipient live-send restriction to synthetic fixtures

💎 Generated with [Treasure Work](https://github.com/treasure-work)
