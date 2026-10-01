# Motion 1 — Prepare your profile

Create a profile CSV for a personalized workshop email. Share your email, first name, last name, and only the additional details the email needs

## Your journey

1. Choose a real email to yourself or a fictional preview
2. Share the name and details you want personalized
3. Review the fields, row count, and approved save location
4. Approve a new CSV file and continue to email creation

Saving the CSV does not send an email. The campaign Skill shows the completed message and waits for a separate final send approval

## Operator notes

- Confirm chat collection/retention, Work Folder access, and downstream TD query/job-history exposure before real data intake
- The default sendable file contains one participant-owned, opted-in address plus 30 approved test recipients. `example.test` profiles are preview-only; simulator recipients do not provide a human inbox
- Preserve original sample files and save a new version. Do not mix other participants or fictional rows into the live self-send list
- Before campaign setup, verify the existing tdx version is `2026.9.3`; do not reinstall a correct runtime or install globally
- Do not query TD, prepare SQL, create tables/campaigns, or send here. Pass only a saved path and non-PII metadata to `motion1-csv-list-campaign`
- Keep participant-facing content in English and technical choices backstage

## Installation

Install both sibling Skills at the same revision in the approved runtime's Skill location. `private/toru/` is distribution source, not an automatically installed Skill folder. Preserve relative paths and exclude real profiles and credentials

💎 Generated with [Treasure Work](https://github.com/treasure-work)
