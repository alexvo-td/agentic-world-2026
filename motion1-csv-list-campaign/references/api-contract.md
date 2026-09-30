# Motion 1 — Operation contract and readiness ledger

Reference for the assistant and workshop operator. Keep CLI output and this ledger backstage. Unknown values block the affected operation. Do not record credentials, real profile rows, full addresses, or SQL containing CSV values

## Pinned runtime ownership

- Required package: `@treasuredata/tdx@2026.9.2`. CSV Intake owns initial download and cache verification
- Campaign commands reuse the same prepared runtime with `npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx`. Offline npm resolution prevents package download; tdx API requests still use the network
- Record runtime, version, and check time. Do not assume another runtime's cache or global binary is correct
- The 2026-09-30 baseline observed global `2026.9.0` and pinned `2026.9.2`, with version/help/local validation checks. That is not a live-send or participant-runtime verification
- A previous runtime emitted an `undici@8.11.2` Node `>=22.19.0` warning on Node `22.16.0`. Distinguish warnings from execution failure and verify the actual runtime again

Sources: [v2026.9.2 Engage docs](https://github.com/treasure-data/tdx/blob/v2026.9.2/docs/commands/engage.md), [PR #3321](https://github.com/treasure-data/tdx/pull/3321)

## ListCampaign operations

Always use `--campaign-type list-campaign` and the verified explicit `--workspace`

| Operation | Effect | Approval |
|---|---|---|
| `campaign validate <yaml>` | Local schema validation only | No persistent-write approval |
| `campaign push <yaml> --dry-run` | Read template/existing resources; plan create/update; no write | No persistent-write approval |
| `campaign push <yaml>` | Create DRAFT if absent; update matching DRAFT only | Separate DRAFT-save approval |
| `campaign show <ID> --full` | Read persisted JSON:API resource | Read-only |
| `campaign list` | List workspace ListCampaigns | Read-only |
| `campaign launch <ID> --dry-run` | Read resource and show source database/table; no launch API | No delivery approval |
| `campaign launch <ID>` | Start delivery from the contact-list table; irreversible | Exact-message/scope review and final send approval |

Neither dry-run counts eligible recipients, renders the message, nor proves consent/suppression. Verify these separately. Capture the ID returned by the approved create/read-back and reuse it through preview, launch, and status confirmation. Never guess the newest campaign

Stop on same-name non-DRAFT or ambiguous matches. Do not invent ListCampaign-specific `pull` or `campaign status` commands; use `show/list`

### Non-interactive execution

Verified against [v2026.9.2 launch code](https://github.com/treasure-data/tdx/blob/v2026.9.2/src/commands/engage-command.ts#L522-L601) and [prompt code](https://github.com/treasure-data/tdx/blob/v2026.9.2/src/utils/prompt.ts)

- TTY stdin normally receives a CLI confirmation prompt
- Non-TTY stdin without `--yes` stops with `Confirmation required but running in non-interactive mode`
- In AI Studio, supply final CLI `--yes` **only after** the relevant human DRAFT-save or final send approval
- This flag handles the CLI's prompt, not human authorization, application live approval, or access controls
- Never launch before final approval. If runtime execution is denied, do not bypass it with raw API, stdin yes injection, a fake TTY, or permission changes
- Do not generalize these ListCampaign CLI instructions to workflow-run or journey-resume approval rules

```bash
# Read-only; always run before launch review
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign launch "<reviewed-ID>" --campaign-type list-campaign --workspace "<workspace>" --dry-run
# Non-interactive launch only after final approval and unchanged-scope checks
npx --offline --yes --package=@treasuredata/tdx@2026.9.2 tdx engage campaign launch "<reviewed-ID>" --campaign-type list-campaign --workspace "<workspace>" --yes
```

## Data and YAML contract

| Field | Requirement |
|---|---|
| `type` | `list_campaign` |
| `contact_list` | Existing `database_name`/`table_name`; not direct CSV upload |
| `source_columns` | Verified physical column/key/type mapping |
| email | `key: email`, `sql_name: email`, `type: string` |
| template | `email.template: ref:<existing-template>` |
| HTML | `email.html_file` in the YAML folder; optional plaintext |
| sender | `email.sender_id`, not the standard connector field |
| workspace | Explicit CLI flag; no CDP audience/segment blocks |
| paths | No companion-file traversal or symlink escape |

Sources: [schema](https://github.com/treasure-data/tdx/blob/v2026.9.2/src/sdk/engage/list-campaign-schema.ts), [YAML loader](https://github.com/treasure-data/tdx/blob/v2026.9.2/src/sdk/engage/list-campaign-yaml.ts)

## Per-run readiness ledger

The operator confirms the following in the actual environment. Reuse already approved settings; do not invent limits or retention policies

| Item | Record |
|---|---|
| Runtime | Site/account/profile, tdx version, runtime/check time |
| Resources | Actual Agentic World Workspace, template/sender names and IDs, permissions |
| Data mode | Synthetic / participant-self / owner-approved-real |
| Exposure approvals | Chat, Work Folder, and query/job history checked separately |
| CSV | Approved path, schema, count, key, blank/time policy, validation |
| Limits | File bytes, row count, SQL bytes; default self-send cap one |
| Table | New run-only `agentic_world_demo.sample_id_<32-lowercase-hex>` |
| Recipient | Private participant match, opt-in, consent/suppression basis |
| Content | Source/hash, preview type, personalization, sender, CTA, unsubscribe, address, asset access |
| Cleanup | Owner and handling policy for private SQL files |

The helper only prepares SQL. Non-time columns are VARCHAR; time is BIGINT. INSERT appends, so no blind retry. Real values may remain in query/job history. Read back counts, keys, and the exact source match. Nonzero `ignored_blank_rows` requires an explicit source correction/exclusion decision

## Approval record

| Action | Exact scope | Approver/time | Result/evidence |
|---|---|---|---|
| CSV save | New Work Folder path, fields/count |  |  |
| CREATE SCHEMA | Only if needed; new database |  |  |
| CREATE TABLE | New run-only table/schema |  |  |
| INSERT | Count and query-history exposure |  |  |
| DRAFT push | Workspace/campaign, mapping, sender, content |  |  |
| Live launch | ID/version, content hash, row-set fingerprint, one participant, send now |  |  |

Send approval applies only to the displayed target and content. A change to campaign version, sender, mappings, CSV, or table invalidates it—even if the count is unchanged. Re-preview and re-approve. Do not treat a shared/mutable table as a fixed launch source

## Recipient snapshot and write exclusion

A last-minute comparison alone cannot prevent a change between comparison and launch. Establish and record these checks before enabling live delivery

1. Create a table dedicated to this run and insert the approved CSV once. No reused, appended, or periodically updated source
2. Freeze writes after INSERT verification through launch processing completion. Exclude other users, service accounts, workflows, imports, and processes sharing credentials, using verified permissions and operating controls
3. Compare mapped CSV/table columns as a canonical row set with fixed schema ordering, row ordering, and NULL/blank rules. Record any approved exclusion of ingest-time fields
4. Use a run-private HMAC-SHA256 key or equivalent for the row-set fingerprint. Keep key/comparison data private; do not treat an unsalted email hash as anonymous data
5. Bind fingerprint, row count, content hash, table, and write-exclusion owner/time to approval. Recheck after approval and detect substituted recipients even with the same count
6. Do not release the freeze while asynchronous launch completion is unknown. Stop if change prevention cannot be established

Do not assume undocumented TD table-lock, snapshot, or transactional-launch APIs exist. A new name and hash are not write-exclusion proof. If the operator cannot establish isolation, stop at DRAFT/preview and explain the missing check

## Status and verification limits

- Documented states: DRAFT, PLANNED, ACTIVE, SUSPENDED, FINISHED. [Type definition](https://github.com/treasure-data/tdx/blob/v2026.9.2/src/sdk/types/engage.ts#L299)
- ACTIVE/FINISHED is not proof of inbox delivery. Compare launch response with read-back of the exact same ID
- ListCampaign support in `preview_engage_campaign`, `campaign readiness`, and actual sender/merge-tag/unsubscribe rendering must be verified in the target environment
- Timeouts/unclear responses require state inspection, not blind re-launch
- Northstar mock content stays non-sendable until replaced by approved real-send content
- Performance reporting is deferred. This version does not run delivery/open/click KPI queries or promise engagement metrics

💎 Generated with [Treasure Work](https://github.com/treasure-work)
