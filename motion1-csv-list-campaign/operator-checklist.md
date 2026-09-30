# Motion 1 — Workshop operator checklist

Participant journey: **profile → create email → preview → approve and send → confirm launch status**. Keep technical details backstage and all participant-facing content in English

## Before the workshop

- [ ] Approve purpose, chat collection/retention, Work Folder access, TD query/job-history exposure, and cleanup ownership
- [ ] Verify actual site/account/profile, Agentic World Workspace, template, sender, and permissions without collecting credentials in chat
- [ ] CSV Intake prepares tdx `2026.9.2` and verifies the offline runner in the same runtime
- [ ] Configure file/row/SQL limits. Default live self-send cap: one participant-owned address
- [ ] Verify the real-send template's personalization, sender, CTA, postal address, unsubscribe, and image access
- [ ] Keep `example.test` addresses and Northstar mock content out of live sends

## Prepare the recipient list

- [ ] Accept a saved CSV and non-PII handoff; verify participant opt-in and approved destination
- [ ] Revalidate actual headers, key, count, blank/time policy, and limits
- [ ] Obtain an explicit source correction/exclusion decision for errors or nonzero `ignored_blank_rows`
- [ ] Preserve the original sample and create a new participant-only version
- [ ] Use a new run-only table; never append to or overwrite an existing/shared table
- [ ] Obtain separate approvals for CREATE SCHEMA if needed, CREATE TABLE, and INSERT
- [ ] Confirm query/job-history exposure separately from CSV-save approval
- [ ] Read back job, schema, count, and unique key after writes. Do not retry INSERT blindly

## Build and preview the campaign

- [ ] Reuse supplied workspace/name/template/CSV and ask only for missing choices
- [ ] Map email and personalization fields from actual table schema
- [ ] Create YAML and HTML together; do not reuse standard campaign audience/segment/connector settings or unsupported tokens
- [ ] Local validation and push dry-run pass; stop for non-DRAFT/ambiguous matches or unexpected updates
- [ ] Obtain DRAFT-save approval before push. For non-TTY CLI execution, use `--yes` only afterward
- [ ] Capture the exact generated campaign ID and carry it through every subsequent operation; do not select latest or make participants reselect
- [ ] Compare persisted table/mapping/template/sender/content through `show --full`
- [ ] Present a supported ListCampaign preview or accurately labeled static content preview. Never call local token replacement a live Engage render
- [ ] Verify required personalization/blank behavior, sender, unsubscribe, address, CTA, and image access before delivery

## Final approval

- [ ] Always run launch dry-run first; it is source-reference validation, not content or recipient-count preview
- [ ] Separately verify the complete table, unique email, exact CSV match, consent/suppression basis, and participant-owned one-row cap
- [ ] Freeze the run-only table after INSERT through launch completion; exclude other writers, workflows, imports, and processes sharing credentials
- [ ] Record the private canonical row-set fingerprint and write-exclusion owner/time. A unique name and last-minute comparison alone are not a freeze guarantee
- [ ] Show campaign/workspace, sender, subject/body preview, recipient count, and “send now” scope
- [ ] Confirm full address only in an allowed private review; never put it in shared artifacts or logs
- [ ] Bind preview-linked final approval to exact ID/version, content, sender, and recipient snapshot. Do not reuse general workshop or save approval
- [ ] Recheck after approval. Changes invalidate approval and require a new preview. Stop if scope cannot be fixed or verified

## Launch and status read-back

- [ ] Once checks and final approval pass, the Skill launches that exact ID once without ritual repeated approval
- [ ] In non-TTY AI Studio execution, append CLI `--yes` only after final approval; respect application approval and permissions
- [ ] Do not bypass runtime denial with raw API, fake TTY, stdin yes injection, or permission changes
- [ ] Do not schedule, expand recipients, or substitute campaigns
- [ ] For timeout/unclear outcome, inspect the same ID before any retry; no blind re-launch
- [ ] Record launch response and `show/list` state. ACTIVE/FINISHED is not proof of inbox delivery
- [ ] Invite the participant to check their inbox without inventing arrival or engagement metrics

## Completion

- [ ] Record non-PII version, CSV path/fields/count, workspace/table, exact campaign ID/version, preview type, approvals, and observed launch state
- [ ] Track CSV save, table setup, DRAFT save, final approval, and launch as separate outcomes
- [ ] Keep credentials, full addresses, real rows, and INSERT text out of shared records
- [ ] Record open issues with owner, action, due date, status, and completion criteria
- [ ] Do not add performance reporting or delivery/open/click KPI queries; this feature is deferred

💎 Generated with [Treasure Work](https://github.com/treasure-work)
