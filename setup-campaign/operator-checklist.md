# Workshop operator checklist

Keep participant-facing content in English and technical details backstage.

## Campaign setup and resource selection
- [ ] Start setup-campaign only for an explicit email-campaign setup/create request; CSV creation alone does not trigger it.
- [ ] Reuse the Intake handoff. If the audience choice is “Create new,” invoke Intake with existing answers, then resume setup with the returned CSV.
- [ ] Run read-only account/workspace/template/sender discovery without “May I run these?” or “Command I’ll run” preambles; respect host/runtime permission prompts.
- [ ] Ask one friendly resource-choice question at a time for Workspace, Template, Sender, and CSV audience. Show `Agentic World Workspace`, `Template Email - Northstar`, and `Northstar Email` only if present in live discovery.
- [ ] For “Create new,” collect needed values and use only documented creation operations. Use the Engage template YAML+HTML workflow for supported new templates. If Workspace/Sender creation is unsupported, report the operator action needed; never guess commands or IDs.
- [ ] Reuse profile answers from intake; ask all missing required profile values together in one ordinary message, never with a Question tool or form; skip questions when complete.
- [ ] Introduce the participant as Northstar Home & Living's marketer re-engaging customers overdue for another purchase.
- [ ] Reuse the objective; ask only for unresolved creative direction. Default to warm home inspiration.
- [ ] Use approved recommendation/offer/CTA content; do not invent purchase history, discounts, prices, or URLs.
- [ ] Explain that the story's business audience is fictional and that the workshop CSV does not establish overdue-customer segmentation.
- [ ] Show the participant's personalized preview and invite subject/body/CTA edits.
- [ ] Update the DRAFT and preview automatically; keep a single final send confirmation.
- [ ] Confirm the actual workshop send target: one participant-provided address plus 30 approved test-recipient destinations by default (31 total), not Northstar's real customer database.
- [ ] Allow the fictional Northstar brand once claims, CTA behavior, assets, sender, and unsubscribe behavior are verified. No postal address is required for the workshop demo; require one only for production sends to real customer recipients. Any unverified benchmark/mock content or supplied assets remain draft-only.

## Readiness
- [ ] Establish data handling, retention, query-history handling, destination, limits, recipient scope, and cleanup ownership once.
- [ ] Verify account/workspace/template/sender IDs against discovery results and confirm existing permissions without collecting credentials.
- [ ] Retain discovered settings for one consolidated report at the final review; do not ask for a separate settings-only confirmation.
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
- [ ] Verify sender, personalization/blanks, CTA behavior, assets, and unsubscribe. A workshop demo to the participant and approved test recipients does not require a postal address; remove any address placeholder. Require an approved postal address for production sends to real customer recipients.

## Send and completion
- [ ] Establish write exclusion and private canonical row-set fingerprint using existing operator controls.
- [ ] Run launch dry-run and separately verify exact full-CSV/table match, unique email, authorized 31-recipient cap, and recipient authorization/consent/suppression basis.
- [ ] Display one settings report, exact preview, sender, participant-plus-test recipient set/count, and send-now scope; obtain one final confirmation covering both settings and send.
- [ ] Recheck unchanged content/source and launch the same ID once with supported `--yes` and the same verified runner.
- [ ] Respect runtime approvals; never add duplicate chat approvals or evade denial.
- [ ] Inspect uncertain outcome before retrying; read back same-ID state.
- [ ] Report observed state honestly; ACTIVE/FINISHED does not establish inbox delivery.
- [ ] Record non-PII execution evidence and final send confirmation; exclude performance reporting.
