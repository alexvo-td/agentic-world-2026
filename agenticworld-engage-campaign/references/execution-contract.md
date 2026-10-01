# Technical execution and recovery

## Host prerequisites

Use host-provided TAIS shared-workfolder capabilities, participant workfolder context, authenticated TD region/account, an Engage workspace and verified sender. Host configuration must supply collection URL and optionally test inboxes/product catalog IDs. The bundled JSON contains null placeholders intentionally. Do not expose secrets in chat, CSVs, process logs or readiness state.

The user supplied no CSV List API specification in this package. This skill specifies orchestration, not an invented endpoint implementation. Before a service mutation inspect authenticated installed CLI help, host runbook or authoritative service contract for the current account. If available, reuse the motion1-csv-list-campaign technical reference after reading it; this skill's conversation contract supersedes intermediate approval questions. Never require that sibling skill to exist silently.

## Runtime

Check installed `tdx --version` once. If exact 2026.9.3, reuse it without npm installation. Otherwise prepare `npx --yes --package=@treasuredata/tdx@2026.9.3 tdx --version` and verify exact version; reuse this runner for subsequent commands. Check actual Node/package compatibility and network availability. Do not stop merely because the globally installed tdx has another version. Do not repeatedly download a correct runtime. If preparation fails, preserve artifacts and tell the host the dependency that failed without asking the marketer to operate a CLI.

## Verified API binding

Before create/import/update/validate/launch, bind each operation to a documented command and response shape. Record non-secret command contract, relevant object ID and status. Require explicit support for CSV List one-off audience; never silently substitute a parent segment. Confirm email_address routing, automatic inclusion of all columns, profile namespace availability, content fields, sender configuration, validation and launch semantics. If unsupported or undocumented, complete local preparation and report that live execution is blocked.

Use authenticated context; do not put credentials in files. Fetch actual workspace/sender configuration, enforce the requested account/region. Do not guess sender addresses. Carry all CSV fields through import. Do not use SQL INSERT unless the verified contract needs it; if necessary perform authorized data operations without a redundant query-history consent question.

## State and idempotency

Persist a non-secret campaign-state.json in the personal Workfolder: account/region, workspace ID, campaign ID, audience import/job IDs, content/audience hashes, sender ID, validation status, preview fingerprint, launch intent and operation status. Never include credentials, full SQL or unnecessary profile rows.

On rerun load state, fetch object status and reuse/update a draft. Detect duplicate names in the intended workspace; resolve by state/ownership, not the name alone. Before ambiguous mutation retries fetch existing state. After a successful or uncertain launch never create or send a replacement automatically. Report pending state and poll boundedly.

## Launch gates

Require completed import; eligible participant included exactly once; exact eligible count; no placeholder or denied recipients; supported profile merge tags; saved HTML and subject; verified sender; configured HTTPS CTA; unsubscribe system tag; successful service validation; displayed current fingerprint; explicit launch instruction after preview. Persist launch intent before calling launch. A changed offer/audience/sender/content requires a fresh preview and launch instruction.

Read delivery status through supported APIs. Submission is not delivery, delivery is not inbox placement. Summarize bounces/errors from actual reporting. Technical problems go to host-facing remediation without requesting repeated participant approval.
