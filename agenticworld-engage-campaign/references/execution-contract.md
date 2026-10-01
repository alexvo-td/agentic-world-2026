# Technical execution and recovery

## Host prerequisites

Use host-provided TAIS shared-workfolder capabilities, participant workfolder context, authenticated TD region/account, an Engage workspace and verified sender. Host configuration must supply collection URL and optionally test inboxes/product catalog IDs. The bundled JSON contains null placeholders intentionally. Do not expose secrets in chat, CSVs, process logs or readiness state.

The official Engage command workflow is summarized in [tdx-commands.md](tdx-commands.md). The user supplied a CSV List campaign YAML specification in [campaign-yaml.md](campaign-yaml.md) and `assets/list-campaign.example.yaml`, with documented validate/push/launch syntax in that reference. Use that documented CLI workflow rather than inventing endpoints. Before a service mutation inspect authenticated installed CLI help, host runbook or authoritative service contract for the current account. If available, reuse the motion1-csv-list-campaign technical reference after reading it; this skill's conversation contract supersedes intermediate approval questions. Never require that sibling skill to exist silently.

## Runtime

Check installed `tdx --version` once. Treat `2026.9.3` as the minimum supported version, not an exact pin. Compare numeric semantic-version components, not lexical strings (for example, 2026.10.0 is newer than 2026.9.3).

- If installed version is 2026.9.3 or newer, reuse the global `tdx` without installation or upgrade.
- If installed version is older, or `tdx` is missing, run `npm install -g @treasuredata/tdx` to install the latest release. Do not add an explicit version suffix and do not substitute a pinned npx runner.
- After installation, run `tdx --version` again and verify it meets the minimum. Use this verified global command for subsequent operations.
- If version output is unparseable, diagnose the installed command before deciding to upgrade; do not assume it is old. For prereleases, use semantic-version ordering against the stable minimum.

Check actual Node/package compatibility, global npm write access and network availability. Do not repeatedly install a runtime that already meets the minimum. If preparation fails or the resulting version is below the minimum, preserve artifacts and tell the host the dependency that failed without asking the marketer to operate a CLI. Record the observed version; check its actual command contract before service mutations.

## Direct CLI invocation

Run all version, help, authentication, audience, campaign, validation, launch and status commands directly as `tdx ...`. Do not prepend `npx`, `--package`, or a version-pinned runner. When reusing commands from another skill or runbook, retain the documented subcommand and arguments but replace its runtime wrapper with `tdx`. If global installation succeeds but `tdx` is not found, diagnose the npm global binary directory and PATH; do not silently fall back to npx.

## Cross-namespace read authorization

Read-only `tdx` discovery is authorized across all namespaces needed for the workshop, including delivery sender commands. `--help` is a local inspection, not a business approval point. Run the reported discovery immediately when supported:

```bash
tdx delivery senders --output json
tdx engage campaign push --help
```

Check `tdx delivery --help` or the relevant command help automatically if sender syntax is uncertain. Do not print a permission question or invoke a choice tool for these commands. The supplied Engage reference does not establish delivery sender flags; use installed help to verify them. Do not extend discovery permission into unrelated destructive commands.

## Read-only discovery without conversational approval

The campaign-preparation request authorizes the reads needed to prepare it. Execute workspace, sender and campaign listing/details, CLI help/version, authenticated configuration reads and status checks immediately. Do not ask for permission because a command accesses a service, because configuration is unknown, or because the operation is read-only. Unknown configuration is a reason to inspect it, not a reason to request approval.

For the reported discovery sequence, use the following direct commands when their syntax is supported by installed CLI help:

```bash
tdx engage workspaces --output json
tdx engage senders
tdx engage campaigns
```

Inspect help automatically and adjust arguments if the installed CLI requires them. Do not print these commands as a proposed action awaiting approval. Participant-facing progress example: “I'm checking the Engage workspace and sender settings.” Then execute and continue preparation.

Use sibling skills and host runbooks for technical command contracts only. Do not inherit their conversational approval prompts, query-history consent steps or npx wrappers. This applies even when they recommend approval before list/show/get operations. Preserve the final participant Launch action after preview. Platform-enforced tool approvals remain outside this skill's control; do not claim they can be disabled here or convert ordinary discovery into a voluntary approval request.

## Verified API binding

Before create/import/update/validate/launch, bind each operation to a documented command and response shape. Record non-secret command contract, relevant object ID and status. Require explicit support for CSV List one-off audience; never silently substitute a parent segment. Confirm the recipient table has a physical `email` column and the mandatory `source_columns` entry uses `key: email`, `sql_name: email`, `type: string`, automatic inclusion of all columns, profile namespace availability, content fields, sender configuration, validation and launch semantics. If unsupported or undocumented, complete local preparation and report that live execution is blocked.

Use authenticated context; do not put credentials in files. Fetch actual workspace/sender configuration, enforce the requested account/region. Do not guess sender addresses. Carry all CSV fields through import. Use the user-specified `tdx query` Trino INSERT INTO workflow in csv-upload.md for recipient CSV ingestion. Perform authorized workshop writes without a redundant query-history consent question, while respecting higher-priority database restrictions.

## State and idempotency

Persist a separate non-secret campaign-state.json in each personal run folder: run ID, creation mode, explicit reuse scope if any, recipient table/audience ID, account/region, workspace ID, campaign ID, audience import/job IDs, content/audience hashes, sender ID, validation status, preview fingerprint, launch intent and operation status. Never include credentials, full SQL or unnecessary profile rows.

For every new campaign-preparation request, allocate a unique run ID and create a new campaign and a new audience/recipient table. Do not reuse an earlier campaign/table because its name, participant email, content hash or latest state matches. Reuse is allowed only when explicitly requested, and separately for each object: “reuse this audience” still means create a new campaign; “update this campaign” does not authorize reuse of an old audience unless specified. Resolve explicit reuse targets from IDs or unambiguous workspace ownership; do not guess.

Create an immutable per-run audience snapshot/import artifact and unique recipient-table name (for example an identifier-safe participant slug plus UTC timestamp and random suffix). Use a unique campaign name suffix when no exact name was requested. Preserve an explicitly requested name when duplicate names are supported; if uniqueness prevents it, explain the collision and ask for a business naming choice. Never overwrite an old campaign/table to avoid a collision. Do not modify or delete prior runs. Reuse source template, workspace, sender and explicitly supplied identity as inputs; copy the reusable profile dataset into a new run snapshot rather than sharing mutable campaign audience state.

Continuing a conversation, correcting copy, changing a choice, polling status or retrying a failed command belongs to the same run unless the participant requests a new campaign. Load that run's state and fetch its object status before retrying an ambiguous mutation. Reconcile only objects created by that run, so retries cannot create duplicates. After a successful or uncertain launch, never automatically resend or create a replacement; report pending state and poll boundedly. A separate explicit new-campaign request creates fresh objects but still requires its own preview and Launch action.

## Launch gates

Require completed import; eligible participant included exactly once; exact eligible row count and unique destination count; verified SES route for success simulator sample recipients, preserving documented plus labels; verified service deduplication behavior; no placeholder or denied recipients; supported profile merge tags; saved HTML and subject; verified sender; verified table/source mappings and YAML companion paths; authorized assets and established offer; configured HTTPS CTA; unsubscribe system tag; successful service validation; displayed current fingerprint; explicit launch instruction after preview. Persist launch intent before calling launch. A changed offer/audience/sender/content requires a fresh preview and launch instruction.

Read delivery status through supported APIs. Submission is not delivery, delivery is not inbox placement. Summarize bounces/errors from actual reporting. Technical problems go to host-facing remediation without requesting repeated participant approval.
