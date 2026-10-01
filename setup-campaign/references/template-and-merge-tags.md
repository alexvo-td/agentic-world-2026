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

## Create a new template when selected

Create a template only when the participant explicitly selects **Create new**. Ask for the new template name, subject, complete message copy, approved assets/CTA, and required personalization. Do not invent offers, prices, URLs, or claims. Write a `type: template` YAML plus companion HTML using the selected workspace and `editor_type: grapesjs`; define variables for each supported merge tag. Use the verified runner to validate, push a dry-run, preview with a supported renderer, and then save the new template. Re-list/read back the template by name before using it in ListCampaign.

Verify that the saved template's variable/merge-tag behavior is compatible with ListCampaign mapping and the `{{ profile.<attribute_name> }}` tokens in this Skill. If compatibility or preview cannot be verified, stop before campaign delivery. A user-selected new template authorizes creating that new resource under setup scope; it does not authorize sending.

No generic workspace-creation or sender-creation procedure is defined here. If a user selects **Create new** for either and no documented supported operation is available, report the operator provisioning step and do not guess API paths, IDs, or commands.

## Sender and delivery content

Use the approved sender and verify its unsubscribe mechanism in ListCampaign. A standard template's `{{sender.unsubscribe_url}}` is not proof that the ListCampaign renderer supports it. Do not claim unsubscribe rendering is verified until tested with the actual renderer.

A postal address is not required for a workshop demo limited to the participant and approved test recipients; remove any postal-address placeholder rather than inventing an address. For production sends to real customer recipients, use the account owner's approved postal address. Never invent CTA URLs, prices, offers, dates, purchase history, or asset approval. Email images need approved HTTPS URLs accessible to recipients; do not use local paths or unapproved assets.

The fictional Northstar Home & Living brand may be used for a workshop email when required delivery details are verified. Any unverified benchmark-price mock or supplied assets are draft-only: do not copy unverified claims, URLs, images, CTA, or unsubscribe behavior into a live campaign without validation and approval. Remove postal-address placeholders; an address is not required for a workshop demo limited to the participant and approved test recipients. `example.test` recipients are preview-only and not eligible delivery targets.

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
- Sender, CTA/link, asset access, and unsubscribe; require an approved postal address only for production sends to real customer recipients
- Workspace, exact generated ID/version, content hash, mapping, template/sender IDs
- Exact match between the full reviewed CSV and frozen table, with one participant address plus 30 approved test-recipient destinations for the default 31-row workshop send; `example.test` is preview-only

Show one consolidated settings report (account/workspace/database, template, sender, runner/version, and recipient composition), the exact preview, actual recipient set/count, and “send now” action. Full addresses belong only in an allowed private review, never a shared HTML artifact. Bind the single final send confirmation to that report and preview; changes invalidate it. Do not ask separate conversational approvals for discovery commands, settings alone, CSV saving, SQL/setup, or DRAFT saving.

After the final confirmation, verify the same target and launch once with the same verified tdx runner. Non-TTY CLI `--yes` is allowed only after the human's exact final send confirmation; application approval and runtime permissions remain enforced. See `api-contract.md` for commands and read-back.

Any unverified claims, CTA destination, image authorization/access, or unsubscribe behavior keep content draft-only. For production to real customer recipients, an unverified postal address also blocks sending; it is not required for the workshop demo. Never reuse historical static-sample counts or state as facts for a new run.

💎 Generated with [Treasure Work](https://github.com/treasure-work)
