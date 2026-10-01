---
name: agenticworld-profile-csv-intake
description: Prepare a Agentic World workshop audience CSV by collecting participant information through free-text Question inputs and adding 30 fictional profiles with safe test recipients. Use for workshop self-send, sample audiences, profile CSV creation, or personalized workshop emails. Check existing tdx 2026.9.3 before campaign setup without reinstalling a correct runtime. Hand campaign creation and delivery to motion1-csv-list-campaign.
---

# Motion 1 — Make your workshop email personal

Use English for participant instructions, questions, previews, and completion messages. Keep technical settings backstage. Prepare the CSV and runtime check only; do not authenticate, query TD, create campaigns, or send emails here.

## Collect participant information with free-text questions

Reuse answers already supplied. Resolve the selected template's required personalization fields from the existing brief. Ask only for missing required values; omit unnecessary optional fields. There is no requirement to collect all fields together or in a single call.

Use the AI Studio `AskUserQuestion` / Question interface when available. Free-text values are intentionally collected through its **Other** input; do not reject this interface merely because email addresses and names require free text, and do not replace a supported Question interaction with a text-message form.

For each free-text question, show **Other only**, with no predefined answers. Use the tool's supported configuration: if Other is automatically supplied and an empty options list is valid, pass no predefined options; if Other must be explicit, supply only Other. Do not create placeholder choices such as "Enter my name", "Use a fictional name", "Skip", or "Preview only". Tell the participant: "Select Other and type your answer."

Follow the actual tool schema. Do not invent parameters, submit invalid calls, or require a tool by name when it is unavailable. If the interface cannot legally display Other alone, use an available native free-text Question field. If neither is supported, explain that limitation briefly and ask for the missing value in a short text question; do not claim the tool was used. This fallback is for an actual capability limitation, not a judgment that structured questions are unsuitable for free text.

Use these English prompts as needed:

| Field | Header | Question |
| --- | --- | --- |
| `email` | Email | What email address should we send your workshop email to? Select Other and type your email address. |
| `first_name` | First Name | What is your first name? Select Other and type your first name. |
| `last_name` | Last Name | What is your last name? Select Other and type your last name. |
| `company` | Company | What is your company name? Select Other and type your company name. |

Collect company only when required by the selected template. Apply the same Other-only pattern to any other required personalization value. Ask follow-ups only to resolve missing required values or ambiguities. Do not ask participants to choose types, merge-tag syntax, mappings, CLI flags, delivery providers, or test-recipient settings.

## Use the workshop send flow

The workshop flow prepares the audience, creates and previews the email, and sends it through `motion1-csv-list-campaign`. Sending is the established outcome. Do not ask for a delivery mode, offer preview-only or skip-send options, or introduce a separate self-send opt-in question. Treat the participant's request for this workshop flow and their supplied recipient address as authorization for the requested self-send, within its stated scope. Do not interpret CSV-only requests as authorization to send.

Keep participant-facing wording simple: "We'll use your details to personalize your workshop email and add 30 fictional profiles for the demonstration." Keep delivery infrastructure, SES, simulator addresses, quotas, and technical validation backstage. Do not ask marketers to approve or configure those details. This intake Skill prepares the CSV; the campaign Skill performs the actual send. Do not claim delivery until the campaign Skill confirms it.

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

If the delivery provider is unknown, resolve it with the operator once. For a non-SES path, use explicitly approved operator-controlled test inboxes or aliases, with receive capability verified for this workflow. Do not invent a universally deliverable address. Never silently omit synthetic recipients or stop a requested send flow after preview.

### Validate and write

Use UTF-8 and standard CSV quoting. Validate required values, email syntax, consistent field counts, unique email keys, required blanks, recipient classes, and row count. Preserve plus labels as part of each unique address. For the default workshop send flow require exactly one authorized participant address and 30 approved simulator/test addresses. Resolve failures rather than dropping rows.

Use existing approved key/blank policy and file/row/SQL limits. Downstream non-time fields are text; `time`, if present, is Unix seconds. Normally omit `time` so the helper can add ingest time. Do not promise unsupported numeric/date types, multiline cells, or large/batched processing.

Save a new file in the approved Work Folder. Preserve original files. Use a unique filename rather than overwrite. If the user has requested CSV creation and the destination and data handling are already approved, that request authorizes saving; do not ask for redundant save approval. Resolve an unknown, unauthorized, or over-shared destination before writing real profiles.

Show a masked summary: purpose, field names, data mode, participant/synthetic/total counts, new filename, destination, validation result, and whether recipients are sendable. For CSV-only requests, saving does not authorize delivery. For the workshop send flow, carry the existing send instruction into the campaign handoff without asking for a delivery-mode selection.

## Handoff to campaign creation

Tell the participant: "Your CSV is saved. Let's create the email and preview it." For CSV-only requests, report completion without initiating campaign setup.

Keep this handoff backstage and include no profile values or credentials:

```text
CSV file: <approved absolute path>
Collection/retention/destination approval: confirmed
Workshop send instruction: confirmed | CSV-only (no send requested)
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

For the workshop send flow, invoke `motion1-csv-list-campaign` with the saved path and existing answers as the next step without asking whether to continue. For CSV-only requests, invoke it only when the user requests continuation. If unavailable, provide a follow-up prompt. The campaign Skill must revalidate the saved file and reuse the verified runner. Do not claim the campaign Skill was updated by creating this Skill. If it enforces a conflicting one-recipient-only rule, report the conflict to the operator before campaign creation; do not silently shrink the audience or override it.

For the workshop send flow, continue through campaign creation, preview, and sending using the existing send instruction; do not add a delivery-mode question or redundant approval request. Honor any applicable mandatory approval in the campaign Skill, but keep participant-facing wording focused on the personalized email. Keep the full test-recipient composition in the internal handoff. Never hand off non-sendable recipients as sendable. No email is sent by this intake Skill itself.

## Examples

- "Create a workshop email with my name and send it to me." Reuse supplied values; collect missing personalization through Other-only Question inputs; generate 1 participant plus 30 approved test profiles; verify installed tdx when continuing; save a new approved CSV; hand off for creation, preview, and sending. Do not ask for delivery mode or explain delivery infrastructure to the participant.
- "Here are my email, first name, and last name; create the CSV." Reuse supplied values, ask only for missing required fields, and save without repeating an already authorized save step. Stop after CSV preparation when that is the requested scope.
- "tdx reports 2026.9.3." Verify in the actual campaign runtime unless this session already has a successful check for that same runtime; reuse the installed runner without package preparation.
