# Reusable Northstar profile contract

## CSV schema

Use plain column names; `profile.` belongs in merge tags only.

```text
customer_id,app_user_id,email_address,first_name,last_name,customer_status,days_since_last_purchase,expected_repurchase_days,purchase_window_status,purchased_in_last_30_days,purchased_in_last_90_days,purchased_in_last_120_days,completed_orders_12m,average_order_value_12m,net_sales_12m,preferred_channel,next_best_channel,next_best_product_id,propensity_to_churn,propensity_to_convert,email_consent_status,push_consent_status,sms_consent_status,in_app_consent_status,loyalty_status,loyalty_tier,points_balance,postal_code,record_role
```

| Fields | Generation contract |
|---|---|
| customer_id, app_user_id | Stable unique synthetic IDs; never copy live customer IDs |
| identity | Sample names are fictional; participant identity is supplied by participant |
| purchase signals | overdue iff days_since_last_purchase > expected_repurchase_days; purchased flags Y iff days <= threshold |
| orders and value | Positive order count, decimal AOV; net_sales = orders × AOV rounded to cents |
| scores | 0–1; participant churn 0.75, conversion 0.60; sample variation |
| channels | email, push, sms, in_app; participant prefers email |
| consent | GRANTED or DENIED; participant email GRANTED represents self-send instruction for THIS exercise, not a persistent marketing opt-in |
| loyalty | not_enrolled/none/0 or enrolled with bronze/silver/gold and nonnegative points |
| next_best_product_id | Use only host-provided catalog IDs; blank if unresolved. Do not associate the pasted P0023 with a product without evidence |
| postal_code | Synthetic five-character string; preserve leading zeros |

Generate 30 varied samples (recent/on-track and overdue, multiple channels and consent values) for a new workshop dataset. For an existing, verified fictional workshop CSV, run prepare_audience.py with --workshop-data to replenish missing WS-C000001 through WS-C000030 IDs while preserving existing rows and overrides. Do not use that flag based on IDs or filenames alone. Omit it for real, mixed or unknown provenance; do not add sample rows to those imports, and report their actual size. Do not contact the example customer in the pasted console profile. Do not manufacture phone numbers or add unneeded timestamps.

Standalone business-profile mode only: participant fictional defaults: active, days 180, expected 90, overdue, all three purchased flags N, preferred/next channel email, email consent GRANTED, other channel consent DENIED. Preserve explicit participant corrections; never overwrite a genuine DENIED value silently. These behavioral values are fictional and must be described as such.

## Delivery addresses and selection

Use the SES success simulator with a distinct documented plus label per sample: `success+sample001@simulator.amazonses.com` through `success+sample030@simulator.amazonses.com`. This is the user-authorized Amazon SES success mailbox simulator destination, not a human inbox. AWS supports mailbox-simulator labeling. Use only these success labels, not unrelated public test domains or bounce/complaint scenarios. Preserve each sample as a distinct profile using customer_id; never deduplicate samples by their shared email address. Upsert the participant independently by their own email, which must not be any success simulator address.

Sending to the simulator requires Amazon SES as the delivery provider; verify the selected Engage sender/delivery route uses SES. AWS documentation: https://docs.aws.amazon.com/ses/latest/dg/send-an-email-from-console.html . The address simulates successful delivery; it does not provide an inbox, opens or clicks for the participant to inspect. Do not infer those events from simulator delivery.

Apply the selected business cohort and consent rules to sample profiles as usual; route eligible samples to the simulator and the eligible participant to their supplied address. Do not silently override DENIED consent or broaden a selected cohort to force 31 messages. Preserve all 30 generated samples in the reusable CSV. Record profile-row count, unique destination count and service-reported send count separately. All 30 samples have distinct labeled recipient addresses. Preserve plus labels through CSV import and delivery; do not strip labels. Verify whether Engage deduplicates by email; do not claim 30 simulator sends unless service behavior supports it. If Engage normalizes away plus labels, report its actual behavior; do not circumvent it through repeated launches.
In standalone business-profile mode, choose the business cohort under guided-journey.md first (all overdue or high-churn overdue); retain its artifact/count separately. Business delivery eligibility: member of the selected cohort AND active AND overdue AND email_consent_status=GRANTED AND email is the participant's supplied self-send address or an approved SES success simulator address matching `success(?:\+[A-Za-z0-9_-]+)?@simulator\.amazonses\.com` (through verified SES delivery) or a host-verified test address. Record exclusions and count after selection. Synthetic consent does not authorize delivery to unrelated real addresses.

Use UTF-8 and Python csv quoting. Trim email whitespace; preserve spelling/case except for case-insensitive deduplication keys. Do not lowercase names. Upsert the participant by normalized email; preserve sample rows by customer_id even when email addresses match; preserve existing IDs, extra columns, sample rows and user overrides. For externally supplied data, validate consent/eligibility and fill only missing fictional fields after identifying it as workshop data. Do not assign synthetic consent to real imported customer records.

## Recipient table email column

Keep `email_address` in the reusable dataset. Build the selected-recipient import artifact with a physical `email` column populated from `email_address`; keep other mapped attributes. Import into the campaign recipient table and verify `email` exists with the expected values. `source_columns` requires `key: email`, `sql_name: email`, `type: string`; an alternate `sql_name: email_address` is invalid. Preserve the reusable CSV and shared tables. Retain email_address additionally only if needed for subsequent profile personalization.

## Upload boundary

Apply csv-upload.md validation and verified upload binding. Rich CSV numeric values describe fictional attributes, not guaranteed TD column types. The supplied helper convention treats non-time fields as text. Parse for cohort selection as needed, then verify actual table types before source_columns mapping. Saving a CSV is not evidence that TD import completed.

## Plot-twist QA and additional-list selection

In Plot-twist, generate/reuse business fixtures separately and run prepare_audience.py --participant-role workshop_self_test --self-test-output participant-confirmation.csv. The confirmation CSV contains the supplied identity, QA ID, record_role=workshop_self_test and self-send GRANTED for this exercise; purchase history, churn and unrelated attributes remain blank. The business source must not be overwritten by the QA output. Preserve matching real business records; genuine DENIED blocks QA until explicitly resolved. A QA row is not a business member and must be excluded from persona/cohort aggregates.

Run analyze_added_audience.py with --input, inherited --strategy (all-overdue or higher-risk), optional verified --baseline, --qa, --participant-email and separate --selected-output/--delivery-output/--report-output paths. Supply --ses-verified and repeated --approved-test-address only after verifying provider/host evidence. The helper excludes known original-audience email overlaps for an additional-list one-off, then includes one independent QA address without relaxing business criteria. Preserve plus labels; exact email overlap is not ID unification. Other inherited criteria require a verified evaluator, not this helper.

Keep selected business source and QA artifacts immutable for each reviewed version. The delivery artifact adds record_role and one QA destination; if QA overlaps a selected delivery row, it is represented once as QA and the report discloses that treatment. Actual service import/count/readiness checks are still required. An eligible QA recipient can be included even when their personal business row is outside the cohort; do not change that customer's history, score or consent. No eligible business profiles, no actual business delivery destination or zero verified additional reach blocks the business campaign; a QA-only preview remains possible. Do not infer service test_mode from record_role.

New workshop fixtures deliberately include three eligible higher-risk business samples alongside varied recent/overdue, consent and channel profiles, so both strategies have evidence without using QA as a persona. This is curated fictional data, not a measured customer distribution. Existing/imported rows are not rewritten to manufacture these groups.
