# Verified service bindings

Read this before launch readiness checks, status polling or performance queries. The host configuration may provide the bindings below; these are skill configuration fields, not an assertion that an API exposes them. Null placeholders are unresolved prerequisites. Confirm each binding against installed help, an authoritative service contract or a current host runbook. Record its source/version and observation time privately; do not invent endpoints, response paths or status names.

## Validation evidence

Keep these results separate in campaign state and the launch review:

| Gate | Required evidence |
|---|---|
| Local validation | Successful YAML/content/schema checks and `tdx engage campaign validate`; proves local validity only |
| Reference resolution | Successful push dry-run resolving the intended workspace, template and sender; proves neither delivery nor complete readiness |
| Saved configuration | Read back the pushed campaign and TD source table; confirm reviewed subject, content, mappings, counts, sender and settings |
| Service readiness | Verified launch dry-run/readiness operation, its response paths and passing checks; list its documented coverage and independently verify remaining launch gates |

Use the documented launch dry-run under tdx-commands.md only after confirming its installed semantics. Do not treat a zero exit code or local validation as proof of checks outside its documented coverage. If no verified service readiness binding is available, preserve the draft and show the missing host prerequisite; do not mark Ready to launch.

## Status binding and bounded polling

Resolve `service_bindings.status` with: documented read operation, campaign-ID/workspace argument binding, response field path for state, and explicit service-state sets for processing, completed, partially_failed and failed. Include count/error paths only when documented. Persist actual raw status and its normalized interpretation. A campaign show command is a status source only if its documented response exposes the required delivery-processing state; draft/configuration state alone is insufficient.

Bind the status operation to the launched campaign and launch operation ID when available. Persist launch intent before launch and persist the returned operation ID/status immediately afterward. On uncertain launch results, use that binding to reconcile; never issue a second launch automatically. Unknown status stays unknown, not completed.

Poll at most five reads over approximately one minute per interaction; honor provider rate limits and stop earlier on a terminal state. After the bound, show pending/unknown and retain state for the next requested check; do not run an endless loop. Completed means send processing has reached a documented terminal state, not that all recipients have Delivery events or inbox placement. Partially failed is terminal with failures disclosed. Failed is a failed send attempt; show the actual error, and provide an already-requested report if logs exist. Store `performance_offer_shown` so completion offers the report once across continuation. Log ingestion delay is separate from send processing.

## Reporting resource and schema binding

Resolve `service_bindings.reporting` with either a documented read operation and response paths, or a host-maintained explicit mapping. Verify the chain: authenticated account/region + campaign workspace + its assigned email domain resource ID -> delivery-log database and events table. If multiple resources apply, require an authoritative campaign-specific mapping; do not pick the first sender/domain or infer database names. Record the binding evidence and verify read access by schema inspection/read-only query before generating metrics. Missing reporting access blocks the report, not an otherwise valid send; disclose it in the launch review when reporting was requested.

Require observed fields/types compatible with the KPI query: Unix-second `time`, string `campaign_id`, nonempty string `message_id`, string `event_type` with documented Delivery/Open/Click/Bounce/Complaint values, and boolean `test_mode` when present. Reject an incompatible schema rather than guessing casts or event-name mappings. Bind query execution, returned job ID, terminal job status and result retrieval through installed `tdx query` help/current query contract. Validate a single aggregate result row before publication.

For absent `test_mode`, `legacy_test_mode_evidence` must identify the provider/migration document and the affected resource/schema generation that proves flags are absent only for normal sends. The statement that D3 is expected to write flags is not sufficient evidence. Without verified evidence, block report generation; never ALTER logs or silently remove the predicate. Bind campaign IDs and timestamps with safe escaping under performance-report.md.
