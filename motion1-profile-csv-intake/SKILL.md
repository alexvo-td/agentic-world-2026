---
name: agenticworld-profile-csv-intake
description: Prepare a Agentic World workshop audience CSV by collecting participant information in one interaction and adding 30 fictional profiles with safe test recipients. Use for workshop self-send, sample audiences, profile CSV creation, or personalized email previews. Check existing tdx 2026.9.3 before campaign setup without reinstalling a correct runtime. Hand campaign creation and delivery to motion1-csv-list-campaign.
---

# Motion 1 — Make your workshop email personal

Use English for participant instructions, questions, previews, and completion messages. Keep technical settings backstage. Prepare the CSV and runtime check only; do not authenticate, query TD, create campaigns, or send emails here.

## Collect everything in one interaction

Reuse all answers already supplied. Resolve the selected template's required personalization fields from the existing brief before asking. Request all missing information in one compact form, rather than one question at a time:

> Please fill in the missing details below so I can prepare your workshop audience:
> - Email address: your own address, if you want to receive the workshop email
> - First name:
> - Last name:
> - Company Name
> - Delivery mode: receive the email after final approval, or preview only
>
> I will add 30 fictional profiles for the demonstration. In delivery mode, these use approved test recipients. Creating the CSV does not send any email.

Omit questions already answered. Include only personalization fields actually needed; mark optional fields as optional. Treat an explicit request to send to the participant's own supplied address as their self-send opt-in. Ask follow-up questions only for missing required values or ambiguities, grouping them in one message. Do not ask participants to choose types, merge-tag syntax, mappings, or CLI flags.

## Reuse approved workshop settings

Use existing operator-approved purpose, collection/retention, Work Folder access, downstream TD query/job-history exposure, save destination, delivery provider, and file/row/SQL limits. Resolve missing workshop settings with the operator once, in a grouped request; do not repeat them for every participant.

For third-party real profiles, require data-owner approval for purpose, collection, retention, and destination. Without approval, collect field names only and request an approved local CSV instead of real rows in chat.

Do not collect credentials, tokens, government IDs, payment data, or unrelated sensitive information. Do not infer, normalize, repair, or silently drop real values. Resolve ambiguity, required blanks, and duplicates with the participant. Keep full real addresses and rows out of shared summaries, technical handoffs, and shell arguments. Use private review only where approved. Never put real profiles in a Skill or source repository.

## Check the existing tdx runner

Skip this step for CSV-only requests. When continuing to campaign operations, run in the exact runtime that will execute the campaign:

```bash
tdx --version
```

Require successful execution reporting exactly `2026.9.3`. If correct, reuse the installed `tdx` command. Skip installation, updates, npx preparation, and offline-cache checks. Record runtime identity, version, runner, and check time in the non-PII handoff. Do not reuse a check from another runtime.

If tdx is missing, fails, or has a different version, report the result to the operator and use an already approved exact-version fallback only if one exists. Otherwise mark the campaign handoff blocked until the operator fixes the runtime; CSV preparation can continue. Do not install globally, silently update, select latest, or bypass denied permissions. Distinguish compatibility warnings from command failure. This Skill's only tdx operation is the version check.

## Build the audience CSV

Default to one participant profile plus exactly 30 synthetic profiles: 31 rows total. Honor an explicitly requested different count or synthetic-only mode. For an existing uploaded customer list, preserve the source and confirm the intended audience composition before adding rows; do not assume it contains only the participant.

Use lowercase `email`, `first_name`, `last_name`, and SQL-safe lowercase optional headers. Generate fictional names and plausible randomized values for the same personalization columns. Keep real values unchanged. Do not copy the participant's attributes to every synthetic row. Use bounded choices suitable for the selected email, without unrelated sensitive attributes or invented real contact details.

### Choose test recipients

For a confirmed Amazon SES delivery path, assign these 30 distinct addresses:

```text
success+motion1-001@simulator.amazonses.com
...
success+motion1-030@simulator.amazonses.com
```

Use these as synthetic recipient values, never random addresses at real domains. Amazon SES supports labels on mailbox simulator addresses. The `success` scenario simulates successful delivery; it does not provide a human inbox for reading, opening, or clicking. Simulator sends require SES and incur normal send charges. They do not affect SES daily sending quota or bounce/complaint rates, but remain subject to sending-rate limits. Do not promise that Engage reporting excludes simulator traffic or that application validation, suppression, or campaign limits are bypassed.

Source: https://docs.aws.amazon.com/ses/latest/dg/send-an-email-from-console.html

If the delivery provider is unknown, resolve it with the operator once. For a non-SES path, use explicitly approved operator-controlled test inboxes or aliases, with receive capability verified for this workflow. Do not invent a universally deliverable address. Never silently omit synthetic recipients or switch a requested live audience to preview mode.

For preview-only mode, use unique `profile-001@example.test` through `profile-030@example.test` addresses; omit a real email if unnecessary and use a fictional address for the participant-shaped row. Mark the whole CSV preview-only and prevent it from being handed off as sendable.

### Validate and write

Use UTF-8 and standard CSV quoting. Validate required values, email syntax, consistent field counts, unique email keys, required blanks, recipient classes, and row count. Preserve plus labels as part of each unique address. For the default live flow require exactly one opted-in participant address and 30 approved simulator/test addresses. Resolve failures rather than dropping rows.

Use existing approved key/blank policy and file/row/SQL limits. Downstream non-time fields are text; `time`, if present, is Unix seconds. Normally omit `time` so the helper can add ingest time. Do not promise unsupported numeric/date types, multiline cells, or large/batched processing.

Save a new file in the approved Work Folder. Preserve original files. Use a unique filename rather than overwrite. If the user has requested CSV creation and the destination and data handling are already approved, that request authorizes saving; do not ask for redundant save approval. Resolve an unknown, unauthorized, or over-shared destination before writing real profiles.

Show a masked summary: purpose, field names, data mode, participant/synthetic/total counts, new filename, destination, validation result, and whether recipients are sendable. Saving never authorizes delivery.

## Handoff to campaign creation

Tell the participant: “Your CSV is saved. Let’s create the email and preview it.” For CSV-only requests, report completion without initiating campaign setup.

Keep this handoff backstage and include no profile values or credentials:

```text
CSV file: <approved absolute path>
Collection/retention/destination approval: confirmed
Workshop self-send opt-in: confirmed
Columns/types: <names and types only>
Rows: <total>; participant: <count>; synthetic: <count>
Sendable: yes
Unique key: email
TDX runner: installed tdx 2026.9.3 verified | not-checked | blocked
Runtime/checked at: <runtime identity and check time>
Campaign brief: <purpose, tone, workspace/template/name; no profile values>
Validation: passed | blocked <aggregate counts and reasons>
Next: motion1-csv-list-campaign
```

When asked to continue, invoke `motion1-csv-list-campaign` with the saved path and existing answers. If unavailable, provide a follow-up prompt. The campaign Skill must revalidate the saved file and reuse the verified runner. Do not claim the campaign Skill was updated by creating this Skill. If it enforces a conflicting one-recipient-only rule, report the conflict to the operator before campaign creation; do not silently shrink the audience or override it.

Require a separate final delivery approval in the campaign Skill, showing the actual recipient composition, for example “1 participant + 30 SES simulator recipients = 31 total.” Preview-only recipients must never be sent. No send approval is requested or exercised here.

## Examples

- “Create a workshop email with my name and send it to me after I approve.” Collect all missing fields once; generate 1 participant plus 30 SES simulator profiles when SES is confirmed; check installed tdx only when continuing; save a new approved CSV; hand off for preview and final send approval.
- “Here are my email, first name, and last name; create the CSV.” Reuse supplied values, ask only for genuinely missing required information, and save without repeating an already authorized save step.
- “Try fictional profiles without sending.” Generate preview-only `example.test` profiles; omit unnecessary real data; save the CSV; skip the version check unless continuing to campaign operations.
- “tdx reports 2026.9.3.” Verify in the actual campaign runtime unless this session already has a successful check for that same runtime; reuse the installed runner without package preparation.
