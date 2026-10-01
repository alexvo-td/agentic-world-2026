# ListCampaign — Content, personalization, and preview

Assistant/operator reference. Ask participants intuitive campaign-content questions only when an answer is actually missing. Reuse profile values already provided during intake; do not repeat the profile-collection questions.

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

Verify actual columns/types with `<verified-tdx-command> describe`. Auto-map only exact unambiguous matches such as `email`, `first_name`, and `last_name`; CSV headers alone do not establish the table schema. Ask about adding a missing field or proceeding without its personalization.

Use the profile-prefixed token `{{ profile.first_name }}` for the mapped first name, and `{{ profile.<attribute_name> }}` for other verified attributes. Keep CSV headers and source mapping keys unprefixed, e.g. `first_name`. Do not use the conflicting `{{ first_name }}` syntax. Verify rendering and blank behavior in the selected ListCampaign renderer before delivery. If a required token/fallback cannot be verified, correct the data or remove that personalization before sending.

## Template and companion HTML

- Use ListCampaign `type`, `contact_list`, `source_columns`, and `email` blocks
- Resolve `email.template` as `ref:` to an existing template in the selected workspace
- Put `email.html_file` inside the YAML folder. Compare actual persisted content and supported preview to confirm what renders
- Do not alter or push a shared template without approval. Do not add standard campaign audience/segment/connector fields
- Obtain `email.sender_id` from the workspace's actual sender list; never infer it from an address or URL
- Reject path traversal and symlink escapes

## Sender and delivery content

Use the approved sender and verify its unsubscribe mechanism in ListCampaign. A standard template's `{{sender.unsubscribe_url}}` is not proof that the ListCampaign renderer supports it. Do not claim unsubscribe rendering is verified until tested with the actual renderer.

Use the account owner's approved postal address. Never invent CTA URLs, prices, offers, dates, purchase history, or asset approval. Email images need approved HTTPS URLs accessible to recipients; do not use local paths or unapproved assets.

The fictional Northstar Home & Living brand may be used for a workshop email when all delivery requirements are verified. Any unverified benchmark-price mock or supplied assets are draft-only: do not copy unverified claims, URLs, images, CTA, postal address, or unsubscribe behavior into a live campaign without validation and approval. `example.test` recipients are preview-only and not eligible delivery targets.

## Distinguish the checks

| Check | Establishes | Does not establish |
|---|---|---|
| Local validate | YAML schema | Recipient eligibility, real rendering, delivery |
| Push/launch dry-run | Planned changes or resource/source references | Counts, content render, consent, delivery |
| Content preview | Display through the chosen renderer | Local substitution does not prove Engage rendering or actual arrival |

Use a compatible ListCampaign preview if available. Do not assume `preview_engage_campaign` or `campaign readiness` compatibility.

A local snapshot must be labeled **static content preview** and compared with the exact saved campaign HTML. Do not label manual token substitution or a mock as a live Engage preview. Stop before launch if required sender/merge-tag/unsubscribe behavior cannot be independently verified.

## Final review

- Subject/body, personalization, and blank-value handling
- Sender, CTA/link, asset access, unsubscribe, and approved postal address
- Workspace, exact generated ID/version, content hash, mapping, template/sender IDs
- Exact match between the full reviewed CSV and frozen table, with one participant address plus 30 approved test-recipient destinations for the default 31-row workshop send; `example.test` is preview-only

Show the exact preview, sender, actual recipient composition/count, and “send now” action. Full addresses belong only in an allowed private review, never a shared HTML artifact. Bind the single final send confirmation to that review; changes invalidate it. Do not ask separate conversational approvals for CSV saving, SQL/setup, or DRAFT saving.

After the final confirmation, verify the same target and launch once with the same verified tdx runner. Non-TTY CLI `--yes` is allowed only after the human's exact final send confirmation; application approval and runtime permissions remain enforced. See `api-contract.md` for commands and read-back.

Any unverified claims, CTA destination, image authorization/access, postal address, or unsubscribe behavior keep content draft-only. Never reuse historical static-sample counts or state as facts for a new run.

💎 Generated with [Treasure Work](https://github.com/treasure-work)
