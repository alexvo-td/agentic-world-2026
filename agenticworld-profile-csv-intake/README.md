# Motion 1 — Prepare your profile

Create a profile CSV for a personalized workshop email. The Skill reuses information you've already shared and, if anything required is missing, asks for all missing details together in one ordinary message.

## Your journey

1. Share your email, name, and only details required by the selected email template
2. If required information is already present, continue without another question; otherwise reply once with the missing details
3. The Skill prepares one participant profile and 30 approved test recipients for the workshop send flow
4. The Skill validates and saves a new CSV in the approved location, then continues to email creation when sending was requested

CSV preparation does not send an email. The campaign Skill previews the exact email and recipient set, then asks once for final confirmation before sending.

## Operator notes

- Confirm chat collection/retention, Work Folder access, and downstream TD query/job-history exposure before real data intake; reuse already approved settings
- The default workshop send list contains one participant-provided address plus 30 approved test destinations (31 total). These test destinations are delivery targets for the workshop flow, not extra participants. `example.test` profiles are preview-only; SES simulator recipients do not provide a human inbox
- Preserve original sample files and save a new version. Do not mix other participants or fictional real-world contact details into the approved test-recipient set
- Before campaign setup, reuse installed `tdx` only if it reports exactly `2026.9.3` in the campaign runtime. Otherwise prepare and verify `@treasuredata/tdx@2026.9.3` with npx; pass the exact verified runner command and runtime to the campaign Skill
- Do not query TD, prepare SQL, create tables/campaigns, or send here. Pass only the saved path and non-PII metadata to `setup-campaign`
- Keep participant-facing content in English and technical choices backstage

## Installation

Install both sibling Skills at the same revision in the approved runtime's Skill location. `private/toru/` is distribution source, not an automatically installed Skill folder. Preserve relative paths and exclude real profiles and credentials

💎 Generated with [Treasure Work](https://github.com/treasure-work)
