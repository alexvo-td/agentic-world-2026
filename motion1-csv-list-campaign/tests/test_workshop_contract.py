"""Local CSV helper and Skill contract tests. Never execute TD queries or sends."""

import importlib.util
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

    def test_version_check_belongs_to_intake(self):
        self.assertIn("tdx --version", self.intake)
        self.assertIn("successful execution reporting exactly `2026.9.3`", self.intake)
        self.assertIn("npx --offline --yes --package=@treasuredata/tdx@2026.9.2", self.campaign)

    def test_final_approval_has_executable_noninteractive_launch(self):
        lines = [line for line in self.campaign.splitlines() if line.startswith("npx ") and " campaign launch " in line]
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].endswith("--dry-run"))
        self.assertTrue(lines[1].endswith("--yes"))
        contract = (ROOT / "references/api-contract.md").read_text(encoding="utf-8").lower()
        self.assertIn("final", contract)
        self.assertIn("approval", contract)
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
                    expected_name = "motion1-" if path == ROOT / "SKILL.md" else "agenticworld-profile-csv-intake\n"
                    self.assertTrue(text.startswith(f"---\nname: {expected_name}"))
                    self.assertLessEqual(len(text.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
