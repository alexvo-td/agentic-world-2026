# Technical execution and recovery

## Session isolation and startup

SKILL.md Fresh-session start controls sequencing: intake and local audience preparation precede runtime/service discovery. All reads in this reference are stage-specific authorization, not an instruction to preload discovery on invocation. Use only current-invocation explicit inputs, exact session host bindings and current-run artifacts. Do not scan current/shared/general directories, list old campaigns, read another run's state/CSV or update the skill repository to reconstruct setup. Missing handoff/config is not evidence that another folder should be searched. Host preflight happens before the participant session.

## Host prerequisites

Use host-provided TAIS shared-workfolder capabilities, participant workfolder context, authenticated TD region/account, an Engage workspace and verified sender. Host configuration must supply collection URL and optionally test inboxes/product catalog IDs. Resolve verified readiness/status/reporting bindings under service-bindings.md; placeholders in service_bindings are not usable configuration. The bundled JSON contains null placeholders intentionally. Do not expose secrets in chat, CSVs, process logs or readiness state.

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

Read-only `tdx` discovery is authorized across all namespaces needed for the workshop, including delivery sender commands. `--help` is a local inspection, not a business approval point. At service preparation, run the needed discovery when supported; do not run it as startup work:

```bash
tdx delivery senders --output json
tdx engage campaign push --help
```

Use `tdx delivery senders` for sender listing. Never infer that sender listing belongs to the Engage namespace. Do not append `--workspace` to delivery commands unless their installed help explicitly supports it; verify workspace association separately from actual workspace configuration/readiness. Check `tdx delivery --help` or the relevant command help automatically if sender syntax is uncertain. Run these only when service preparation needs them; do not delay identity intake or local audience analysis for discovery. Do not print a permission question or invoke a choice tool for these commands. The supplied Engage reference does not establish delivery sender flags; use installed help to verify them. Do not extend discovery permission into unrelated destructive commands.

## Read-only discovery without conversational approval

The campaign-preparation request authorizes the reads needed to prepare it. At the relevant service stage, execute needed workspace/sender/template discovery, CLI checks and exact current-run/explicitly-targeted campaign reads automatically. Do not list campaigns to locate previous sessions, and do not run this discovery before the initial intake/local audience work. Do not ask for permission because a command accesses a service, because configuration is unknown, or because the operation is read-only. Unknown configuration is a reason to inspect it, not a reason to request approval.

At the service-operation stage, use these direct discovery commands only when explicit session configuration cannot resolve the needed workspace/sender and installed help supports their syntax:

```bash
tdx engage workspaces --output json
tdx delivery senders
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

Explicit continuation, copy/choice revision, launch, status polling or technical retry for the current run may use its already-known exact state path. A new skill invocation starts a fresh run unless continuation/reuse is explicit; never load state by searching previous folders. Load that current/explicitly-targeted run's state and fetch its object status before retrying an ambiguous mutation. Reconcile only objects created by that run, so retries cannot create duplicates. After a successful or uncertain launch, never automatically resend or create a replacement; report pending state and poll boundedly. A separate explicit new-campaign request creates fresh objects but still requires its own preview and Launch action.

## Launch gates

Require completed import; at least one actual business delivery destination in Plot-twist; a nonempty eligible business cohort and nonzero verified additional reach when baseline is known; a nonempty delivery audience; the explicitly authorized participant destination exactly once (independent identity-only QA in Plot-twist, or eligible fictional business participant in standalone mode); exact eligible row count and unique destination count; verified SES route for success simulator sample recipients, preserving documented plus labels; verified service deduplication behavior; no placeholder or denied recipients (QA cannot bypass genuine DENIED); supported profile merge tags; saved HTML and subject; verified sender; verified table/source mappings and YAML companion paths; authorized assets and established offer; configured HTTPS CTA; unsubscribe system tag; evidence for each validation gate under tdx-commands.md, including a verified service-side launch readiness binding and independent checks outside its documented coverage; displayed four-section completed campaign review report with current fingerprint; explicit approval to launch that report version. Persist launch intent before calling launch. A changed offer/audience/sender/content/QA recipient requires a fresh preview and launch instruction.

Read delivery status through the verified status binding and bounded polling under service-bindings.md. Submission is not delivery, delivery is not inbox placement. Summarize bounces/errors from actual reporting. Technical problems go to host-facing remediation without requesting repeated participant approval.

For Plot-twist operation scope, follow plot-twist.md. Inherited discovery decisions do not authorize modifying its campaign object. Distinguish an additional-list one-off from an explicit existing-draft update; preserve original snapshots and report exact-email deduplication limits. Keep inherited decision versions, business/QA artifacts, impact-report version, reporting_requested and journey-handoff path in private state.
