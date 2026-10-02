# Northstar content and preview

## Fixed brief

Re-engage overdue customers with a fictional workshop offer: 20% OFF selected home favorites. Subject: `{{profile.first_name}}, enjoy 20% off your next home refresh`. Greeting: `Hi {{profile.first_name}},`. Keep all three product cards by default; support an explicit choice of two by adapting only the personal copy. In Plot-twist, inherit the selected copy and recommend only a justified subject/opening change under guided-journey.md; in standalone mode guide home-refresh versus welcoming win-back. Wait only for unresolved content choices. Store next_best_product_id for later exercises without conditional product rendering in this exercise.

The supplied source is retained in `assets/northstar-source.html`. The normalized workshop template is `assets/northstar-email.html`, with stylesheet embedded; `assets/northstar.css` retains the original CSS. It removes all benchmark/reference prices and conflicting discount rates. Do not present other retailers' prices as Northstar prices. Do not invent sale amounts, deadlines or promo codes. Use host overrides consistently if a different workshop offer is supplied.

## Merge tags

Use `{{ profile.attribute }}` (compact brace spacing is also valid) for every customer attribute, e.g. first_name, last_name, loyalty_tier, points_balance. Reject `{{first_name}}`. Retain `{{sender.unsubscribe_url}}` exactly in sending content. Validate all profile tags against imported column names. Escape values when resolving HTML previews; never treat participant text as markup. Keep server merge tags intact in campaign HTML. Check `source_columns` keys against actual table columns using [campaign-yaml.md](campaign-yaml.md). Verify image authorization, postal address and sender unsubscribe behavior from the approved assets/configuration; never infer them from reachability or fictional branding.

For blank first names or other personalized values, obtain a correction or explicit approval to remove that personalization. Do not generate fallback data or invent undocumented engine fallbacks or template-engine conditionals. For local previews label sender unsubscribe as system-resolved and disable the link if no real preview URL is available; never replace the send-time system tag with a fake URL.

## Links and visual checks

The original CTA has no destination. Replace the span with an anchor only when a host-provided validated HTTPS collection URL is available; preserve its ID/style. Remove the missing-link explanation after configuring it. Without it, allow a draft preview with a visibly disabled CTA, but do not mark the campaign launch-ready. Verify image availability with supported capabilities; unavailable images require host remediation or approved alternate assets. Check desktop/mobile width, readable offer, three cards, greeting, CTA and unsubscribe. Inline CSS before upload if required by the delivery contract.

## Preview layout

Present this summary within the mandatory four-section report in launch-review.md. Show complete email content and personalization previews, then audience and sender/settings; this summary alone does not replace the rendered full email or final report approval.

Show a rendered personalized email followed by the summary:

| Item | Actual value |
|---|---|
| Campaign | Saved campaign name |
| Goal | Re-engage customers overdue for their next purchase |
| Dataset | Actual total and sample/participant breakdown |
| Audience strategy | Selected criteria and actual business-cohort count |
| Message direction | Selected theme and changes made |
| Sending to | Actual eligible count; exclusions summarized |
| Your recipient | Supplied email; label delivery-confirmation role in Plot-twist |
| Subject | Resolved participant subject |
| Offer | 20% off selected home favorites |
| Products | Japandi Sofa, Geometric Area Rug, Modern & Chic Floor Lamp |
| Audience signal | Observed business-cohort signals; QA has no purchase/churn defaults |
| Sender | Actual verified display name and from/reply-to addresses |
| Settings | One-off, intended Engage workspace, timing, tracking settings |
| Status | Draft / blocked / Ready to launch based on evidence |

Show “Launch this campaign” as the sole business action once ready. Do not add a second confirmation after the participant chooses it. Explain actual selection and destinations plainly: generated samples route to the SES success simulator, while the participant receives their own personalized email. Show business and QA counts, unique destinations, excluded rows and service-reported send count separately; simulator events do not represent human inbox engagement.

Compute the versioned read-back fingerprint under launch-review.md, including saved recipient data and mappings. Save it with preview state; do not use the local eligible CSV alone as its recipient evidence. Local rendering demonstrates personalization but is not proof of server merge behavior. Validate service configuration independently.

Show a concise inherited/current-versus-proposed subject/opening comparison when requesting a change. Use conference wording only when supported by the list fixture/provenance; do not present fixed sofa/rug/lamp cards as individualized recommendations. A QA preview must use the same saved content/mappings and supplied name as sending, with no invented behavioral fields.
