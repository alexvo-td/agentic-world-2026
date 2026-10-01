# Workshop operator checklist

Keep participant-facing content in English and technical details backstage.

## Northstar participant journey
- [ ] Reuse profile answers from intake; ask all missing required profile values together in one ordinary message, never with a Question tool or form; skip questions when complete.
- [ ] Introduce the participant as Northstar Home & Living's marketer re-engaging customers overdue for another purchase.
- [ ] Reuse the objective; ask only for unresolved creative direction. Default to warm home inspiration.
- [ ] Use approved recommendation/offer/CTA content; do not invent purchase history, discounts, prices, or URLs.
- [ ] Explain that the story's business audience is fictional and that the workshop CSV does not establish overdue-customer segmentation.
- [ ] Show the participant's personalized preview and invite subject/body/CTA edits.
- [ ] Update the DRAFT and preview automatically; keep a single final send confirmation.
- [ ] Confirm the actual workshop send target: one participant-provided address plus 30 approved test-recipient destinations by default (31 total), not Northstar's real customer database.
- [ ] Allow the fictional Northstar brand once content claims, CTA, assets, sender, postal address, and unsubscribe behavior are verified. Any unverified benchmark/mock content or supplied assets remain draft-only.

## Readiness
- [ ] Establish data handling, retention, query-history handling, destination, limits, recipient scope, and cleanup ownership once.
- [ ] Verify actual account/workspace/template/sender and existing permissions without collecting credentials.
- [ ] Require exact tdx `2026.9.3`; reuse installed `tdx` when already exact, otherwise prepare and verify pinned `npx --yes --package=@treasuredata/tdx@2026.9.3 tdx` in the campaign runtime.
- [ ] Carry the exact verified runner command/runtime from intake into all campaign operations; do not substitute versions or use `--offline`.
- [ ] Verify personalization uses `{{ profile.<attribute_name> }}` tokens; mapping keys remain unprefixed.

## Setup and preview
- [ ] Reuse intake CSV and answers; validate source/schema/key/count and the participant-plus-30-approved-test recipient composition.
- [ ] Resolve invalid/ignored rows explicitly without silently dropping recipients.
- [ ] Create a unique table and INSERT automatically under approved setup scope; inspect uncertain jobs before retrying.
- [ ] Validate, dry-run, and save the intended DRAFT with supported `--yes` without separate conversational approval.
- [ ] Capture exact ID and compare persisted source/mappings/template/sender/content.
- [ ] Render exact saved HTML with `{{ profile.first_name }}`-style tokens; accurately label static previews.
- [ ] Verify sender, personalization/blanks, CTA, assets, unsubscribe, and postal address. Stop delivery if any critical item is unverified.

## Send and completion
- [ ] Establish write exclusion and private canonical row-set fingerprint using existing operator controls.
- [ ] Run launch dry-run and separately verify exact full-CSV/table match, unique email, authorized 31-recipient cap, and recipient authorization/consent/suppression basis.
- [ ] Display exact preview, sender, participant-plus-test recipient composition/count, and send-now scope; obtain one final confirmation.
- [ ] Recheck unchanged content/source and launch the same ID once with supported `--yes` and the same verified runner.
- [ ] Respect runtime approvals; never add duplicate chat approvals or evade denial.
- [ ] Inspect uncertain outcome before retrying; read back same-ID state.
- [ ] Report observed state honestly; ACTIVE/FINISHED does not establish inbox delivery.
- [ ] Record non-PII execution evidence and final send confirmation; exclude performance reporting.
