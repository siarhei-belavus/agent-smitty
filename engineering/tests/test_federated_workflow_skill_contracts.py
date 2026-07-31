from __future__ import annotations

import unittest
from pathlib import Path


ENGINEERING_SKILLS = Path(__file__).resolve().parents[1]
IMPLEMENT = ENGINEERING_SKILLS / "implement" / "SKILL.md"
CODE_REVIEW = ENGINEERING_SKILLS / "code-review" / "SKILL.md"


def skill_text(path: Path) -> str:
    return path.read_text()


class ImplementContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_text(IMPLEMENT)

    def test_standalone_assignment_accepts_one_or_many_repository_deliveries(self) -> None:
        self.assertIn("Standalone assignment", self.skill)
        self.assertIn("one or more Repository Deliveries", self.skill)
        self.assertIn("Repository ID", self.skill)
        self.assertIn("Repository Reference", self.skill)
        self.assertIn("Repository Scope", self.skill)

    def test_coordinator_narrowing_is_one_repository_and_one_execution_worktree(self) -> None:
        self.assertIn("Coordinator-narrowed assignment", self.skill)
        self.assertIn("exactly one named Repository Scope entry", self.skill)
        self.assertIn("supplied Execution Worktree", self.skill)
        self.assertIn("Do not start reviewers or any other child agent", self.skill)

    def test_delivery_result_is_bound_to_exact_git_and_validation_evidence(self) -> None:
        for public_field in (
            "Fixed review base",
            "Exact local HEAD",
            "Repository validation",
        ):
            with self.subTest(public_field=public_field):
                self.assertIn(public_field, self.skill)

    def test_narrowed_assignment_never_expands_scope_or_publishes(self) -> None:
        self.assertIn("Material contradiction", self.skill)
        self.assertIn("change only that execution worktree", self.skill.lower())
        self.assertIn("Do not publish a branch", self.skill)
        self.assertIn("Do not create or update a Review Proposal", self.skill)
        self.assertIn("Do not change Work Tracker state", self.skill)


class CodeReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_text(CODE_REVIEW)

    def test_review_accepts_one_or_many_fixed_targets(self) -> None:
        self.assertIn("one or more fixed Repository Targets", self.skill)
        for public_field in (
            "Repository ID",
            "Fixed point",
            "Review head",
            "Authoritative sources",
            "Settled seams",
        ):
            with self.subTest(public_field=public_field):
                self.assertIn(public_field, self.skill)

    def test_axes_are_selectable_and_default_to_both(self) -> None:
        self.assertIn("Standards only", self.skill)
        self.assertIn("Spec only", self.skill)
        self.assertIn("Both (the standalone default)", self.skill)

    def test_results_are_repository_local_for_standards_and_bundle_wide_for_spec(self) -> None:
        self.assertIn("one fresh Standards Reviewer per selected Repository Target", self.skill)
        self.assertIn("one fresh Bundle Spec Reviewer", self.skill)
        self.assertIn("## Standards — <Repository ID>", self.skill)
        self.assertIn("## Spec — Delivery Bundle", self.skill)

    def test_changed_heads_invalidate_validation_and_standards_evidence(self) -> None:
        self.assertIn("Changed heads invalidate", self.skill)
        self.assertIn("repository validation", self.skill)
        self.assertIn("Standards", self.skill)

    def test_review_has_no_external_mutation_authority(self) -> None:
        self.assertIn("does not publish", self.skill)
        self.assertIn("does not create or update Review Proposals", self.skill)
        self.assertIn("does not change Work Tracker state", self.skill)


if __name__ == "__main__":
    unittest.main()
