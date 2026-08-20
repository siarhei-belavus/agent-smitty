from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = SKILL_ROOT / "SKILL.md"
LIFECYCLE = SKILL_ROOT / "LIFECYCLE.md"
ARTIFACTS = SKILL_ROOT / "ARTIFACTS.md"
REPLAY = SKILL_ROOT / "scripts" / "replay_lifecycle.py"
FIXTURES = Path(__file__).parent / "fixtures"


class SkillContractTests(unittest.TestCase):
    def test_skill_is_user_invoked_and_progressively_discloses_live_branches(self) -> None:
        text = SKILL.read_text()

        self.assertRegex(text, r"(?m)^name: coordinate-delivery$")
        self.assertRegex(text, r"(?m)^disable-model-invocation: true$")
        self.assertIn("[durable lifecycle](LIFECYCLE.md)", text)
        self.assertIn("[artifact contracts](ARTIFACTS.md)", text)
        self.assertLessEqual(len(text.splitlines()), 145)
        self.assertEqual(8, len(re.findall(r"(?m)^## [1-8]\. ", text)))
        self.assertEqual(8, text.count("**Complete when:**"))

    def test_lifecycle_reference_owns_every_resume_gate_branch(self) -> None:
        text = LIFECYCLE.read_text()
        required_headings = (
            "## Reconstruct durable state",
            "## Establish a human boundary",
            "## Apply the Resume Gate",
            "## Invalidate evidence by influence",
            "## Recover handoff only",
            "## Replay the contract",
        )
        for heading in required_headings:
            self.assertIn(heading, text)
        for phrase in (
            "Execution Checkpoint plus a completed Human Response",
            "actionable Review Feedback after a completed review round",
            "runtime-proven termination plus a reconstructed Execution Checkpoint",
            "continue",
            "replan",
            "Resumption Record",
            "Validation Indeterminacy",
            "local-only",
        ):
            self.assertIn(phrase, text)

    def test_artifact_reference_defines_complete_durable_records(self) -> None:
        text = ARTIFACTS.read_text()
        required_headings = (
            "## Execution Checkpoint",
            "## Human Action Request",
            "## Human Response",
            "## Resumption Plan",
            "## Resumption Record",
        )
        for heading in required_headings:
            self.assertIn(heading, text)
        for phrase in (
            "exact Published Delivery Heads",
            "affected and preserved Repository Deliveries",
            "next permissible step",
            "reproducible steps",
            "pass/fail criteria",
            "accountable owner",
            "free-form",
            "invalidated evidence",
        ):
            self.assertIn(phrase, text)

    def test_changed_skill_links_resolve_and_vocabulary_is_current(self) -> None:
        deprecated = (
            "Continuation Checkpoint",
            "Recovery Checkpoint",
            "Escalation Record",
            "Human Resolution",
        )
        for path in (SKILL, LIFECYCLE, ARTIFACTS):
            text = path.read_text()
            for target in re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
                if "://" not in target:
                    self.assertTrue((path.parent / target).resolve().exists(), target)
            for phrase in deprecated:
                self.assertNotIn(phrase, text)

    def test_fixture_catalog_covers_the_public_lifecycle(self) -> None:
        required = {
            "environment-blocker-continue",
            "planned-verification-indeterminate",
            "unresolved-active-request",
            "contradictory-active-requests",
            "superseded-without-successor",
            "response-replan",
            "response-replan-without-plan",
            "actionable-review-feedback",
            "runtime-proven-termination",
            "mixed-resume-sources",
            "fresh-initial-attempt",
            "exact-head-drift",
            "local-only-dirty-work",
            "handoff-only-recovery",
            "indeterminate-runtime-liveness",
        }
        fixtures = [json.loads(path.read_text()) for path in FIXTURES.glob("*.json")]
        fixture_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(len(fixture_ids), len(set(fixture_ids)))
        self.assertEqual(required, set(fixture_ids))
        for fixture in fixtures:
            result = subprocess.run(
                [sys.executable, str(REPLAY), str(FIXTURES / f"{fixture['id']}.json")],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            observed = json.loads(result.stdout)
            self.assertLessEqual(1 if observed["active_request_id"] else 0, 1)
            if observed["result"] == "human-boundary":
                self.assertIsNone(observed["attempt_id"])
            if observed["source"] == "runtime-termination":
                self.assertEqual("continue", observed["disposition"])
            if observed["result"] == "resume":
                self.assertEqual(observed["resumption_record_id"], observed["event_order"][0])
                self.assertEqual(observed["attempt_id"], observed["event_order"][1])


if __name__ == "__main__":
    unittest.main()
