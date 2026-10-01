---
name: agenticworld-profile-csv-intake
description: Prepare a workshop audience CSV by reusing supplied profile values, asking once in an ordinary message for missing required values, and adding 30 approved test recipients. Use for workshop audience CSV creation and personalized email preparation. Reuse installed tdx 2026.9.3 or prepare and verify that exact version with npx before handing campaign work to setup-campaign.
---

# Motion 1 — Make your workshop email personal

Use English for participant instructions, questions, previews, and completion messages. Keep technical settings backstage. Prepare the CSV and verified runtime handoff only; do not authenticate, query TD, create campaigns, or send emails here.

## Collect missing profile information once

Reuse every value already supplied. Determine required personalization fields from the selected template and existing brief. If required values are missing, ask for all and only those values together in one ordinary chat message. Do not use `AskUserQuestion`, a structured Question interaction, or a form. If all required values are already available, do not ask again; continue directly to CSV preparation.

Use a short grouped prompt, for example:

> To personalize your workshop email, please send the missing details together: email address, first name, and last name. Add company only if the selected template requires it.

Adapt the list to the actual missing fields. Collect `company` or other optional fields only when the selected template requires them. Ask a follow-up only to resolve an ambiguity, invalid value, required blank, or duplicate. Do not ask participants to choose field types, merge-tag syntax, mappings, CLI flags, delivery providers, or test-recipient settings.

## Use the workshop send flow

The workshop flow prepares the audience, creates and previews the email, and hands it to `setup-campaign` for the requested send. Do not ask for a delivery mode, offer preview-only or skip-send options, or add a separate self-send opt-in question. The request to run the workshop flow and the participant-provided address authorize preparation within the established scope, but sending still requires the single final confirmation after the exact campaign preview and recipient set are shown. Do not interpret a CSV-only request as authorization to send.

Keep participant-facing wording simple: “We'll use your details to personalize your workshop email and add 30 approved test profiles for the demonstration.” Keep delivery infrastructure, SES, simulator addresses, quotas, and technical validation backstage. Do not ask marketers to approve or configure those details. This Skill prepares the CSV; the campaign Skill performs the actual send. Do not claim delivery until the campaign Skill confirms the observed launch state.

## Reuse approved workshop settings

Use existing operator-approved purpose, collection/retention, Work Folder access, downstream TD query/job-history exposure, save destination, delivery provider, and file/row/SQL limits. Resolve a genuine missing workshop policy with the operator once in a grouped request; do not repeat already approved settings for every participant.

For third-party real profiles, require data-owner approval for purpose, collection, retention, and destination. Without approval, collect field names only and request an approved local CSV instead of real rows in chat.

Do not collect credentials, tokens, government IDs, payment data, or unrelated sensitive information. Do not infer, normalize, repair, or silently drop real values. Resolve ambiguity, required blanks, and duplicates with the participant. Keep full real addresses and rows out of shared summaries, technical handoffs, and shell arguments. Use private review only where approved. Never put real profiles in a Skill or source repository.

## Verify or prepare the tdx runner

Skip runtime setup for CSV-only requests. For campaign continuation, work in the exact runtime that will execute the campaign. Treat the required version check as authorized read-only setup: run it without asking “May I run this?” or announcing “Command I’ll run” and waiting for approval. If npx preparation is needed, do not request a separate conversational approval for this authorized setup step. Always respect host/runtime permission prompts; never bypass them.

First check the installed runner:

```bash
tdx --version
```

If it succeeds and reports exactly `2026.9.3`, reuse the installed `tdx` command. Do not install, update, or prepare it with npx.

If `tdx` is missing, fails, or reports another version, prepare and verify the pinned workshop version with:

```bash
npx --yes --package=@treasuredata/tdx@2026.9.3 tdx --version
```

Proceed only when that command succeeds and reports exactly `2026.9.3`. Use the same invocation prefix—`npx --yes --package=@treasuredata/tdx@2026.9.3 tdx`—for every campaign command and pass it unchanged in the handoff. Do not install globally, choose `latest`, switch versions, or bypass denied permissions. If exact-version preparation or verification fails, CSV preparation may continue but mark campaign execution blocked. Record the runtime identity, verified version, exact runner command, and check time. Never reuse a check from another runtime.

## Build the audience CSV

Default to one participant profile plus exactly 30 approved test profiles: 31 rows total. These are the actual workshop send targets when the workshop send flow is requested; do not silently exclude or relabel the approved test recipients as preview-only. Honor an explicitly requested different count or synthetic-only mode only when that scope is approved. For an existing uploaded customer list, preserve the source and confirm the intended audience composition before adding rows; do not assume it contains only the participant.

Use lowercase `email`, `first_name`, `last_name`, and SQL-safe lowercase optional headers. Generate fictional names and plausible randomized values for the same personalization columns. Keep real values unchanged. Do not copy the participant's attributes to every synthetic row. Use bounded choices suitable for the selected email, without unrelated sensitive attributes or invented real contact details.

### Choose approved test recipients

For a confirmed Amazon SES delivery path, use these 30 distinct addresses:

```text
success+motion1-001@simulator.amazonses.com
...
success+motion1-030@simulator.amazonses.com
```

Use these as test recipient values, never random addresses at real domains. Amazon SES supports labels on mailbox simulator addresses. The `success` scenario simulates successful delivery; it does not provide a human inbox for reading, opening, or clicking. Simulator sends require SES and incur normal send charges. They do not affect SES daily sending quota or bounce/complaint rates, but remain subject to sending-rate limits. Do not promise that Engage reporting excludes simulator traffic or that application validation, suppression, or campaign limits are bypassed.

Source: https://docs.aws.amazon.com/ses/latest/dg/send-an-email-from-console.html

If the delivery provider is unknown, resolve it with the operator once. For a non-SES path, use only explicitly approved operator-controlled test inboxes or aliases whose receive capability is verified for this workflow. Do not invent universally deliverable addresses. `example.test` addresses are preview-only and are not sendable recipients. Never silently omit test recipients or stop a requested send flow after preview.

### Validate and write

Use UTF-8 and standard CSV quoting. Validate required values, email syntax, consistent field counts, unique email keys, required blanks, recipient classes, and row count. Preserve plus labels as part of each unique address. For the default workshop send flow require exactly one authorized participant address and 30 approved test addresses. Resolve failures rather than dropping rows.

Use existing approved key/blank policy and file/row/SQL limits. Downstream non-time fields are text; `time`, if present, is Unix seconds. Normally omit `time` so the helper can add ingest time. Do not promise unsupported numeric/date types, multiline cells, or large/batched processing.

Save a new file in the approved Work Folder. Preserve original files. Use a unique filename rather than overwrite. When CSV creation is requested and the destination and data handling are already approved, that request authorizes saving; do not ask for redundant save approval. Resolve an unknown, unauthorized, or over-shared destination before writing real profiles.

Show a masked summary: purpose, field names, data mode, participant/test/total counts, new filename, destination, validation result, and sendability. For CSV-only requests, saving does not authorize delivery. For the workshop send flow, carry the send instruction and the actual participant-plus-test recipient composition into the campaign handoff without asking for a delivery-mode selection.

## Handoff to campaign creation

Tell the participant: “Your CSV is saved. Let's create the email and preview it.” For CSV-only requests, report completion without initiating campaign setup.

Keep this handoff backstage and include no profile values or credentials:

```text
CSV file: <approved absolute path>
Collection/retention/destination approval: confirmed
Workshop send instruction: requested | CSV-only (no send requested)
Recipient authorization: participant-provided workshop address + approved test-recipient set | not applicable
Columns/types: <names and types only>
Rows: 31; participant: 1; approved test recipients: 30
Sendable: yes | no <aggregate reason>
Unique key: email
TDX version: 2026.9.3 | blocked
TDX command: tdx | npx --yes --package=@treasuredata/tdx@2026.9.3 tdx | not-checked
Runtime/checked at: <runtime identity and check time>
Campaign brief: <purpose, tone, workspace/template/name; no profile values>
Validation: passed | blocked <aggregate counts and reasons>
Next: setup-campaign
```

For the workshop send flow, invoke `setup-campaign` with the saved path, existing answers, recipient composition, and exact verified runner command as the next step without asking whether to continue. For CSV-only requests, invoke it only when the user requests continuation. If unavailable, provide a follow-up prompt. The campaign Skill must revalidate the saved file and reuse the verified runner command. Never hand off non-sendable recipients as sendable. No email is sent by this intake Skill itself.

## Examples

- “Create a workshop email with my name and send it to me.” Reuse supplied values; ask once in a regular message for only any missing required profile values; prepare one participant plus 30 approved test recipients; verify or prepare exact-version tdx; save a new approved CSV; then hand off for creation, preview, and the one final send confirmation.
- “Here are my email, first name, and last name; create the CSV.” Reuse all values, ask only for any missing required field, and save without a redundant approval. Stop after CSV preparation when that is the requested scope.
- “tdx reports 2026.9.3.” Verify in the actual campaign runtime; reuse the installed runner without package preparation.
