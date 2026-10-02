# Completed campaign review report

## Present before approval

After draft push and validation, AI Studio must present a completed campaign review report before any live launch. Read back the saved campaign and recipient table; use actual saved values and the same rendered content that will be sent. Never substitute a CLI success message or a subject-only preview for the report.

Save `campaign-review.md` and the resolved participant `email-preview.html` beside the run's campaign artifacts. Display the full review in AI Studio, using its native rendered HTML preview if available, or a visible preview artifact plus in-conversation report. A filename alone is not presentation. Do not require the participant to navigate CLI logs or understand YAML to approve.

In Plot-twist, make the complete rendered email the main surface and show a compact summary of inherited decisions, list/copy changes, actual business-versus-QA destinations and sender/readiness. Keep the full four sections available in the displayed/detail report; do not omit exclusions or hide blockers.

Use these four report sections, in order:

### 1. Email content

Show the resolved subject and rendered full email body, selected messaging direction, deal size, two or three product recommendations and actual CTA destination. Provide the plain-text version when configured. If HTML cannot render inline, make the preview artifact directly available and summarize the complete offer/product/CTA content in the displayed report. Mark unavailable assets or links explicitly.

### 2. Personalization

Label a Plot-twist participant preview as a delivery-confirmation example, not proof of customer-cohort membership. Show the participant's resolved subject and greeting, and a compact field-to-value table for the attributes actually used. Include one fictional sample preview from the selected delivery audience when one exists, using its own values. If no sample is selected, show the participant preview alone and state that no sample is in the send audience. Any optional sample outside that audience must be labeled an unsent illustration; never add it to targeting to satisfy preview requirements. Explain fictional business signals where applicable; do not imply QA has purchase/churn signals. Show missing-value and unresolved-token validation results; distinguish system-resolved unsubscribe from profile attributes. Keep full participant values in this personal review only; no real profiles in shared summaries.

### 3. Audience

Reference the Plot-twist impact report (or standalone audience insight report) and summarize the selected persona hypothesis and its supporting signals. Recompute that report if source data or criteria changed; do not present persona hypotheses as measured behavior or predicted results. Show chosen business criteria, full dataset count, selected business-cohort count, actual delivery row count and unique email count. Break delivery down into selected business destinations and the one QA destination in Plot-twist (standalone participant/test breakdown otherwise). Show original-audience overlap/additional reach only when verified and disclose QA/business overlap. Show excluded counts/reasons. State that samples use success+sampleNNN@simulator.amazonses.com and simulate SES delivery rather than human opens/clicks. Show the participant's actual destination and a short labeled sample list, not a full raw dataset. Include the actual database/table as a secondary source detail; all counts must come from the verified selected table/data. Do not promise 31 sends if filtering or service behavior changes the count.

### 4. Sender and campaign settings

Show saved campaign name and ID, intended Engage workspace, one-off CSV List type, verified sender display name/from/reply-to, immediate launch timing and display timezone for ListCampaign (future scheduling is unsupported here); show scheduled timing only for another model whose service contract supports it, relevant tracking settings, template reference and unsubscribe behavior. State observed configuration/readiness results and remaining blockers. Do not call unconfigured values defaults or hide unknown timing. Do not mark ready if required checks failed.

## One final approval

End a ready report with a single clear action: “Approve and launch this campaign.” Accept that action or an explicit equivalent such as “I approve this report; launch the campaign” or “Launch this campaign” as authorization to send the reviewed version. Generic “looks good,” business direction choices and technical preparation permission are not launch authorization.

Do not invoke an optional business-choice tool as a substitute for required send authorization. Prefer a documented native approval action if supported, otherwise an explicit ordinary-message instruction. Do not ask a second confirmation after approval; use the documented launch command with --yes.

For blocked reports, show blockers and invite corrections, not approval to launch. No answer means no approval and no send. Recheck the current report fingerprint, recipient source and saved campaign before execution. If content, personalization, audience, sender or settings changed, invalidate the previous approval, present a new report and obtain approval for that version.

## State

Persist report version/path, report fingerprint, presentation status and actual approval text/action with time in private run state. Fingerprint campaign ID, subject, sending HTML/plaintext, selected recipient data, source table, source mapping, sender, workspace and delivery/tracking settings. Do not store credentials or full recipient rows in this state. Approval applies only to that run and version. After launch report actual service status; do not promise inbox arrival.

## Deterministic fingerprint and launch recheck

Build a versioned fingerprint manifest from read-back saved values: authenticated account/region, campaign ID/model, workspace ID, sender ID and resolved from/reply-to/display name, template reference, source database/table/mapping, subject, sending HTML/plaintext, recipient-data digest, and delivery/tracking settings. Hash exact UTF-8 subject/content bytes without resolving send-time system tags. Include every mapped recipient attribute, not just email/count. For recipient data, serialize each verified imported row as JSON with sorted column keys and observed scalar types, sort those serialized rows, preserve duplicates, then hash the array. This makes row ordering irrelevant while preserving data changes. Serialize manifest JSON with sorted keys, UTF-8, compact separators, no NaN/Infinity and explicit nulls; compute SHA-256. Keep hashes in state, not full rows. Exclude report prose, presentation timestamps, query IDs and processing status from the send fingerprint. Record the fingerprint algorithm version; do not compare different versions as equal.

After approval, read back the saved campaign, sender settings and source rows again and recompute the same manifest before launch. Do not use cached local CSVs as proof that a TD table is unchanged. Block on failed reads or stale analysis awaiting an audience-update decision. On mismatch, invalidate approval and present a newly validated review; its new approval is required. Persist approval as run ID + review version + fingerprint + actual text/action + timestamp. Require presentation status for that exact version and no already-submitted/uncertain launch intent before invoking launch. If the service supports conditional revision checks, use their documented contract; otherwise perform the recheck immediately before launch and disclose that this cannot eliminate a concurrent external mutation. Do not claim atomic server-side approval enforcement.
