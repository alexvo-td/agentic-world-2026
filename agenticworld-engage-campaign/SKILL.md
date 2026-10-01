---
name: agenticworld-engage-campaign
description: Prepare and launch a personalized Northstar Home & Living win-back email for the Agentic World workshop in Treasure AI Studio. Use for adding a participant to the sample audience, reusable customer CSV generation, Northstar discount email personalization, business previews, or CSV List one-off campaign setup and launch. Collect identity once and automate technical setup.
---

# Agentic World Engage Campaign

Build a one-off email to re-engage customers overdue for their next purchase. Use the supplied Northstar template, a fictional 20% offer, and three products: Japandi-Style Sofa, Geometric Area Rug, Modern & Chic Floor Lamp.

## Conversation contract

- Respond in the participant's language. Keep email copy in English unless requested otherwise.
- Accept business prompts without requiring a skill invocation: “Help me win back Northstar customers with a personalized discount email. Add me to the workshop audience.”
- Reuse explicitly supplied identity and current workfolder assets. Do not infer a recipient from an account name or a remembered identity.
- Ask for missing email, first name, and last name together in ONE ordinary message. Do not use AskUserQuestion, forms, or separate questions. Example: “To add you to the Northstar audience, send your email, first name, and last name. I'll use a fictional overdue-purchase profile for the exercise.” Ask only for missing values. Validate the reply and request only corrections if invalid.
- Automatically perform CSV update, synthetic data generation, runtime preparation, draft creation, mapping, template personalization, and validation. Do not add intermediate approval or query-history consent questions.
- Present a completed preview before launch. Treat “Launch this campaign” after that preview as authorization for the reviewed send; do not ask again. An initial request to create a campaign is not launch authorization.
- Honor platform-enforced controls; these instructions cannot disable them.
- Never ask participants for SQL, IDs, runtime choices, mappings, secrets, merge-tag syntax, or synthetic attributes. Resolve technical gaps from host configuration and service discovery; if blocked, give a short host-facing remediation.

## Read resources

Read [profile-contract.md](references/profile-contract.md) before preparing CSVs, [content-preview.md](references/content-preview.md) before content work, and [execution-contract.md](references/execution-contract.md) before any service operation. Read [scenarios.md](references/scenarios.md) for expected conversation and recovery behavior.

## Execute

1. Find the shared “Engage Workshop” assets and the participant's personal TAIS Workfolder. Copy inputs into that folder without modifying shared originals. Keep the TAIS Workfolder distinct from the Engage workspace. Automatically reuse/create the personal folder only through available documented capabilities; otherwise give the exact manual step and continue independent preparation. Do not save only to a local temporary folder.
2. Load host configuration using `assets/workshop-config.example.json` as the schema, not as production configuration. Resolve the participant's intended Engage workspace unambiguously. Preserve explicit campaign/template/audience names. Default campaign name: `Agentic World Engage Workshop.firstname.lastname`.
3. Collect missing identity together, then use `scripts/prepare_audience.py` to create/update a reusable 30-sample-plus-participant CSV. Reuse existing sample rows; upsert the participant by email; preserve unrelated fields. Save the result into the personal Workfolder and show “Your audience is ready: [actual count] profiles. Your fictional profile is overdue for a home refresh.”
4. Select eligible recipients into a separate campaign audience. Keep the full CSV reusable. Apply the overdue, active, email-consent and verified delivery-address rules in the profile contract. Never claim all CSV profiles will be sent merely because they were imported.
5. Prepare the required runtime backstage; reuse installed `tdx` if exactly `2026.9.3`. Otherwise prepare the pinned runner and verify it. Follow the execution contract using locally documented commands and authenticated context. Reconcile prior objects before creating new ones.
6. Create the CSV List one-off campaign and import the eligible audience with all attributes. Map `email_address` as recipient email using the actual API contract. Do not create manual output mappings when all CSV columns are used automatically. Verify that each referenced `profile.*` field reaches personalization.
7. Use `assets/northstar-email.html` and `assets/northstar.css`; preserve structure, IDs, images, three product cards, and unsubscribe. Personalize subject and greeting with `{{profile.first_name}}`. Keep system tags in their own namespace. Finalize links and sender from host configuration. Inline email CSS with an available trusted inliner; preserve supported responsive rules. Keep HTML and plain text consistent.
8. Generate a resolved participant HTML preview and a concise audience/sender/settings summary in TAIS. Prefer native HTML preview capabilities, otherwise a Workfolder HTML artifact plus an in-conversation summary. Use the same saved HTML/subject/recipient values as the campaign. Distinguish preview simulation from server validation. Display “Ready to launch” only after all gates pass.
9. After launch authorization, check the preview fingerprint still matches current audience, content, sender and campaign settings. Re-preview if changed. Start the existing campaign once; persist operation identifiers. On an ambiguous response, query status before retrying. Never automatically repeat a send.
10. Show actual recipient count and service status. Say submitted/processing/delivered only when supported by that evidence. Invite the participant to check their inbox; do not claim inbox arrival or engagement without evidence.

## Completion

Report campaign name, audience count, participant personalization, offer, sender, and the personal Workfolder artifacts. On blocked setup, retain the CSV and preview and state the exact unresolved prerequisite. Never fabricate API calls, object IDs, credentials, destination URLs, product ID mappings, or successful delivery.
