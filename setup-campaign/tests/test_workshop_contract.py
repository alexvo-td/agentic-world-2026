"""Local CSV helper and Skill contract tests. Never execute TD queries or sends."""

import importlib.util
import json
import os
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("csv_to_tdx_sql", ROOT / "scripts/csv_to_tdx_sql.py")
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class CsvHelperTests(unittest.TestCase):
    def read(self, text, max_rows=10):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(text, encoding="utf-8")
            return HELPER.read_csv(path, 4096, max_rows)

    def test_participant_profile_and_names(self):
        headers, rows, blank = self.read("email,first_name,last_name\ndemo@example.test,Sample,Person\n")
        HELPER.validate_key(headers, rows, "email")
        self.assertEqual(headers, ["email", "first_name", "last_name"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(blank, 0)

    def test_synthetic_preview_allows_two_rows(self):
        headers, rows, _ = self.read("email,first_name\na@example.test,A\nb@example.test,B\n")
        HELPER.validate_key(headers, rows, "email")
        self.assertEqual(len(rows), 2)

    def test_duplicate_email_case_is_rejected(self):
        headers, rows, _ = self.read("email\nA@example.test\na@example.test\n")
        with self.assertRaises(SystemExit):
            HELPER.validate_key(headers, rows, "email")

    def test_malformed_email_is_rejected(self):
        with self.assertRaises(SystemExit):
            HELPER.validate_key(["email"], [["not-an-address"]], "email")

    def test_missing_email_header_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.read("first_name\nSample\n")

    def test_row_limit_is_enforced(self):
        with self.assertRaises(SystemExit):
            self.read("email\na@example.test\nb@example.test\n", max_rows=1)

    def test_mismatched_columns_are_rejected(self):
        with self.assertRaises(SystemExit):
            self.read("email,first_name\na@example.test\n")

    def test_ignored_blank_rows_are_reported(self):
        _, rows, blank = self.read("email\na@example.test\n\n")
        self.assertEqual(len(rows), 1)
        self.assertEqual(blank, 1)
        # The Skill must obtain a source correction or exclusion decision for skipped rows.
        self.assertIn("ignored_blank_rows", (ROOT / "SKILL.md").read_text(encoding="utf-8"))

    def test_sql_escaping_and_blank_policy(self):
        self.assertEqual(HELPER.sql_string("O'Example"), "'O''Example'")
        self.assertEqual(HELPER.sql_value("", "null"), "NULL")
        self.assertEqual(HELPER.sql_value("", "empty"), "''")

    def test_multiline_and_nul_are_rejected(self):
        for value in ("line\nline", "line\rline", "nul\x00value"):
            with self.subTest(value=repr(value)), self.assertRaises(SystemExit):
                HELPER.sql_string(value)

    def test_private_sql_file_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            path = HELPER.write_private_file(Path(directory), "query.sql", "SELECT 1;\n")
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                HELPER.write_private_file(Path(directory), "query.sql", "SELECT 2;\n")


class InfoPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.language = None
        self.csp = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "meta" and attrs.get("http-equiv") == "Content-Security-Policy":
            self.csp = attrs.get("content")

    def handle_data(self, data):
        self.text.append(data)


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campaign = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.intake = (ROOT.parent / "agenticworld-profile-csv-intake/SKILL.md").read_text(encoding="utf-8")

    def test_exact_version_and_runner_handoff_belong_to_intake(self):
        self.assertIn("tdx --version", self.intake)
        self.assertIn("reports exactly `2026.9.3`", self.intake)
        npx_runner = "npx --yes --package=@treasuredata/tdx@2026.9.3 tdx"
        self.assertIn(f"{npx_runner} --version", self.intake)
        self.assertIn(npx_runner, self.intake)
        self.assertIn("exact runner command from the handoff", self.campaign)
        self.assertIn("<verified-tdx-command>", self.campaign)
        self.assertNotIn("2026.9.2", self.campaign)
        marketplace = (ROOT.parent / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        self.assertIn("exact tdx 2026.9.3", marketplace)
        self.assertNotIn("2026.9.2", marketplace)

    def test_final_approval_has_noninteractive_launch_commands(self):
        lines = [line for line in self.campaign.splitlines() if line.startswith("<verified-tdx-command>") and " campaign launch " in line]
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].endswith("--dry-run"))
        self.assertTrue(lines[1].endswith("--yes"))
        contract = (ROOT / "references/api-contract.md").read_text(encoding="utf-8").lower()
        self.assertIn("final confirmation", contract)
        self.assertIn("launch `--yes` sends only after one fresh final confirmation", contract)
        self.assertIn("exact approved recipient set and count", self.campaign)
        self.assertIn("Show full addresses only in an allowed private review", self.campaign)
        self.assertIn("Confirmation required but running in non-interactive mode", self.campaign)

    def test_no_fixed_draft_only_boundary(self):
        documents = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "operator-checklist.md", ROOT / "references/api-contract.md", ROOT / "references/template-and-merge-tags.md"]
        forbidden = r"never launches or sends|This Skill never launches|draft is the terminal outcome|This workshop stops before live launch"
        for path in documents:
            with self.subTest(path=path.name):
                self.assertIsNone(re.search(forbidden, path.read_text(encoding="utf-8"), re.I))

    def test_changed_content_and_recipient_binding_are_documented(self):
        self.assertIn("fingerprint", self.campaign.lower())
        self.assertIn("approval", self.campaign.lower())
        self.assertIn("retry", self.campaign.lower())
        contract = (ROOT / "references/api-contract.md").read_text(encoding="utf-8")
        self.assertIn("HMAC-SHA256", contract)

    def test_performance_reporting_is_excluded(self):
        self.assertIn("Performance reporting is excluded", self.campaign)
        for path in (ROOT / "SKILL.md", ROOT / "README.md", ROOT / "operator-checklist.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("references/reporting.md", text)
            self.assertNotIn("campaign_performance_report.py", text)

    def test_generated_campaign_id_is_carried_through_workflow(self):
        self.assertIn("exact campaign ID returned", self.campaign)
        self.assertIn("same generated campaign ID", self.campaign)
        self.assertIn("Do not select the newest campaign", self.campaign)

    def test_distribution_docs_are_english(self):
        files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "operator-checklist.md",
                 ROOT / "references/api-contract.md", ROOT / "references/template-and-merge-tags.md",
                 ROOT / "csv-list-generator.html", ROOT.parent / "agenticworld-profile-csv-intake/SKILL.md",
                 ROOT.parent / "agenticworld-profile-csv-intake/README.md"]
        for path in files:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertFalse(any(0x3040 <= ord(char) <= 0x30FF or 0x3400 <= ord(char) <= 0x9FFF for char in text))

    def test_english_guide_has_no_collection_or_send_controls(self):
        parser = InfoPage()
        parser.feed((ROOT / "csv-list-generator.html").read_text(encoding="utf-8"))
        self.assertEqual(parser.language, "en")
        self.assertIn("script-src 'none'", parser.csp)
        self.assertTrue(set(parser.tags).isdisjoint({"script", "form", "input", "button", "iframe"}))
        self.assertIn("send", "".join(parser.text).lower())

    def test_markdown_fences_and_skill_names(self):
        for path in [ROOT / "SKILL.md", ROOT.parent / "agenticworld-profile-csv-intake/SKILL.md", ROOT / "references/api-contract.md", ROOT / "references/template-and-merge-tags.md"]:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertEqual(sum(line.startswith("```") for line in text.splitlines()) % 2, 0)
                if path.name == "SKILL.md":
                    expected_name = "setup-campaign\n" if path == ROOT / "SKILL.md" else "agenticworld-profile-csv-intake\n"
                    self.assertTrue(text.startswith(f"---\nname: {expected_name}"))
                    self.assertLessEqual(len(text.splitlines()), 500)

    def test_intake_asks_for_missing_values_in_one_regular_message(self):
        self.assertIn("ask for all and only those values together in one ordinary chat message", self.intake)
        self.assertIn("If all required values are already available, do not ask again", self.intake)
        self.assertIn("Do not use `AskUserQuestion`", self.intake)
        self.assertIn("or a form", self.intake)
        self.assertNotIn("AskUserQuestion` / Question interface", self.intake)

    def test_campaign_skill_name_matches_marketplace_registration(self):
        manifest = json.loads((ROOT.parent / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        entries = [plugin for plugin in manifest["plugins"] if plugin["name"] == "setup-campaign"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["skills"], ["./setup-campaign"])
        self.assertTrue((ROOT / "SKILL.md").read_text(encoding="utf-8").startswith("---\nname: setup-campaign\n"))

    def test_canonical_intake_skill_name_is_used(self):
        marketplace = (ROOT.parent / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        self.assertIn("agenticworld-profile-csv-intake", self.campaign)
        self.assertIn("agenticworld-profile-csv-intake", marketplace)
        self.assertNotIn("motion1-profile-csv-intake", self.campaign)
        self.assertNotIn("motion1-profile-csv-intake", marketplace)

    def test_merge_tag_is_consistent(self):
        documents = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "operator-checklist.md",
            ROOT / "references/api-contract.md",
            ROOT / "references/template-and-merge-tags.md",
        ]
        for path in documents:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("{{ profile.first_name }}", text)
                if path.name == "template-and-merge-tags.md":
                    self.assertIn("Do not use the conflicting `{{ first_name }}` syntax", text)
                else:
                    self.assertNotIn("{{ first_name }}", text)

    def test_default_recipient_scope_is_one_plus_thirty_send_targets(self):
        documents = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "operator-checklist.md",
            ROOT / "references/api-contract.md",
            ROOT / "references/template-and-merge-tags.md",
            ROOT / "csv-list-generator.html",
            ROOT.parent / "agenticworld-profile-csv-intake/SKILL.md",
        ]
        for path in documents:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8").lower()
                self.assertIn("30", text)
        intake = (ROOT.parent / "agenticworld-profile-csv-intake/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("one participant profile plus exactly 30", intake)
        self.assertIn("actual workshop send targets", intake)
        self.assertIn("one participant-provided address plus 30 approved test recipients", self.campaign)
        self.assertIn("part of the actual send target", (ROOT / "references/api-contract.md").read_text(encoding="utf-8"))
        self.assertIn("example.test", self.campaign)

    def test_setup_and_draft_have_no_separate_chat_approval(self):
        for text in (self.campaign, (ROOT / "README.md").read_text(encoding="utf-8"),
                     (ROOT / "operator-checklist.md").read_text(encoding="utf-8")):
            self.assertIn("without separate", text.lower())
        self.assertIn("one final confirmation", self.campaign.lower())
        self.assertNotIn("self-send opt-in", self.campaign.lower())

    def test_northstar_send_conditions_and_unverified_content_boundary(self):
        self.assertIn("fictional workshop brand", self.campaign.lower())
        self.assertIn("draft-only", self.campaign.lower())
        self.assertIn("unverified benchmark/mock content", self.campaign.lower())
        self.assertIn("Any unverified benchmark/mock content", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_unused_sample_directories_are_not_bundled(self):
        self.assertFalse((ROOT / "campaigns").exists())
        self.assertFalse((ROOT / "samples").exists())

    def test_documents_do_not_claim_preview_fixtures_are_sendable(self):
        references = (ROOT / "references/template-and-merge-tags.md").read_text(encoding="utf-8").lower()
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("example.test", references)
        self.assertIn("preview-only", references)
        self.assertIn("example.test", readme)
        self.assertIn("preview-only", readme)


if __name__ == "__main__":
    unittest.main()
