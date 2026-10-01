# tdx command reference

Source: https://tdx.treasuredata.com/commands/engage.html#campaigns
Checked: 2026-10-01. Confirm installed help automatically before using unsupported flags.

Use an explicit workspace. Regular campaigns are the default; select ListCampaign explicitly.

```bash
tdx engage campaign list --campaign-type list-campaign --workspace "<workspace>"
tdx engage campaign show "<campaign-id>" --campaign-type list-campaign --workspace "<workspace>" --full
tdx engage template list --workspace "<workspace>"
tdx engage template show "<template>" --workspace "<workspace>" --full
tdx engage campaign validate campaign.yaml --campaign-type list-campaign
tdx engage campaign push campaign.yaml --campaign-type list-campaign --workspace "<workspace>" --dry-run
tdx engage campaign push campaign.yaml --campaign-type list-campaign --workspace "<workspace>" --yes
tdx engage campaign launch "<campaign-id>" --campaign-type list-campaign --workspace "<workspace>" --dry-run
```

Validation is local. Push dry-run resolves references; inspect whether it plans creation or an existing-draft update. For new runs require creation, using a unique name. Push saves a draft, not delivery. Readiness checks workspace sender/domain assignments, not every delivery prerequisite.

After participant launch authorization only:

```bash
tdx engage campaign launch "<campaign-id>" --campaign-type list-campaign --workspace "<workspace>" --yes
```

Use `--yes` for authorized draft push; for launch use it only after the reviewed preview and explicit Launch instruction. Never infer launch authorization from technical-command permission.

Sender discovery reported by the participant is not documented on this Engage page. Verify installed delivery help before binding sender commands; do not fabricate workspace-sender relationships.
