# Post-delivery performance report

## Offer and refresh

If reporting_requested is already set by a participant/facilitator workshop request that includes performance review, generate directly and skip the question. Otherwise, after observed send-processing completion (including partial failure), ask once with the available business-choice tool: “Would you like to see this campaign's performance report?” Options: “Show report” and “Not now”. If the participant already requested reporting, generate it without asking again. Use the status binding under tdx-commands.md; processing completion does not mean every message was delivered or every event has arrived. Submission alone is not completion: if still processing, state actual status and allow an explicitly requested interim report. Do not repeatedly prompt while polling or fabricate completion.

On “refresh/update the report” or equivalent, re-query delivery events and regenerate the report for the same campaign. Do not merely redisplay cached metrics, relaunch, create another campaign or change its audience. Preserve the resolved campaign scope. Show generated-at time on every version; late events and subsequent opens/clicks can change results. No technical query approval is needed after reporting is requested.

## Resolve scope before querying

Read the actual campaign model, ID, launch/schedule timestamps and timezone. For ListCampaign: period starts at launched_at and ends exclusively seven days later; future scheduling is not supported. For regular one-off: use start_at interpreted in campaign timezone when present, otherwise launched_at; end exclusively seven days later. For always-on: seven days preceding report creation time, so a newly generated refresh resolves a new rolling period. Never ask participants to select a reporting period.

Follow service-bindings.md for authoritative resource mapping, schema checks and query job/result retrieval. Resolve the email domain resource assigned to the campaign's workspace and its actual delivery-log database. Do not derive a database from a free-form domain string, use agentic_world_demo as event storage, or silently choose a source/CDP database. Verify events table and actual column types/schema. Freeze period_start, period_end, email domain resource, resolved event database and campaign ID for each running report. Store them in the private report record along with campaign_model for resource resolution. Campaign/domain changes during a query must not change that query's scope. A refresh for a one-off/ListCampaign preserves its resolved period and source unless an explicitly reviewed scope correction is needed.

Filter by campaign_id only; do not filter campaign_model, because historical events may have it null. Cache/report identity excludes campaign_model. Use safe identifier validation/quoting for the database and parameter binding or equivalent value escaping for campaign ID and period. Never interpolate raw IDs into SQL.

## Exact KPI query

Create a private SQL file and run via direct tdx query. Replace placeholders through binding or safe escaping; the template is not executable as written.

```sql
WITH per_message AS (
  SELECT
    message_id,
    max(CASE WHEN event_type = 'Delivery' THEN 1 END) AS delivered,
    max(CASE WHEN event_type = 'Open' THEN 1 END) AS opened,
    max(CASE WHEN event_type = 'Click' THEN 1 END) AS clicked,
    max(CASE WHEN event_type = 'Bounce' THEN 1 END) AS bounced,
    max(CASE WHEN event_type = 'Complaint' THEN 1 END) AS complained
  FROM <event_database>.events
  WHERE td_time_range(time, :period_start, :period_end)
    AND campaign_id = :campaign_id
    AND coalesce(test_mode, false) = false
    AND message_id IS NOT NULL
  GROUP BY message_id
)
SELECT
  count(delivered) AS delivered,
  count(opened) AS unique_opens,
  cast(count(opened) AS double) / nullif(count(delivered), 0) AS open_rate,
  count(clicked) AS unique_clicks,
  cast(count(clicked) AS double) / nullif(count(delivered), 0) AS click_rate,
  count(bounced) AS bounced,
  count(complained) AS complaints
FROM per_message
```

Each marker is 1 or null, so counts represent distinct message IDs per event type and resist duplicate event writes/repeated opens and clicks. Rates are against Delivered, not input rows or Send events. Display rates as percentages, with null denominator results as “—”, not 0%. Do not intersect opens/clicks with delivered IDs or cap rates silently; implement the supplied definition exactly. Use exact counts; approximate aggregation is allowed only after a confirmed memory-limit failure and must be labeled approximate.

## Test-mode schema compatibility

Exclude test_mode=true. Historical null values count as normal through coalesce. Inspect the schema before referencing test_mode: older tables without any test events may lack this column. Do not run known-invalid SQL or ALTER a delivery-log table. If absent, verify through documented migration/provider evidence that missing flags represent normal sends; only then omit the test_mode predicate for that legacy schema, recording this compatibility decision. Otherwise report the schema prerequisite and failed/blocked generation without claiming test exclusion. Verify observed schema and the resource-specific provider/migration evidence under service-bindings.md rather than assuming migration completion.

Neither record_role=workshop_self_test nor SES success simulator recipients are automatically test_mode sends. Exclude by actual test_mode, not by simulator email address, unless a separately requested report changes the contract. Explain that included simulator delivery events represent simulated delivery, not human engagement. Do not promise their opens/clicks or exclude them silently.

## Report presentation

Display the report in AI Studio and save/update performance-report.md in the personal run folder; preserve report metadata and generated-at timestamp. Use a native report/HTML surface when available. Keep the same report surface through not generated, generating, failed, no-event and ready states. On query failure retain the last successful report labeled stale, include its original generation time, and show the failure; do not replace metrics with zero.

Layout:
- Campaign name; current Performance context.
- Resolved period start/end with timezone and explicit end-exclusive semantics; generated-at timestamp.
- KPI cards: Delivered; Unique opens (count and rate); Unique clicks (count and rate).
- Delivery issues: Bounced; Complaints.
- Refresh report action when supported, or the instruction “Ask me to refresh this report.”

Wrap cards into one or two columns on narrow screens. Do not include a period selector, Campaigns sent, “of N sent”, link text or per-URL breakdown. Do not build an unrelated website for this report. Zero events is a successful no-event result with zero counts and undefined rates; distinguish it from query failure and delayed data. Label interim reports and explain metrics may change as events arrive.

If an API-shaped metric result is needed, use attributes.metrics.delivered, uniqueOpens, openRate, uniqueClicks, clickRate, bounced and complaints. Rates are ratios in data, percentages in display. These are mappings, not a claim that a report API was called.

## Record and validation

Persist campaign/run ID, campaign_model, period_start/end, email domain resource and event database, report state/version, job identifier if available, query hash, generated-at timestamp, actual metrics and schema compatibility decision. Never store credentials or unnecessary recipient/event rows. Validate query success and returned numeric fields before presentation. Verify refresh issues a new query and replaces metrics only after success. Report generation creates no campaign or delivery action.

## Refresh ordering and publication

Resolve an existing report from its private run/account/region/workspace/campaign identity; if more than one campaign matches a standalone refresh request, ask which campaign rather than taking the latest silently. Do not enter new-campaign preparation. For one-off/ListCampaign, reuse the stored period and event source; detect drift against current resource bindings and retain the existing scope unless a correction is explicitly reviewed. Capture the launch-time reporting binding when available so a later workspace-domain reassignment cannot silently redirect historical reporting. If no launch-time binding exists, verify the current mapping also covers this campaign's launch before the first query. A not-yet-launched campaign has no launched_at-based report period: explain that prerequisite instead of guessing a date.

Before each generation, atomically increment and persist report_request_version, the frozen scope, request time and generating state. Launch a fresh query even when the SQL hash is unchanged. Keep at most one active query per report where possible; queue a newer request or use version checks if concurrent jobs exist. Store each job ID against its request version. After job completion, validate one row with all seven KPI fields: nonnegative integer counts and finite nonnegative ratios, or null ratios when delivered is zero. Do not cap rates above 1 or intersect event sets; retain the exact KPI definition.

Publish metrics only if the completing request is still the latest request version and its frozen scope matches; discard older completions from the displayed report. Apply the same version check to errors so an older failure cannot overwrite a newer success. Write the new report/metadata to temporary files and atomically replace the visible report, committing ready state last. Reconcile an interrupted publication before claiming ready. Retain the previous successful metrics/time while generating and on failure, labeled stale. Record last_attempt_at separately from last_successful_generated_at; a failed refresh never advances the successful generation time. Persist performance_offer_shown independently from report state so Not now is not repeated on continuation.

In Plot-twist, accompany KPIs with a short interpretation: this includes simulator/confirmation delivery according to actual test_mode and does not establish customer response or revenue growth. Explain no-event/delayed/interim states plainly; provide Refresh instead of inventing engagement. Save actual outcomes/gaps and report references into journey-handoff.md without creating a journey or schedule.
