# CSV List campaign YAML contract

Use the following user-supplied specification as the baseline. Read the selected Engage workspace's existing template and approved sender automatically. Verify every source column against the actual recipient table schema. Auto-map only unambiguous matches; ask for missing business data or give the host a precise technical gap instead of inventing values. Preserve shared templates; create a personal copy. Modifying the shared original requires explicit authorization.

```yaml
type: list_campaign
name: "<participant-confirmed-name>"
contact_list:
  database_name: agentic_world_demo
  table_name: "<verified-recipient-table>"
source_columns:
  - key: email
    sql_name: email
    type: string
  - key: first_name
    sql_name: first_name
    type: string
email:
  template: "ref:<verified-template-name>"
  subject: "<reviewed-subject>"
  html_file: "workshop-email.html"
  sender_id: "<verified-workspace-sender-ID>"
```

## Resolve fields

- Set `type` to `list_campaign`.
- Use the participant-confirmed name. An explicit name in their request is sufficient; otherwise show the proposed name in the business preview, where the Launch instruction accepts the reviewed configuration. Do not add a separate naming approval.
- Verify `agentic_world_demo` and the selected recipient table exist in the authenticated account/region. Do not substitute an unrelated table.
- Use source mapping `key` for the attribute name and `sql_name` for the verified physical column name. Keep CSV headers and mapping keys unprefixed. Verify data types rather than casting speculatively.
- Require a physical recipient-table column named `email`. `source_columns` must include `key: email`, `sql_name: email`, `type: string`. Mapping `sql_name: email_address` does NOT satisfy this contract.
- Keep `email_address` in the reusable profile CSV for cross-exercise compatibility. When producing the campaign recipient import CSV/table, explicitly convert it to a physical `email` column. Verify the table schema after import before creating the campaign. If a supplied table has only `email_address`, prepare a separate recipient table containing `email` through the documented import/query operation; do not silently rewrite a shared source table. If both columns exist, check their values agree for selected rows; report conflicts rather than choosing arbitrarily.
- Use `{{ profile.email }}` for email personalization when only the campaign `email` attribute is mapped. If content needs `{{ profile.email_address }}`, retain that as an additional column/mapped attribute while still keeping the mandatory `email` entry.
- Map `first_name` to its verified table column. Extend `source_columns` with each needed personalization attribute and other required CSV attributes, using documented supported types. Do not fabricate manual output mapping; `source_columns` is the YAML source-attribute contract, not a separate output-mapping approval step.
- Resolve `email.template` as `ref:<verified-template-name>` from the selected workspace, not from an invented filename or cross-workspace template.
- Set subject to the reviewed subject, retaining server merge tags.
- Set `email.html_file` to `workshop-email.html`, stored beside the YAML.
- Use the verified sender ID belonging to the selected workspace.

Use `scripts/prepare_recipient_import.py --input <already-selected-delivery-csv> --output <personal-folder-recipient-import.csv>` for deterministic email-column conversion. It preserves the source, rejects conflicting values, and removes email_address from the import. It does not select recipients; apply strategy/consent/delivery eligibility first. If email_address is required as an additional personalization attribute, retain it in a separately validated import variant with explicit mapping.

## Files and validation

Create `campaign.yaml` and companion `workshop-email.html` in the participant's approved personal folder. Existing user-selected personal folder counts as authorization; do not ask an additional folder approval. Resolve paths before writing and before invocation. Reject absolute companion paths, `..` traversal, and symlink escapes outside that folder. Do not overwrite a shared template. Use a YAML serializer; do not interpolate names/subjects into raw YAML.

Use `{{ profile.first_name }}` and `{{ profile.<attribute_name> }}` for mapped attributes. Whitespace inside braces is permitted; retain `profile.` in both service HTML and static TAIS preview. Resolve previews from the same mapping keys and recipient data, with HTML escaping. Detect missing values and unresolved tokens. For blanks, obtain a correction or explicit approval to remove that personalization; do not invent fallback data or undocumented engine fallbacks. This correction concerns content, not permission to run technical commands.

Never invent offers, CTA URLs, asset authorization, postal addresses, or unsubscribe behavior. Northstar fictional branding is allowed for this workshop. The bundled 20% offer is an explicitly labeled fictional workshop draft default; it does not authorize a real retail offer. Carry only a host/participant-established workshop offer into launch content. Verify asset authorization separately from image reachability. Retain the provided sender unsubscribe tag only under the verified sender/template contract. Placeholder/mock configuration and unresolved content remain draft-only.

Parse YAML and verify required fields, table/source types, template reference, sender ownership, companion-file containment and every merge tag before service validation. Read installed CLI help for the documented YAML create/update operation and invoke it directly as `tdx ...`; this YAML specification does not define an endpoint or CLI subcommand. Never execute the example with angle-bracket placeholders.
