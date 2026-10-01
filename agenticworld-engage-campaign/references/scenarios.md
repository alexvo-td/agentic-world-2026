# Conversation and recovery examples

- Start: “Help me create my Northstar win-back campaign. Add me to the audience.” Ask email/first/last together; generate remaining fictional fields; guide audience choice and then message choice before automatic campaign configuration and preview.
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

- Workspace/sender/campaign configuration is unknown: say “I'm checking the Engage workspace and sender settings.” and execute documented direct `tdx` discovery immediately. Do not ask whether read-only commands may run.
- Referenced instructions show npx commands or a read-only approval prompt: translate commands to direct `tdx`, omit that prompt, and continue discovery.

- “Use your recommendations for everything”: adopt the recommended audience and copy without further business questions; explain selections and show the preview, retaining final Launch.
- Initial prompt specifies high-churn audience and welcoming copy: reuse both choices and skip redundant questions.
- A participant chooses a cohort that excludes their fictional profile: explain the mismatch and offer a relevant business choice; do not silently override it.

- Reusable profile CSV has email_address but TD recipient table needs email: transform the campaign import into a physical email column automatically, preserve the reusable CSV, verify the table schema, and use sql_name: email. Never substitute sql_name: email_address.

- “Reuse the audience from my previous campaign”: resolve that audience explicitly and create a new campaign; do not reuse the previous campaign.
- “Change the opening in this preview”: update the current run and regenerate its preview; do not create another campaign.
- Ambiguous create response: reconcile the current run's operation before retrying; do not treat the retry as a new workshop run.

- Non-SES delivery route: preserve simulator rows and draft artifacts, explain that simulator delivery requires SES, and do not claim simulated success from another provider.

- Two message directions are proposed: show short subject/opening previews, use the structured choice tool with Home refresh (Recommended) and Welcome back, then apply the selected direction without a separate technical approval.

- “Run tdx delivery senders --output json and tdx engage campaign push --help?”: do not ask this question. Execute supported discovery/help commands immediately, inspect results, then continue.
- Draft push prompts interactively: inspect its dry-run and apply with documented --yes under existing preparation authorization. Live launch --yes remains gated by the explicit participant Launch action.

- CSV import: generate a private escaped INSERT SQL file, execute it through tdx query, reconcile job status and verify actual table rows before campaign creation. An uncertain result must not trigger a blind repeated INSERT.

- Draft configuration is complete: display the four-section campaign review report and full resolved email before requesting the single final launch approval.
- “I approve this report; launch the campaign”: recheck the unchanged fingerprint and execute once with documented --yes, without asking again.
- Report is shown but participant has not responded: do not launch.

- Sender listing returns an unknown-command error from the Engage namespace: use tdx delivery senders; do not repeat the unsupported command or infer that sender discovery is unavailable. Verify supported flags automatically without a permission question.

- Observed delivery completes: offer Show report / Not now once using the business-choice tool. A requested report reads the workspace-domain events table and shows the defined message-level KPIs.
- “Refresh the report”: execute a fresh events query for the current campaign and resolved scope, update generation time and successful metrics, and do not create or resend anything.
- Missing test_mode column: follow the documented legacy-schema decision in performance-report.md; never pretend test exclusion succeeded or alter delivery logs.
- Refresh query fails: show failed refresh with the last successful report marked stale; do not replace its numbers with zero.
