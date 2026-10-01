# Northstar content and preview

## Fixed brief

Re-engage overdue customers with a fictional workshop offer: 20% OFF selected home favorites. Subject: `{{profile.first_name}}, enjoy 20% off your next home refresh`. Greeting: `Hi {{profile.first_name}},`. Keep all three product cards fixed. Store next_best_product_id for later exercises without conditional product rendering in this exercise.

The supplied source is retained in `assets/northstar-source.html`. The normalized workshop template is `assets/northstar-email.html`, with stylesheet embedded; `assets/northstar.css` retains the original CSS. It removes all benchmark/reference prices and conflicting discount rates. Do not present other retailers' prices as Northstar prices. Do not invent sale amounts, deadlines or promo codes. Use host overrides consistently if a different workshop offer is supplied.

## Merge tags

Use `{{profile.attribute}}` for every customer attribute, e.g. first_name, last_name, loyalty_tier, points_balance. Reject `{{first_name}}`. Retain `{{sender.unsubscribe_url}}` exactly in sending content. Validate all profile tags against imported column names. Escape values when resolving HTML previews; never treat participant text as markup. Keep server merge tags intact in campaign HTML.

For blank first names, use a verified engine fallback if supported; otherwise create consistent fallback data before import. Do not invent template-engine conditionals. For local previews label sender unsubscribe as system-resolved and disable the link if no real preview URL is available; never replace the send-time system tag with a fake URL.

## Links and visual checks

The original CTA has no destination. Replace the span with an anchor only when a host-provided validated HTTPS collection URL is available; preserve its ID/style. Remove the missing-link explanation after configuring it. Without it, allow a draft preview with a visibly disabled CTA, but do not mark the campaign launch-ready. Verify image availability with supported capabilities; unavailable images require host remediation or approved alternate assets. Check desktop/mobile width, readable offer, three cards, greeting, CTA and unsubscribe. Inline CSS before upload if required by the delivery contract.

## Preview layout

Show a rendered personalized email followed by the summary:

| Item | Actual value |
|---|---|
| Campaign | Saved campaign name |
| Goal | Re-engage customers overdue for their next purchase |
| Dataset | Actual total and sample/participant breakdown |
| Sending to | Actual eligible count; exclusions summarized |
| Your recipient | Supplied email |
| Subject | Resolved participant subject |
| Offer | 20% off selected home favorites |
| Products | Japandi Sofa, Geometric Area Rug, Modern & Chic Floor Lamp |
| Audience signal | Fictional overdue purchase; 180 days vs expected 90 by default |
| Sender | Actual verified display name and from/reply-to addresses |
| Settings | One-off, intended Engage workspace, timing, tracking settings |
| Status | Draft / blocked / Ready to launch based on evidence |

Show “Launch this campaign” as the sole business action once ready. Do not add a second confirmation after the participant chooses it. Explain exclusions plainly, e.g. “31 profiles saved; your email is the only delivery address. Sample addresses are for analysis.”

Fingerprint the campaign ID, HTML, subject, eligible CSV, sender and settings. Save the fingerprint with preview state. Local rendering demonstrates personalization but is not proof of server merge behavior. Validate service configuration independently.
