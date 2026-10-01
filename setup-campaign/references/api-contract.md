# Operation contract and readiness ledger

Keep technical details backstage. Require tdx exactly `2026.9.3`; use the verified command handed off by `agenticworld-profile-csv-intake`. If the installed command was missing or mismatched, intake prepares and verifies `npx --yes --package=@treasuredata/tdx@2026.9.3 tdx`; use that exact invocation for every campaign command. Do not add `--offline`, substitute a version, or silently reconstruct the runner. Record actual command/runtime/version once.

## Story and delivery scope

Use Northstar Home & Living's established re-engagement objective without asking the participant to restate it. Record the story's business audience separately from the actual workshop recipients. The CSV does not prove overdue-purchase eligibility or real behavioral segmentation. The fictional Northstar brand is eligible for a workshop send when all content and delivery settings are verified; fictional branding alone is not a blocker. Any unverified benchmark/mock content or assets are draft-only until claims, CTA, images, postal address, sender and unsubscribe behavior are resolved. Final confirmation covers the exact workshop recipients and preview, not Northstar's real customers.

The default workshop send list has one participant-provided address plus 30 approved test-recipient addresses (31 total). Those approved test destinations are part of the actual send target and must not be silently removed or described as preview-only. Use SES simulator addresses only when the SES delivery path is confirmed; otherwise use approved operator-controlled test destinations verified for this workflow. `example.test` fixtures are preview-only and never sendable.

## Operation authorization

A campaign setup request authorizes local validation, reads, dry-runs, a unique recipient table, loading the reviewed CSV, and saving the intended new DRAFT within the already approved account/workspace/data-handling scope. Do not add per-command, CREATE TABLE, INSERT, CSV-save, or DRAFT-save conversational approvals. Resolve actual policy or scope gaps with the operator once. Missing schema provisioning must be within operator setup scope. Never overwrite shared resources or alter permissions incidentally.

Use `--campaign-type list-campaign` and explicit verified `--workspace` for workspace-scoped commands. validate and push `--dry-run` do not save; push `--yes` saves the intended DRAFT. `show <ID> --full` and list inspect persisted resources. launch `--dry-run` checks references, not recipient eligibility or rendering. launch `--yes` sends only after one fresh final confirmation bound to the exact preview and recipient set. These flags handle CLI prompts, not runtime permissions. Never evade denial or blindly retry writes.

## Data contract

YAML type is `list_campaign`. `contact_list` supplies `database_name`/`table_name`. `source_columns` maps actual columns with `key`/`sql_name`/`type`; email uses `email`/`email`/`string`. `email.template` references an existing template; `email.html_file` is a companion file; `email.sender_id` identifies the verified sender. Prevent traversal and symlink escapes. Do not use standard campaign audience/segment/connector configuration. Attribute tokens use `{{ profile.first_name }}` (and `{{ profile.<attribute_name> }}`); mapping keys remain unprefixed, such as `first_name`.

## Per-run ledger

Record account/workspace, exact runner command/runtime/version, template/sender IDs, CSV path/schema/count/key, blank/time policy, established file/row/SQL/live-recipient limits, unique table, authorized participant/test-recipient composition, consent/suppression basis, content hash/preview type, isolation controls, and cleanup owner. Do not record profile values, credentials, full addresses, or INSERT text in shared records. Track setup as execution evidence rather than separate approval gates. Bind the single final send confirmation to exact ID/version, content, sender, mappings, row-set fingerprint, recipient composition/count, timing, and response/time.

## Recipient snapshot and write exclusion

Create a run-specific table and load the reviewed CSV once. Establish existing verified operating controls excluding other users, service accounts, workflows, imports, and shared-credential processes from writing after verification through source processing completion. Compare the full reviewed CSV/table as a canonical row set with fixed ordering and NULL/blank rules; record any excluded ingest-time columns. Use a private HMAC-SHA256 key or equivalent; keep key and rows private. Bind fingerprint/count/table/content to send confirmation and recheck before launch, including same-count substitutions. A new name/hash alone is not isolation proof. Do not assume undocumented locks or snapshot APIs. If isolation is unavailable, complete DRAFT/preview and pause delivery for operator resolution. Maintain exclusion while completion is unknown.

## Verification limits

Capture the exact campaign ID and reuse it; do not select newest. Stop on ambiguous or unrelated/non-DRAFT matches. Re-preview and reconfirm material changes to the reviewed send. Do not silently reduce or expand the authorized audience. `example.test` addresses and unresolved benchmark/sample content are draft-only. Inspect uncertain launch state before retrying. Do not invent campaign status/pull commands. ACTIVE/FINISHED does not prove inbox delivery. Exclude performance reporting.

Technical baseline references: https://github.com/treasure-data/tdx/blob/v2026.9.3/docs/commands/engage.md and https://github.com/treasure-data/tdx/blob/v2026.9.3/src/sdk/engage/list-campaign-schema.ts . Check installed help and supported behavior if the exact pinned version differs from this documented contract.
