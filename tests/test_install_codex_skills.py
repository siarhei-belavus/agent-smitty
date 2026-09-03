#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "bin" / "install-codex-skills"


class InstallCodexSkillsTest(unittest.TestCase):
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
            self.assertTrue(
                (
                    target
                    / "coordinate-delivery"
                    / ".."
                    / "federated-workflow"
                    / "WORK-TRACKER-CONTEXT-ASSEMBLY.md"
                ).is_file()
            )
            self.assertTrue((target / "implement" / "SKILL.md").is_file())
            self.assertTrue((target / "writing-for-agents" / "SKILL.md").is_file())
            self.assertIn("Installed 39 Codex skill links", result.stdout)

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


if __name__ == "__main__":
    unittest.main()
