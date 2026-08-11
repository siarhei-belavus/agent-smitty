from __future__ import annotations

import os
import subprocess
import tempfile
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
        self.assertIn("For each selected axis only", aggregate)
        self.assertIn("## Standards — <Repository ID>", aggregate)
        self.assertIn("## Spec — Delivery Bundle", aggregate)
        self.assertIn("do not merge, reclassify, or rerank the axes", aggregate.lower())

    def test_wip_evidence_uses_a_canonical_git_tree_snapshot(self) -> None:
        pinning = markdown_section(self.skill, "### 1. Pin every target")
        self.assertIn("Worktree snapshot ID", pinning)
        self.assertIn("temporary Git index", pinning)
        self.assertIn("temporary object store", pinning)
        self.assertIn("GIT_OBJECT_DIRECTORY", pinning)
        self.assertIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", pinning)
        self.assertIn("git write-tree", pinning)
        self.assertIn("snapshot ID changes", pinning)

    def test_wip_snapshot_capture_covers_the_repository_root(self) -> None:
        pinning = markdown_section(self.skill, "### 1. Pin every target")
        self.assertIn("target repository root as the working directory", pinning)
        self.assertIn("top-anchored pathspec `:/`", pinning)

    def test_wip_comparison_base_is_pinned_from_fixed_target_history(self) -> None:
        pinning = markdown_section(self.skill, "### 1. Pin every target")
        self.assertIn("git merge-base <fixed-point> <review-head>", pinning)
        self.assertIn("exact **Comparison base**", pinning)

    def test_wip_snapshot_evidence_covers_changes_outside_callers_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            repository = temporary / "repository"
            repository.mkdir()

            def git(*arguments: str, environment: dict[str, str] | None = None) -> str:
                result = subprocess.run(
                    ["git", *arguments],
                    cwd=repository,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return result.stdout.strip()

            git("init", "--quiet")
            git("config", "user.name", "Contract Test")
            git("config", "user.email", "contract@example.invalid")
            (repository / "root.txt").write_text("before\n")
            (repository / "nested").mkdir()
            (repository / "nested" / "kept.txt").write_text("kept\n")
            git("add", "-A")
            git("commit", "--quiet", "-m", "initial")
            (repository / "root.txt").write_text("after\n")

            object_store = temporary / "objects"
            object_store.mkdir()
            environment = os.environ | {
                "GIT_OBJECT_DIRECTORY": str(object_store),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(repository / ".git" / "objects"),
                "GIT_INDEX_FILE": str(temporary / "snapshot-index"),
            }
            git("read-tree", "HEAD", environment=environment)
            git("add", "-A", "--", ":/", environment=environment)
            snapshot_id = git("write-tree", environment=environment)

            self.assertEqual(
                "after",
                git("show", f"{snapshot_id}:root.txt", environment=environment),
            )

    def test_wip_diff_uses_the_pinned_base_for_divergent_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            repository = temporary / "repository"
            repository.mkdir()

            def git(*arguments: str, environment: dict[str, str] | None = None) -> str:
                result = subprocess.run(
                    ["git", *arguments],
                    cwd=repository,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return result.stdout.strip()

            git("init", "--quiet")
            git("config", "user.name", "Contract Test")
            git("config", "user.email", "contract@example.invalid")
            (repository / "shared.txt").write_text("shared\n")
            git("add", "-A")
            git("commit", "--quiet", "-m", "shared base")
            shared_base = git("rev-parse", "HEAD")

            git("checkout", "--quiet", "-b", "fixed")
            (repository / "fixed-only.txt").write_text("fixed\n")
            git("add", "-A")
            git("commit", "--quiet", "-m", "fixed side")
            fixed_point = git("rev-parse", "HEAD")

            git("checkout", "--quiet", "-b", "reviewed", shared_base)
            (repository / "reviewed.txt").write_text("reviewed\n")
            git("add", "-A")
            git("commit", "--quiet", "-m", "reviewed side")
            review_head = git("rev-parse", "HEAD")
            (repository / "wip.txt").write_text("wip\n")

            comparison_base = git("merge-base", fixed_point, review_head)
            self.assertEqual(shared_base, comparison_base)

            object_store = temporary / "objects"
            object_store.mkdir()
            environment = os.environ | {
                "GIT_OBJECT_DIRECTORY": str(object_store),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(repository / ".git" / "objects"),
                "GIT_INDEX_FILE": str(temporary / "snapshot-index"),
            }
            git("read-tree", review_head, environment=environment)
            git("add", "-A", "--", ":/", environment=environment)
            snapshot_id = git("write-tree", environment=environment)
            changed_files = git(
                "diff",
                "--name-only",
                comparison_base,
                snapshot_id,
                environment=environment,
            ).splitlines()

            self.assertEqual(["reviewed.txt", "wip.txt"], changed_files)

    def test_wip_validation_evidence_is_bound_to_the_snapshot(self) -> None:
        public_input = markdown_section(self.skill, "## Public input")
        self.assertIn(
            "bound to both the Review head and Worktree snapshot ID",
            public_input,
        )

    def test_wip_standards_reviewers_receive_the_immutable_change_set(self) -> None:
        reviews = markdown_section(self.skill, "### 4. Run the selected fresh reviews")
        self.assertIn("immutable materialized diff", reviews)
        self.assertIn("Worktree snapshot ID", reviews)
        self.assertIn("Standards Reviewer", reviews)

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
