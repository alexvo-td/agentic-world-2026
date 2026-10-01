# Motion 1 — Create your email and receive it

Turn your reviewed profile CSV and chosen template into a personalized workshop email. Let AI Studio handle the setup; review the message and approve sending it to yourself

## Try this prompt

> “In Agentic World Workspace, create a one-off campaign named Agentic World Engage Workshop.firstname.lastname using [template] and [CSV]. Show me the preview, then send it to me after I approve.”

If your CSV is not ready, begin with `agenticworld-profile-csv-intake`. You do not need to repeat answers already collected

## Participant journey

| Step | What you do |
|---|---|
| Profile | Share your name, email, and needed personalization |
| Create email | Choose a template, campaign name, and message |
| Preview | Review content, personalization, recipient, and sender |
| Approve and send | Approve the exact one-time send to your own address |
| Confirm launch status | See the actual campaign state and check your inbox |

After verified final approval, the Skill launches the campaign itself. It does not impose a blanket demo-send refusal or ask participants to use a terminal. Changes to content or recipients require a new preview and approval

## Behind the scenes

- CSV Intake prepares tdx `2026.9.2`; the campaign Skill reuses that cached version without installing/updating it
- ListCampaign uses a staged contact-list table, not direct CSV upload or a CDP Audience/segment
- The Skill validates the file, maps actual table columns, checks supported merge tags, and verifies workspace/template/sender with existing authentication
- CREATE SCHEMA, CREATE TABLE, INSERT, DRAFT push, and final delivery have separate approvals
- Push/launch dry-runs do not render email, count eligible recipients, or prove consent. Verify those separately
- Non-TTY execution uses the CLI's final `--yes` only after the corresponding human approval. Application execution approval and permissions remain enforced
- The exact ID returned by campaign creation is carried through preview, launch, and status read-back. Never guess the latest campaign
- Freeze the run-only recipient table and bind content/row-set fingerprints to final approval. Stop if write exclusion cannot be established

## Package files

- `SKILL.md` — participant workflow and approval-gated launch
- `operator-checklist.md` — environment, write, preview, send, and read-back checks
- `references/api-contract.md` — verified CLI contract and readiness ledger
- `references/template-and-merge-tags.md` — mappings, personalization, and preview rules
- `scripts/csv_to_tdx_sql.py` — local CSV validation/private SQL preparation; no execution
- `tests/test_workshop_contract.py` — offline helper and documentation-contract tests
- `csv-list-generator.html` — English participant guide; not a data-entry or send form
- `campaigns/` and `samples/` — non-sendable reference content and synthetic fixtures

Environment-bound campaign/template YAML, credentials, real profiles, generated INSERT SQL, and the old static campaign review are not part of the PR distribution

## Environment and fixtures

Default to Agentic World Workspace, but verify the actual account/workspace and sender IDs. Do not reuse the older `Agentic World CSV Demo fac377ba` environment by guess. Confirm each CTA instead of automatically using a landing-page host

Northstar content is an internal benchmark mock with third-party prices, unresolved image access, no CTA destination, a postal-address placeholder, and unverified ListCampaign unsubscribe rendering. Do not push or send it as-is. `example.test` recipients are not deliverable

## Current scope and validation

Performance reporting is deferred and excluded from this PR. Do not run delivery/open/click KPI queries or generate a performance dashboard in this workflow. Campaign state is not proof of inbox delivery

Install both Skills at the same revision and preserve relative paths. Local helper/schema/contract tests do not establish a successful live AI Studio send or renderer compatibility. Record those only after a separately approved real walkthrough

💎 Generated with [Treasure Work](https://github.com/treasure-work)
