# Motion 1 — Create your email and receive it

Turn your reviewed profile CSV and chosen template into a personalized workshop email. AI Studio handles setup, asks only about unresolved creative choices, shows the exact preview and full workshop recipient set, and asks once for final send confirmation.

## Try this prompt

> “In Agentic World Workspace, create a one-off campaign named Agentic World Engage Workshop.firstname.lastname using [template] and [CSV]. Show me the exact preview and workshop recipient list, then ask once before sending.”

If your CSV is not ready, begin with `agenticworld-profile-csv-intake`. It reuses information already collected and asks all missing required profile details together in one ordinary message. It skips the question when the required values are already present.

## Participant journey

| Step | What happens |
|---|---|
| Profile | Reuse details already supplied; ask once for missing required fields only |
| Create email | Choose a template, campaign name, and any unresolved message choices |
| Preview | Review the exact content, personalization, sender, and actual recipient composition |
| Approve and send | Confirm the one-time send to the participant plus 30 approved test destinations by default |
| Confirm launch status | See the actual campaign state and check the participant inbox if applicable |

The workshop send target is one participant-provided address plus 30 approved test-recipient addresses (31 total). Test addresses are included in the delivery target; they are not extra participants. `example.test` fixtures are preview-only. After the exact preview and target list are shown, one final confirmation is required. The Skill launches only that unchanged campaign once.

## Behind the scenes

- Reuse installed tdx only when it reports exactly `2026.9.3` in the campaign runtime. If missing or mismatched, intake prepares and verifies `@treasuredata/tdx@2026.9.3` with npx, then passes the exact same runner command to this Skill
- ListCampaign uses a staged contact-list table, not direct CSV upload or a CDP Audience/segment
- The Skill batches read-only account/workspace/template/sender discovery under campaign setup authorization, then reports the collected settings once in the final review; it validates the file, maps actual table columns, and personalizes with `{{ profile.first_name }}`
- An authorized campaign request covers necessary setup, CSV loading, SQL execution, DRAFT save, previews, and read-back without separate conversational approvals
- Push/launch dry-runs do not render email, count eligible recipients, or prove consent. Verify those separately
- Non-TTY execution uses CLI `--yes` for already authorized operations; the final settings report, exact preview, and recipient set are covered by one send confirmation. Runtime approval and permissions remain enforced
- The exact ID returned by campaign creation is carried through preview, launch, and status read-back. Never guess the latest campaign
- Freeze the run-only recipient table and bind content/row-set fingerprints to final approval. Stop if write exclusion cannot be established

## Package files

- `SKILL.md` — participant workflow and preview-confirmed launch
- `operator-checklist.md` — environment, write, preview, send, and read-back checks
- `references/api-contract.md` — verified CLI contract and readiness ledger
- `references/template-and-merge-tags.md` — mappings, personalization, and preview rules
- `scripts/csv_to_tdx_sql.py` — local CSV validation/private SQL preparation; no execution
- `tests/test_workshop_contract.py` — offline helper and documentation-contract tests
- `csv-list-generator.html` — English static participant guide; not a data-entry or send form
- No legacy campaign HTML, local campaign images, or sample CSV data are bundled

Environment-bound campaign/template YAML, credentials, real profiles, generated INSERT SQL, and the old static campaign review are not part of the PR distribution.

## Environment and content

Default to Agentic World Workspace, but verify the actual account/workspace and sender IDs. Never assume environment-bound IDs or reuse unverified sample values. Confirm each CTA instead of automatically using a landing-page host.

Northstar Home & Living is a fictional workshop brand, not a reason by itself to block sending. A workshop demo to the participant and approved test recipients does not require a postal address; remove any postal-address placeholder rather than inventing one. Production sends to real customer recipients require the approved address. Verify CTA behavior, asset authorization/access, sender, and unsubscribe behavior. Any unverified benchmark/mock content or assets supplied for a run remain draft-only; do not invent missing values. `example.test` recipients are not deliverable. No campaign or CSV example data is bundled.

## Current scope and validation

Performance reporting is deferred and excluded from this PR. Do not run delivery/open/click KPI queries or generate a performance dashboard in this workflow. Campaign state is not proof of inbox delivery.

Install both Skills at the same revision and preserve relative paths. Local helper/schema/contract tests do not establish a successful live AI Studio send, renderer compatibility, or delivery eligibility. Report live behavior only after observing it in an actual workshop run.

💎 Generated with [Treasure Work](https://github.com/treasure-work)
