# Conversation and recovery examples

- Plot-twist start: “Use our selected strategy with the new conference list. Add my email for delivery confirmation and show performance after launch.” Reuse the verified discovery handoff, collect missing identity together, prepare independent QA and show the added-list impact before any unresolved copy choice. Do not repeat settled audience choices.
- Explicit standalone win-back: guide the full audience/message comparison and use the fictional business-profile exercise when requested.
- All identity present: “I'm Alex Lee, alex@my-controlled-domain.test. Prepare my workshop email.” Reuse values; no intake question. Address syntax is not proof of delivery; this example is illustrative.
- Partial identity: email and first name supplied; ask only last name. Invalid email: request corrected email only.
- New preparation request with the same email: preserve the identity and source data as appropriate, but create a fresh run audience snapshot/recipient table and campaign. Within that run, upsert the participant once. Never reuse an old draft merely because the email matches.
- Default sample delivery: all 30 generated profiles use unique success+sampleNNN@simulator.amazonses.com labels. Send only cohort/consent-eligible samples through a verified SES route; preserve their distinct customer IDs. Show actual selected rows and unique destination counts; do not assume the service sends once per row.
- Missing sender or CTA: show resolved draft with blocked status and a precise host configuration gap. Do not ask CSV/runtime/mapping approval.
- “Looks good”: at the audience/message decision stage, adopt the clearly presented recommendation and advance; at final preview, treat it as feedback and invite explicit launch. Never interpret it as launch authorization.
- “Launch this campaign” after ready preview: verify fingerprint and launch once; do not request another confirmation.
- “Launch” before preview: finish preparation and show the preview, then invite launch.
- Lost launch response: reconcile service status; never blindly resend.
- Participant changes offer: update subject, hero and every product discount consistently, validate, show updated preview.
- Real customer import with denied consent: preserve denied status and exclude; never apply fictional self-send defaults to real customers.

- Workspace/sender configuration is unknown: complete initial intake and local audience work first. At service preparation, use exact supplied config or needed workspace/sender discovery automatically. Do not search old campaign folders/state to obtain settings, or ask read-only command permission.
- Referenced instructions show npx commands or a read-only approval prompt: translate commands to direct `tdx`, omit that prompt, and continue discovery.

- “Use your recommendations for everything”: adopt the recommended audience and copy without further business questions; explain selections and show the preview, retaining final Launch.
- Initial prompt specifies high-churn audience and welcoming copy: reuse both choices and skip redundant questions.
- Standalone fictional business participant falls outside a selected cohort: explain the mismatch without overriding attributes. Plot-twist confirmation uses independent QA instead; preserve business targeting.

- Reusable profile CSV has email_address but TD recipient table needs email: transform the campaign import into a physical email column automatically, preserve the reusable CSV, verify the table schema, and use sql_name: email. Never substitute sql_name: email_address.

- “Reuse the audience from my previous campaign”: resolve that audience explicitly and create a new campaign; do not reuse the previous campaign.
- “Change the opening in this preview”: update the current run and regenerate its preview; do not create another campaign.
- Ambiguous create response: reconcile the current run's operation before retrying; do not treat the retry as a new workshop run.

- Non-SES delivery route: preserve simulator rows and draft artifacts, explain that simulator delivery requires SES, and do not claim simulated success from another provider.

- Two message directions are proposed: show short subject/opening previews, use the structured choice tool with Home refresh (Recommended) and Welcome back, then apply the selected direction without a separate technical approval.

- “Run tdx delivery senders --output json and tdx engage campaign push --help?”: do not ask this question. At the service stage, execute needed supported discovery/help, inspect results and continue; this does not require startup discovery.
- Draft push prompts interactively: inspect its dry-run and apply with documented --yes under existing preparation authorization. Live launch --yes remains gated by the explicit participant Launch action.

- CSV import: generate a private escaped INSERT SQL file, execute it through tdx query, reconcile job status and verify actual table rows before campaign creation. An uncertain result must not trigger a blind repeated INSERT.

- Draft configuration is complete: display the four-section campaign review report and full resolved email before requesting the single final launch approval.
- “I approve this report; launch the campaign”: recheck the unchanged fingerprint and execute once with documented --yes, without asking again.
- Report is shown but participant has not responded: do not launch.

- Sender listing returns an unknown-command error from the Engage namespace: use tdx delivery senders; do not repeat the unsupported command or infer that sender discovery is unavailable. Verify supported flags automatically without a permission question.

- Observed send processing completes, including partial failure: offer Show report / Not now once using the business-choice tool. A requested report reads the workspace-domain events table and shows the defined message-level KPIs.
- “Refresh the report”: execute a fresh events query for the current campaign and resolved scope, update generation time and successful metrics, and do not create or resend anything.
- Missing test_mode column: follow the documented legacy-schema decision in performance-report.md; never pretend test exclusion succeeded or alter delivery logs.
- Refresh query fails: show failed refresh with the last successful report marked stale; do not replace its numbers with zero.

- Audience choice pending: compute and display the audience comparison and each option's evidence-grounded Northstar persona before invoking the choice tool. Show overlap and distinguish the business cohort from verified delivery eligibility.
- “Use your recommendations for everything”: still present audience insights, mark the recommended strategy as adopted, and continue without a redundant audience question.
- Imported data lacks churn scores: show broader overdue insights where evaluable, mark higher-risk analysis unavailable and do not impute scores or invent a higher-risk persona/count.
- High-risk cohort is empty: show zero and no supported persona; offer the nonempty broader strategy rather than fabricating differences.
- Cohort aggregates are similar: state the observed similarity; do not invent different demographics, styles or discount sensitivity to distinguish personas.
- “Refresh the audience report”: reread the current source, recompute aggregates and regenerate insights. Do not change targeting or send; if a prelaunch selected cohort changes, mark its launch review stale and invalidate approval. Apply updated targeting only on explicit or already-delegated audience-update authorization, then synchronize artifacts, a new run-owned recipient table and the saved draft before a new launch review. After launch, retain the sent snapshot and label analysis of newer data separately.

- Plot-twist participant outside business criteria: include the explicitly authorized identity-only QA address independently; do not change business data. Genuine DENIED or an empty actual business delivery audience blocks business activation. Standalone business-profile mode retains its own eligibility checks.
- Standalone selected audience contains only the participant: label that actual selection and omit the sample preview. Plot-twist has no eligible business recipients: show a QA-only draft, not a customer activation.
- Existing verified workshop CSV has fewer than 30 sample IDs: replenish missing IDs with --workshop-data, preserve existing rows/overrides and verify rerun stability. Real/mixed/unknown-provenance CSV: omit the flag and do not replenish fictional samples.
- Local validate passes but service readiness/status contract is unresolved: retain the draft and report the precise host prerequisite; do not label Ready or fabricate completion.
- Previewed recipient table changes before approval is executed: read-back fingerprint mismatch invalidates approval; no launch until a new review is presented and approved.
- Two refresh jobs finish in reverse order: only the latest request may publish success or failure; keep the previous successful report stale while waiting.
- Reporting workspace-domain mapping changes after launch: preserve the launch-time source and period; do not silently redirect the report.

- Original selected audience/copy supplied: inherit both and show only conference-list impact/justified changes; do not repeat Customer Discovery.
- New list contains prospects with no history: show the win-back mismatch; do not create synthetic history or consent for imported prospects.
- Original audience unavailable: show overlap/net-new unavailable, never zero or deduplicated. Already-sent original with unresolved duplicate risk blocks customer activation.
- Participant QA email matches an eligible business destination: send once, retain business evidence, disclose QA overlap and exclude QA from persona aggregates.
- Request includes performance review: generate real/interim metrics without asking whether to show them; refresh remains query-only.
- Completion: save journey-handoff.md and propose a repeatable workflow; do not create a journey/recurring send or claim revenue growth.

- New invocation while general/previous-run folders exist: ignore them. First introduce the task and ask missing identity in one ordinary message; do not ls/find/glob folders, read old CSV/state or announce a prior campaign.
- Complete identity supplied at invocation: allocate a new run and prepare the new dataset with the documented helper; no folder/history scan, git pull, test reading or helper-source review first.
- No handoff or audience CSV supplied: create fresh fictional business samples and separate QA. Show original overlap unavailable and guide current-data choices; absence is not a technical blocker.
- Explicit refresh for this run: use its exact already-known state/IDs, query afresh and do not start a new campaign. Explicit prior reuse: read only the named target, never scan for latest/matching runs.
