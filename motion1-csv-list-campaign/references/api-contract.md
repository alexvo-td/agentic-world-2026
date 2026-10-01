# Operation contract and readiness ledger

Keep technical details backstage. Accept tdx >=2026.9.2; reuse a verified compatible installed runner. If preparation is required, use workshop version 2026.9.3 through intake/operator setup. Do not reinstall a compatible runner. Record actual runner/version/runtime once.

## Story and delivery scope

Use Northstar Home & Living's established re-engagement objective without asking the participant to restate it. Record the business audience separately from the actual workshop delivery list. The CSV does not prove overdue-purchase eligibility or real behavioral segmentation. Authorized fictional branding is sendable once all content and delivery settings are verified; unresolved placeholders remain draft-only. Final confirmation covers the workshop recipients and exact preview, not Northstar's real customers.

## Operation authorization

Campaign setup authorizes local validation, reads, dry-runs, a unique recipient table, loading the reviewed CSV, and saving the intended new DRAFT. Do not add per-command, CREATE TABLE, INSERT, or DRAFT-save approval. Apply established data handling and retention policies; resolve actual policy gaps with the operator. Missing schema provisioning must be within operator setup scope. Never overwrite shared resources or alter permissions incidentally.

Use --campaign-type list-campaign and explicit verified --workspace for workspace-scoped commands. validate and push --dry-run do not save; push --yes saves the intended DRAFT. show <ID> --full and list inspect persisted resources. launch --dry-run checks references, not recipient eligibility or rendering. launch --yes sends only after exact preview-linked final confirmation. These flags handle CLI prompts, not runtime permissions. Never evade denial or blindly retry writes.

## Data contract

YAML type is list_campaign. contact_list supplies database_name/table_name. source_columns maps actual columns with key/sql_name/type; email uses email/email/string. email.template references an existing template; email.html_file is a companion file; email.sender_id identifies the verified sender. Prevent traversal and symlink escapes. Do not use standard campaign audience/segment/connector configuration. Attribute tokens use {{ profile.first_name }}; mapping keys remain first_name.

## Per-run ledger

Record account/workspace, runner/runtime/version, template/sender IDs, CSV path/schema/count/key, blank/time policy, established file/row/SQL/live-recipient limits, unique table, authorized participant/test-recipient composition, consent/suppression basis, content hash/preview type, isolation controls, and cleanup owner. Do not record profile values, credentials, full addresses, or INSERT text in shared records. Track setup as execution evidence rather than separate approval gates. Bind the single final send confirmation to exact ID/version, content, sender, mappings, row-set fingerprint, recipients, timing, and response/time.

## Recipient snapshot and write exclusion

Create a run-specific table and load the reviewed CSV once. Establish existing verified operating controls excluding other users, service accounts, workflows, imports, and shared-credential processes from writing after verification through source processing completion. Compare the mapped CSV/table as a canonical row set with fixed ordering and NULL/blank rules; record any excluded ingest-time columns. Use a private HMAC-SHA256 key or equivalent; keep key and rows private. Bind fingerprint/count/table/content to send confirmation and recheck before launch, including same-count substitutions. A new name/hash alone is not isolation proof. Do not assume undocumented locks or snapshot APIs. If isolation is unavailable, complete DRAFT/preview and pause delivery for operator resolution. Maintain exclusion while completion is unknown.

## Verification limits

Capture the exact campaign ID and reuse it; do not select newest. Stop on ambiguous or unrelated/non-DRAFT matches. Re-preview and reconfirm material changes to the reviewed send. Do not silently reduce or expand the authorized audience. Draft-only addresses cannot be delivered. Inspect uncertain launch state before retrying. show/list are inspection operations; do not invent campaign status/pull commands. ACTIVE/FINISHED does not prove inbox delivery. Exclude performance reporting.

Technical baseline references: https://github.com/treasure-data/tdx/blob/v2026.9.2/docs/commands/engage.md and https://github.com/treasure-data/tdx/blob/v2026.9.2/src/sdk/engage/list-campaign-schema.ts . Check installed help and supported behavior if a later version differs.
