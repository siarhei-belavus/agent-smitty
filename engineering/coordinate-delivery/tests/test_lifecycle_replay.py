from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPLAY = SKILL_ROOT / "scripts" / "replay_lifecycle.py"
FIXTURES = Path(__file__).parent / "fixtures"


class LifecycleReplayTests(unittest.TestCase):
    def replay_fixture(self, fixture: Path) -> dict[str, object]:
        result = subprocess.run(
            [sys.executable, str(REPLAY), str(fixture)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def assert_fixture(self, fixture: Path) -> dict[str, object]:
        specification = json.loads(fixture.read_text())
        observed = self.replay_fixture(fixture)
        for key, expected in specification["expected"].items():
            self.assertEqual(expected, observed[key], key)
        return observed

    def test_environment_blocker_resumes_from_durable_records(self) -> None:
        fixture = FIXTURES / "environment-blocker-continue.json"
        observed = self.assert_fixture(fixture)
        self.assertLess(
            observed["event_order"].index(observed["resumption_record_id"]),
            observed["event_order"].index(observed["attempt_id"]),
        )

    def test_request_lifecycle_fails_closed(self) -> None:
        fixture_names = (
            "planned-verification-indeterminate.json",
            "unresolved-active-request.json",
            "contradictory-active-requests.json",
            "superseded-without-successor.json",
        )
        for fixture_name in fixture_names:
            with self.subTest(fixture=fixture_name):
                fixture = FIXTURES / fixture_name
                self.assert_fixture(fixture)

    def test_resume_gate_accepts_only_settled_sources_and_dispositions(self) -> None:
        fixture_names = (
            "response-replan.json",
            "response-replan-without-plan.json",
            "actionable-review-feedback.json",
            "runtime-proven-termination.json",
            "mixed-resume-sources.json",
            "fresh-initial-attempt.json",
        )
        for fixture_name in fixture_names:
            with self.subTest(fixture=fixture_name):
                fixture = FIXTURES / fixture_name
                self.assert_fixture(fixture)

    def test_recovery_invalidates_only_dependent_evidence(self) -> None:
        fixture_names = (
            "exact-head-drift.json",
            "stale-evidence-bindings.json",
            "local-only-dirty-work.json",
            "handoff-only-recovery.json",
            "indeterminate-runtime-liveness.json",
        )
        for fixture_name in fixture_names:
            with self.subTest(fixture=fixture_name):
                self.assert_fixture(FIXTURES / fixture_name)

    def test_malformed_durable_records_cannot_authorize_an_attempt(self) -> None:
        fixture_names = (
            "duplicate-durable-record-id.json",
            "incomplete-durable-record.json",
            "misbound-runtime-termination.json",
            "mismatched-response-request.json",
            "unbound-runtime-termination.json",
        )
        for fixture_name in fixture_names:
            with self.subTest(fixture=fixture_name):
                self.assert_fixture(FIXTURES / fixture_name)


if __name__ == "__main__":
    unittest.main()
