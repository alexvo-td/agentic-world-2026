# ListCampaign — Content, personalization, and preview

Assistant/operator reference. Ask participants only intuitive questions such as which name to use or whether to omit a greeting when a field is blank

## Map verified table columns

`source_columns` maps content keys to physical table columns and types. Required email mapping:

```yaml
source_columns:
  - key: email
    sql_name: email
    type: string
  - key: first_name
    sql_name: first_name
    type: string
```

Verify actual columns/types with `tdx describe`. Auto-map only exact unambiguous matches such as `email`, `first_name`, and `last_name`; CSV headers alone do not establish the table schema. Ask about adding a missing field or proceeding without its personalization

The v2026.9.2 example uses `{{ first_name }}`. Do not assume standard CDP `{{profile.first_name}}`, `variables`, or `default_value` behavior transfers. Generate only verified mapped keys. If blank/fallback rendering is unknown, request a correction or remove personalization with approval

## Template and companion HTML

- Use ListCampaign `type`, `contact_list`, `source_columns`, and `email` blocks
- Resolve `email.template` as `ref:` to an existing template in the selected workspace
- Put `email.html_file` inside the YAML folder. Compare actual persisted content and supported preview to confirm what renders
- Do not alter or push a shared template without approval. Do not add standard campaign audience/segment/connector fields
- Obtain `email.sender_id` from the workspace's actual sender list; never infer it from an address or URL
- Reject path traversal and symlink escapes

## Sender and delivery content

Use the approved sender and verify its unsubscribe mechanism in ListCampaign. A standard template's `{{sender.unsubscribe_url}}` is not proof that the ListCampaign renderer supports it

Use the account owner's approved postal address. Never invent CTA URLs, prices, offers, dates, or asset approval. Email images need approved HTTPS URLs accessible to recipients; do not use local paths or unapproved assets

## Distinguish the checks

| Check | Establishes | Does not establish |
|---|---|---|
| Local validate | YAML schema | Recipient eligibility, real rendering, delivery |
| Push/launch dry-run | Planned changes or resource/source references | Counts, content render, consent, delivery |
| Content preview | Display through the chosen renderer | Local substitution does not prove Engage rendering or actual arrival |

Use a compatible ListCampaign preview if available. Do not assume `preview_engage_campaign` or `campaign readiness` compatibility

A local snapshot must be labeled **static content preview** and compared with the exact saved campaign HTML. Do not label manual token substitution or a mock as a live Engage preview. Stop before launch if required sender/merge-tag/unsubscribe behavior cannot be independently verified

## Final review

- Subject/body, personalization, and blank-value handling
- Sender, CTA/link, asset access, unsubscribe, and approved postal address
- Workspace, exact generated ID/version, content hash, mapping, template/sender IDs
- Exact match between the participant-only CSV and frozen one-row table; `example.test` is preview-only

Show the email, sender, one-recipient count, and “send now” action. Full address belongs only in an allowed private review, never a shared HTML artifact. Bind final approval to that review; changes invalidate it

After approval, verify the same target and launch once. Non-TTY CLI `--yes` is allowed only after the human's exact final approval; application approval and permissions remain enforced. See `api-contract.md` for commands and read-back

Keep the Northstar benchmark mock non-sendable. Never reuse historical static-sample counts or state as facts for a new run

💎 Generated with [Treasure Work](https://github.com/treasure-work)
