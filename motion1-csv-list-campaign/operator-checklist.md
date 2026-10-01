# Workshop operator checklist

Keep participant-facing content in English and technical details backstage.

## Northstar participant journey
- [ ] Introduce the participant as Northstar Home & Living's marketer re-engaging customers overdue for another purchase.
- [ ] Reuse the objective; ask only for unresolved creative direction. Default to warm home inspiration.
- [ ] Use approved recommendation/offer/CTA content; do not invent purchase history, discounts, or URLs.
- [ ] Explain that participant and fictional profiles demonstrate the story, without claiming actual overdue-customer segmentation.
- [ ] Show the participant's personalized preview and invite subject/body/CTA edits.
- [ ] Update the DRAFT and preview automatically; keep a single final send confirmation.
- [ ] Confirm actual workshop recipient composition/count, not delivery to Northstar's real customers.
- [ ] Allow the fictional Northstar brand once placeholders and required delivery settings are verified.

## Readiness
- [ ] Establish data handling, retention, query-history handling, destination, limits, recipient scope, and cleanup ownership once.
- [ ] Verify actual account/workspace/template/sender and existing permissions without collecting credentials.
- [ ] Accept tdx 2026.9.2 or later; reuse the compatible installed runner. Prepare 2026.9.3 only if setup is needed.
- [ ] Verify personalization uses profile.<attribute_name> tokens; mapping keys remain unprefixed.

## Setup and preview
- [ ] Reuse intake CSV and answers; validate source/schema/key/count and authorized recipient composition.
- [ ] Resolve invalid/ignored rows explicitly without silently dropping recipients.
- [ ] Create a unique table and INSERT automatically under setup scope; inspect uncertain jobs before retrying.
- [ ] Validate, dry-run, and save the intended DRAFT with supported --yes without separate approval.
- [ ] Capture exact ID and compare persisted source/mappings/template/sender/content.
- [ ] Render exact saved HTML with {{ profile.first_name }}-style tokens; accurately label static previews.
- [ ] Verify sender, personalization/blanks, CTA, assets, unsubscribe, and postal address.

## Send and completion
- [ ] Establish write exclusion and private canonical row-set fingerprint using existing operator controls.
- [ ] Run launch dry-run and separately verify exact source match, authorized count, consent/suppression.
- [ ] Display preview, sender, recipient composition/count, and send-now scope; obtain one final confirmation.
- [ ] Recheck unchanged content/source and launch the same ID once with supported --yes.
- [ ] Respect runtime approvals; never add duplicate chat approval or evade denial.
- [ ] Inspect uncertain outcome before retrying; read back same-ID state.
- [ ] Report observed state honestly; ACTIVE/FINISHED does not establish inbox delivery.
- [ ] Record non-PII execution evidence and final send confirmation; exclude performance reporting.
