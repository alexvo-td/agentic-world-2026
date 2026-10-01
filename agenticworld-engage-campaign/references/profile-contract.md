# Reusable Northstar profile contract

## CSV schema

Use plain column names; `profile.` belongs in merge tags only.

```text
customer_id,app_user_id,email_address,first_name,last_name,customer_status,days_since_last_purchase,expected_repurchase_days,purchase_window_status,purchased_in_last_30_days,purchased_in_last_90_days,purchased_in_last_120_days,completed_orders_12m,average_order_value_12m,net_sales_12m,preferred_channel,next_best_channel,next_best_product_id,propensity_to_churn,propensity_to_convert,email_consent_status,push_consent_status,sms_consent_status,in_app_consent_status,loyalty_status,loyalty_tier,points_balance,postal_code
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

Generate 30 varied samples (recent/on-track and overdue, multiple channels and consent values). Do not contact the example customer in the pasted console profile. Do not manufacture phone numbers or add unneeded timestamps.

Participant fictional defaults: active, days 180, expected 90, overdue, all three purchased flags N, preferred/next channel email, email consent GRANTED, other channel consent DENIED. Preserve explicit participant corrections; never overwrite a genuine DENIED value silently. These behavioral values are fictional and must be described as such.

## Delivery addresses and selection

Default sample addresses: `customer000001@northstar.example` through `customer000030@northstar.example`. They are dataset placeholders, not deliverable recipients. Keep them out of the send audience. Never treat arbitrary public test domains as safe inboxes.

For samples to receive mail, host must supply controlled, verified test inbox addresses and declare they are authorized for the workshop. Do not guess aliases or expand plus-addresses. Keep their delivery configuration separate from participant identity. If no verified test inboxes exist, send only to the eligible participant: 31 stored profiles, 1 recipient. If supplied, use the actual eligible controlled-inbox count; do not force 31.

Choose the business cohort under guided-journey.md first (all overdue or high-churn overdue); retain its artifact/count separately. Delivery eligibility: member of the selected cohort AND active AND overdue AND email_consent_status=GRANTED AND email is the participant's supplied self-send address or a host-verified test address. Record exclusions and count after selection. Synthetic consent does not authorize delivery to unrelated real addresses.

Use UTF-8 and Python csv quoting. Trim email whitespace; preserve spelling/case except for case-insensitive deduplication keys. Do not lowercase names. Upsert by normalized email; preserve existing IDs, extra columns, sample rows and user overrides. For externally supplied data, validate consent/eligibility and fill only missing fictional fields after identifying it as workshop data. Do not assign synthetic consent to real imported customer records.

## Recipient table email column

Keep `email_address` in the reusable dataset. Build the selected-recipient import artifact with a physical `email` column populated from `email_address`; keep other mapped attributes. Import into the campaign recipient table and verify `email` exists with the expected values. `source_columns` requires `key: email`, `sql_name: email`, `type: string`; an alternate `sql_name: email_address` is invalid. Preserve the reusable CSV and shared tables. Retain email_address additionally only if needed for subsequent profile personalization.
