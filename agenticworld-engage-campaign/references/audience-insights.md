# Audience insights before selection

## Sequence and source

In standalone mode or when a new audience choice is required, compute, save and display an audience insight report before asking which audience to use. In Plot-twist with an inherited choice, use plot-twist.md's concise added-list impact report and do not reopen Customer Discovery. Exclude record_role=workshop_self_test rows from business counts, comparisons and personas. Read the current run's reusable CSV/snapshot, not cached counts from another campaign. Use local aggregation or a verified read-only query; do not ask the marketer for technical permission. Retain the original dataset. Save `audience-insights.md` beside the personal run artifacts, record source hash, generation time, criteria and report version in private campaign state, and present the substantive comparison in conversation/AI Studio before invoking the choice tool. Do not build an unrelated website.

In standalone mode, for a supplied/delegated choice display the comparison and mark the adopted strategy, but skip the question. In Plot-twist, show the concise impact report with the inherited strategy marked; do not require a full repeated comparison. For a CSV-only/add-row request, do not force this campaign report. Refresh requests reread the source and recompute; keep the last successful report marked stale if computation fails. An analysis refresh updates only the insight report; it must not mutate the saved campaign or recipient table or send. Compare the new analysis with the active selection snapshot. If data changes the prelaunch selected cohort, mark the launch review stale and invalidate approval. Preserve the active snapshot until the participant asks to apply the updated audience (or has explicitly delegated that update). Then rebuild cohort/delivery artifacts, import into a new run-owned table without modifying the previous table, update the current draft/source mapping, read back and validate all saved values, and present a new launch review requiring explicit launch approval. Applying an audience update remains part of the same run and does not create a new campaign. After launch, preserve the sent snapshot and clearly distinguish any newer-source analysis.

## Cohort definitions and evidence

Use these two strategies unless the participant specified other evaluable criteria:

- **All overdue customers:** customer_status = active AND email_consent_status = GRANTED AND days_since_last_purchase > expected_repurchase_days.
- **Higher-risk overdue customers:** all preceding criteria AND propensity_to_churn >= 0.70. Describe 0.70 as a workshop threshold, not a validated business model cutoff.

Parse numeric CSV strings before comparison. Require finite values; scores must be in [0, 1], purchase days and monetary/order/points values must be nonnegative, and expected purchase days must be positive. Use days versus expected days for overdue logic; flag inconsistencies with purchase_window_status. Do not replace missing/invalid values with zero or assign synthetic attributes/consent to real imports. Exclude unknown required values from the affected evaluable cohort and disclose counts/reasons. Missing churn excludes only higher-risk evaluation, not otherwise eligible broader members. Use valid values for optional aggregate metrics and show the denominator or missing count. Preserve each profile row; disclose duplicate customer IDs and resolve them before claiming a trustworthy customer count. Do not deduplicate SES sample profiles merely because they share a simulator route.

Compute for every offered option from its own rows:

| Metric | Computation / display |
|---|---|
| Business cohort | Profile count and share of full dataset; disclose ineligible/unevaluable rows |
| Purchase gap | Median days since purchase, median expected repurchase days, and median row-level excess days (days minus expected); do not subtract medians |
| Purchase history | Median completed_orders_12m, average_order_value_12m and net_sales_12m; use stored values, flag contradictions |
| Model scores | Median churn and conversion scores with coverage; call them scores, not forecast response rates |
| Loyalty | Enrolled share and tier counts, with known-value denominator |
| Channel | Preferred-channel distribution and email-preference share; email consent does not imply email preference |
| Product signals | next_best_product_id distribution only if host-verified catalog mapping exists; otherwise state unavailable |
| Delivery | Verified eligible delivery count and participant inclusion, or pending verification; do not equate business profiles with sends |

State the intersection count and that higher-risk is a subset of all overdue customers. Do not add their counts. When reporting a share, show its denominator. Describe unavailable optional metrics explicitly. For zero rows, display zero and “No data-grounded persona available”; for very small groups, disclose limited evidence. Do not fabricate benchmarks, significance, uplift, expected revenue, causal explanations or statistical confidence. Show observed similarities when the options differ only by risk score.

## Brand interpretation and personas

Anchor the brand lens in the supplied Northstar brief/template: a home-and-living retailer, home refresh, sofa/rug/lamp, and the fictional 20% offer. Use host-provided brand guidance if available; do not infer luxury positioning, sustainability claims, price positioning or demographic targets from product names.

Give each nonempty evaluable option one short representative persona, in the participant's language. Present a composite **hypothesis based on cohort signals**, not a real named customer or a claim that all members behave alike. Include:

1. A behavior-based label, such as “Past buyers overdue for their next home refresh.”
2. Two or three computed signals with values/coverage from this cohort.
3. A tentative Northstar interpretation tied to those signals, such as a possible opportunity to renew the customer relationship. Explain uncertainty about why customers have not returned.
4. A suggested message angle and the existing offer/products, plus a sample opening clearly labeled proposed copy.
5. A limitation: observed history/score alone does not establish motivation, discount sensitivity or product preference.

Separate **Observed data**, **Persona hypothesis** and **Suggested brand message** visibly. Do not invent age, gender, income, family composition, home ownership, lifestyle, design taste or psychological motives. Do not infer geographic traits from synthetic postal codes. Mention product affinity only with verified catalog-backed signals; otherwise explain that the three cards are fixed workshop content. Do not claim conditional product personalization or use loyalty/points in copy without verified content/merge support.

Generated profiles are fictional. Label the overall report “Workshop simulation based on fictional profiles”; participant identity is supplied. Standalone business-profile defaults are fictional; Plot-twist QA has no purchase/model defaults and is not part of persona evidence. Mixed/real imports require explicit provenance labels and must not be presented as fully synthetic. Use aggregate facts, not raw email/name lists, in the comparison.

## Display contract

Use this concise layout, with actual computed values instead of illustrative numbers:

1. **Scope:** brand/goal, source filename, generated-at time/timezone, profile count, provenance and data gaps.
2. **Comparison table:** the two strategies as columns, clear criteria, counts/overlap and available metrics above.
3. **Persona for each option:** observed signals → tentative interpretation → proposed message → limitation.
4. **Recommendation:** which strategy fits the stated goal and why; disclose reach-versus-focus tradeoff and participant eligibility. The broader cohort remains the default for the first workshop win-back exercise unless the participant's explicit goal changes it.
5. **Choice:** only after the report is displayed, ask the structured business question under guided-journey.md. If the choice is already supplied/delegated, state it and continue.

Keep the report readable; use a comparison table and short persona paragraphs. The report supports audience selection and does not replace the separate completed campaign launch review or post-delivery performance report.
