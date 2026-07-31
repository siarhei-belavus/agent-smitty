from __future__ import annotations

import unittest
from pathlib import Path


ENGINEERING_SKILLS = Path(__file__).resolve().parents[1]
IMPLEMENT = ENGINEERING_SKILLS / "implement" / "SKILL.md"
CODE_REVIEW = ENGINEERING_SKILLS / "code-review" / "SKILL.md"


def skill_text(path: Path) -> str:
    return path.read_text()


def markdown_section(text: str, heading: str) -> str:
    marker = f"{heading}\n"
    start = text.index(marker) + len(marker)
    level = len(heading) - len(heading.lstrip("#"))
    lines: list[str] = []
    for line in text[start:].splitlines():
        if line.startswith("#"):
            next_level = len(line) - len(line.lstrip("#"))
            if next_level <= level:
                break
        lines.append(line)
    return "\n".join(lines)


class ImplementContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_text(IMPLEMENT)

    def test_standalone_assignment_accepts_one_or_many_repository_deliveries(self) -> None:
        standalone = markdown_section(self.skill, "### Standalone assignment")
        self.assertIn("accepts one or more Repository Deliveries", standalone)
        self.assertIn("Repository References", standalone)
        self.assertIn("Repository Scope", standalone)
        self.assertIn("single-repository invocation", standalone)

    def test_coordinator_narrowing_is_one_repository_and_one_execution_worktree(self) -> None:
        narrowed = markdown_section(self.skill, "### Coordinator-narrowed assignment")
        self.assertIn("exactly one named Repository Scope entry", narrowed)
        self.assertIn("one supplied Execution Worktree", narrowed)
        self.assertIn("Change only that Execution Worktree", narrowed)
        self.assertIn("Material contradiction", narrowed)

    def test_delivery_result_is_bound_to_exact_git_and_validation_evidence(self) -> None:
        result = markdown_section(self.skill, "## Finish the selected mode")
        for public_field in (
            "Fixed review base",
            "Exact local HEAD",
            "Clean delivery state",
            "Repository validation commands and outcomes",
        ):
            with self.subTest(public_field=public_field):
                self.assertIn(public_field, result)

    def test_validation_evidence_matches_a_committed_clean_delivery_state(self) -> None:
        validation = markdown_section(self.skill, "## Implement and validate")
        self.assertIn("Clean delivery state", validation)
        self.assertIn("every assignment-owned change is committed", validation)
        self.assertIn("worktree is clean", validation)
        self.assertIn("do not attribute validation to `HEAD`", validation)

    def test_narrowed_assignment_has_no_external_mutation_authority(self) -> None:
        narrowed = markdown_section(self.skill, "### Coordinator-narrowed assignment")
        self.assertIn("Do not publish a branch", narrowed)
        self.assertIn("Do not create or update a Review Proposal", narrowed)
        self.assertIn("Do not change Work Tracker state", narrowed)


class CodeReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_text(CODE_REVIEW)

    def test_review_accepts_one_or_many_fixed_targets(self) -> None:
        public_input = markdown_section(self.skill, "## Public input")
        self.assertIn("one or more fixed Repository Targets", public_input)
        for public_field in (
            "Repository ID",
            "Fixed point",
            "Review head",
            "Authoritative sources",
            "Settled seams",
        ):
            with self.subTest(public_field=public_field):
                self.assertIn(public_field, public_input)

    def test_single_repository_dirty_state_is_classified(self) -> None:
        public_input = markdown_section(self.skill, "## Public input")
        self.assertIn("When the single-repository worktree is dirty", public_input)
        self.assertIn("ask whether those changes are in scope", public_input)

    def test_axes_are_selectable_and_default_to_both(self) -> None:
        public_input = markdown_section(self.skill, "## Public input")
        self.assertIn("Standards only", public_input)
        self.assertIn("Spec only", public_input)
        self.assertIn("Both (the standalone default)", public_input)

    def test_results_are_repository_local_for_standards_and_bundle_wide_for_spec(self) -> None:
        aggregate = markdown_section(self.skill, "### 5. Aggregate without merging axes")
        self.assertIn("## Standards — <Repository ID>", aggregate)
        self.assertIn("## Spec — Delivery Bundle", aggregate)
        self.assertIn("Do not merge, reclassify, or rerank the axes", aggregate)

    def test_wip_evidence_uses_a_canonical_git_tree_snapshot(self) -> None:
        pinning = markdown_section(self.skill, "### 1. Pin every target")
        self.assertIn("Worktree snapshot ID", pinning)
        self.assertIn("temporary Git index", pinning)
        self.assertIn("git write-tree", pinning)
        self.assertIn("snapshot ID changes", pinning)

    def test_changed_targets_invalidate_dependent_evidence(self) -> None:
        freshness = markdown_section(self.skill, "## Evidence freshness")
        self.assertIn("Changed heads or snapshot IDs", freshness)
        self.assertIn("repository validation and Standards results", freshness)
        self.assertIn("Spec result", freshness)

    def test_review_has_no_external_mutation_authority(self) -> None:
        aggregate = markdown_section(self.skill, "### 5. Aggregate without merging axes")
        self.assertIn("does not publish", aggregate)
        self.assertIn("does not create or update Review Proposals", aggregate)
        self.assertIn("does not change Work Tracker state", aggregate)


if __name__ == "__main__":
    unittest.main()
