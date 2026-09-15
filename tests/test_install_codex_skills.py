#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "bin" / "install-codex-skills"


class InstallCodexSkillsTest(unittest.TestCase):
    def run_from_copy(self, skill_text: str) -> subprocess.CompletedProcess[str]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        repository = Path(temporary_directory.name) / "agent-smitty"
        shutil.copytree(ROOT, repository, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        skill_file = repository / "skills" / "engineering" / "coordinate-delivery" / "SKILL.md"
        skill_file.write_text(skill_text, encoding="utf-8")
        return subprocess.run(
            [str(repository / "bin" / "install-codex-skills"), "--target", str(repository / "target")],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_installs_discoverable_links_with_complete_skill_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / ".agents" / "skills"
            result = subprocess.run(
                [str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "coordinate-delivery").is_symlink())
            self.assertTrue((target / "coordinate-delivery" / "SKILL.md").is_file())
            self.assertTrue((target / "coordinate-delivery" / "RECOVERY.md").is_file())
            self.assertTrue((target / "federated-workflow").is_symlink())
            self.assertTrue(
                (
                    target
                    / "federated-workflow"
                    / "WORK-TRACKER-CONTEXT-ASSEMBLY.md"
                ).is_file()
            )
            self.assertTrue((target / "implement" / "SKILL.md").is_file())
            self.assertTrue((target / "writing-for-agents" / "SKILL.md").is_file())
            self.assertTrue((target / "closeout" / "SKILL.md").is_file())
            skill_count = len(list((ROOT / "skills").rglob("SKILL.md")))
            self.assertIn(
                f"Installed {skill_count} Codex skill links and 1 shared resource link",
                result.stdout,
            )

    def test_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "skills"

            first = subprocess.run(
                [str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            second = subprocess.run(
                [str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)

    def test_refuses_to_replace_an_existing_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "skills"
            target.mkdir()
            conflict = target / "coordinate-delivery"
            conflict.write_text("keep me", encoding="utf-8")

            result = subprocess.run(
                [str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Refusing to replace existing paths", result.stderr)
            self.assertEqual(conflict.read_text(encoding="utf-8"), "keep me")

    def test_rejects_name_outside_front_matter(self) -> None:
        result = self.run_from_copy("# Broken skill\n\nname: coordinate-delivery\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("front matter", result.stderr)

    def test_rejects_multiple_names_in_front_matter(self) -> None:
        result = self.run_from_copy(
            "---\nname: coordinate-delivery\nname: another-name\n---\n# Broken skill\n"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("exactly one name", result.stderr)

    def test_rejects_mismatched_name_quotes(self) -> None:
        for invalid_name in ("'coordinate-delivery\"", "\"coordinate-delivery'"):
            with self.subTest(invalid_name=invalid_name):
                result = self.run_from_copy(
                    f"---\nname: {invalid_name}\n---\n# Broken skill\n"
                )

                self.assertEqual(result.returncode, 1)
                self.assertIn("Invalid name", result.stderr)


if __name__ == "__main__":
    unittest.main()
