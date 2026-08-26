from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_federation.py"
)
REQUIRED_WORK_TRACKER_HEADINGS = (
    "## Binding",
    "## Ticket operations",
    "## Routing",
    "## Dependencies",
    "## Claims",
    "## Delivery frontier",
    "## Coordination log",
    "## Triage request surfaces",
    "## Wayfinding operations",
    "## Workflow Identity permissions",
    "## Binding validation",
)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def run_setup(
    command: list[str],
    cwd: Path,
    *,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def write_repository(
    root: Path,
    repository_id: str,
    remote: str,
    base_branch: str,
    *,
    role: str,
    home: tuple[str, str, str],
    ticket_origin: bool = False,
    work_tracker_headings: tuple[str, ...] = REQUIRED_WORK_TRACKER_HEADINGS,
    work_tracker_section_content: str = "Provider-specific instructions.",
) -> None:
    root.mkdir()
    run_setup(["git", "init", "-b", base_branch], root)
    run_setup(["git", "remote", "add", "origin", remote], root)
    (root / "docs" / "agents").mkdir(parents=True)
    (root / "AGENTS.md").write_text(
        "# Agent instructions\n\n"
        "## Agent skills\n\n"
        "### Code host\n\nSee `docs/agents/code-host.md`.\n\n"
        "### Domain docs\n\nSee `docs/agents/domain.md`.\n"
        + (
            "\n### Issue tracker\n\nSee `docs/agents/issue-tracker.md`.\n"
            "\n### Triage labels\n\nSee `docs/agents/triage-labels.md`.\n"
            if ticket_origin
            else ""
        )
    )
    (root / "docs" / "agents" / "code-host.md").write_text(
        "# Code Host: GitLab\n\n"
        "## Binding\n\n"
        f"- Repository ID: `{repository_id}`\n"
        f"- Remote: `{remote}`\n"
        f"- Base Branch: `{base_branch}`\n\n"
        "## Repository operations\n\nRead and fetch exact revisions.\n\n"
        "## Published Delivery Heads\n\nPublish and verify the exact revision.\n\n"
        "## Review Proposals\n\nUse one proposal per delivery.\n\n"
        "## Review Feedback\n\nRead actionable feedback.\n\n"
        "## Workflow Identity permissions\n\nNo credentials.\n\n"
        "## Binding validation\n\nValidation is non-destructive.\n"
    )
    home_id, home_remote, home_branch = home
    (root / "docs" / "agents" / "domain.md").write_text(
        "# Domain Orientation\n\n"
        "## Domain Federation\n\n"
        f"- Role: `{role}`\n"
        f"- Home Repository ID: `{home_id}`\n"
        f"- Home Remote: `{home_remote}`\n"
        f"- Home Base Branch: `{home_branch}`\n"
    )
    if ticket_origin:
        work_tracker_sections = "\n\n".join(
            f"{heading}\n\n{work_tracker_section_content}"
            for heading in work_tracker_headings
        )
        (root / "docs" / "agents" / "issue-tracker.md").write_text(
            f"# Work Tracker: GitLab\n\n{work_tracker_sections}\n"
        )
        (root / "docs" / "agents" / "triage-labels.md").write_text(
            "# Routing Labels\n"
        )
    run_setup(["git", "config", "user.name", "Test User"], root)
    run_setup(["git", "config", "user.email", "test@example.test"], root)
    run_setup(["git", "config", "maintenance.auto", "false"], root)
    run_setup(["git", "config", "core.hooksPath", "/dev/null"], root)
    tree = run_setup(
        ["git", "hash-object", "-t", "tree", "--stdin"],
        root,
        input_text="",
    )
    commit = run_setup(
        ["git", "commit-tree", tree.stdout.strip(), "-m", "test fixture"],
        root,
    )
    run_setup(
        ["git", "update-ref", f"refs/heads/{base_branch}", commit.stdout.strip()],
        root,
    )


class ValidateFederationCliTests(unittest.TestCase):
    def test_fixture_setup_ignores_piped_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repository"
            identity = (
                "repository",
                "git@example.test:group/repository.git",
                "main",
            )
            read_fd, write_fd = os.pipe()
            os.write(write_fd, b"ambient input must not become a Git object")
            os.close(write_fd)
            original_stdin = os.dup(0)
            try:
                os.dup2(read_fd, 0)
                os.close(read_fd)
                write_repository(
                    root,
                    *identity,
                    role="Home",
                    home=identity,
                )
            finally:
                os.dup2(original_stdin, 0)
                os.close(original_stdin)

            result = run(["git", "rev-parse", "refs/heads/main"], root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_tracker_pointers_without_confirmed_ticket_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
            )
            agents_path = home / "AGENTS.md"
            agents_path.write_text(
                agents_path.read_text()
                + "\n### Issue tracker\n\n"
                + "See `docs/agents/issue-tracker.md`.\n"
                + "\n### Triage labels\n\n"
                + "See `docs/agents/triage-labels.md`.\n"
            )
            (home / "CONTEXT-MAP.md").write_text(
                "# Map\n\n## Contexts\n\n- None.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [sys.executable, str(SCRIPT), "--home", f"home={home}"],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                "home is not a confirmed Ticket Origin but AGENTS.md indexes "
                "docs/agents/issue-tracker.md",
                result.stderr,
            )
            self.assertIn(
                "home is not a confirmed Ticket Origin but AGENTS.md indexes "
                "docs/agents/triage-labels.md",
                result.stderr,
            )

    def test_rejects_tracker_bindings_without_confirmed_ticket_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            (home / "CONTEXT-MAP.md").write_text(
                "# Map\n\n## Contexts\n\n- None.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [sys.executable, str(SCRIPT), "--home", f"home={home}"],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                "home is not a confirmed Ticket Origin and must not own "
                "issue-tracker.md",
                result.stderr,
            )

    def test_requires_every_work_tracker_section(self) -> None:
        for missing_heading in REQUIRED_WORK_TRACKER_HEADINGS:
            with self.subTest(missing_heading=missing_heading):
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    home = root / "home"
                    home_identity = (
                        "home",
                        "git@example.test:group/home.git",
                        "main",
                    )
                    headings = tuple(
                        heading
                        for heading in REQUIRED_WORK_TRACKER_HEADINGS
                        if heading != missing_heading
                    )
                    write_repository(
                        home,
                        *home_identity,
                        role="Home",
                        home=home_identity,
                        ticket_origin=True,
                        work_tracker_headings=headings,
                    )
                    (home / "CONTEXT-MAP.md").write_text(
                        "# Map\n\n## Contexts\n\n- None.\n\n"
                        "## External Systems\n\n- None.\n\n"
                        "## Relationships\n\n- None.\n"
                    )

                    result = run(
                        [
                            sys.executable,
                            str(SCRIPT),
                            "--home",
                            f"home={home}",
                            "--ticket-origin",
                            "home",
                        ],
                        root,
                    )

                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(
                        f"is missing {missing_heading}",
                        result.stderr,
                    )

    def test_does_not_interpret_work_tracker_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
                work_tracker_section_content=(
                    "Provider-specific ordinary instructions."
                ),
            )
            (home / "CONTEXT-MAP.md").write_text(
                "# Map\n\n## Contexts\n\n- None.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                ],
                root,
            )

            self.assertEqual(
                "Federation valid: 1 home, 0 members\n",
                result.stdout,
            )
            self.assertEqual("", result.stderr)
            self.assertEqual(0, result.returncode)

    def test_rejects_a_configured_base_branch_that_does_not_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
            )
            code_host_path = member / "docs" / "agents" / "code-host.md"
            code_host_path.write_text(
                code_host_path.read_text().replace(
                    "- Base Branch: `master`",
                    "- Base Branch: `missing`",
                )
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# PNL Federated Context Map\n\n"
                "## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `missing`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                "member configured Base Branch missing does not exist",
                result.stderr,
            )

    def test_rejects_any_inconsistent_repeated_map_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# PNL Federated Context Map\n\n"
                "## Contexts\n\n"
                "- [First](member:CONTEXT.md) — first context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:wrong/member.git`; Base Branch: `master`.\n\n"
                "- [Second](member:CONTEXT.md) — second context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                "member has an inconsistent portable identity in the Home map",
                result.stderr,
            )

    def test_rejects_duplicate_member_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# PNL Federated Context Map\n\n"
                "## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("member is supplied more than once", result.stderr)

    def test_validates_configuration_from_delivery_branches(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
            )
            run_setup(["git", "switch", "-c", "ai/federation-setup"], home)
            run_setup(["git", "switch", "-c", "ai/federation-setup"], member)
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# PNL Federated Context Map\n\n"
                "## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertEqual(0, result.returncode, result.stderr)

    def test_validates_reciprocal_portable_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# PNL Federated Context Map\n\n"
                "## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Federation valid: 1 home, 1 member", result.stdout)

    def test_rejects_nonreciprocal_or_machine_local_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
                ticket_origin=True,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=("wrong-home", "/Users/test/home", "main"),
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# Map\n\n## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--ticket-origin",
                    "home",
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("member Home Repository ID is not home", result.stderr)
            self.assertIn("machine-local path", result.stderr)

    def test_validates_a_member_as_the_independent_ticket_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "home"
            member = root / "member"
            home_identity = (
                "home",
                "git@example.test:group/home.git",
                "main",
            )
            write_repository(
                home,
                *home_identity,
                role="Home",
                home=home_identity,
            )
            write_repository(
                member,
                "member",
                "git@example.test:group/member.git",
                "master",
                role="Member",
                home=home_identity,
                ticket_origin=True,
            )
            (member / "CONTEXT.md").write_text("# Member Context\n")
            (home / "CONTEXT-MAP.md").write_text(
                "# Map\n\n## Contexts\n\n"
                "- [Member](member:CONTEXT.md) — member context.\n"
                "  - Owner: `member`; Remote: "
                "`git@example.test:group/member.git`; Base Branch: `master`.\n\n"
                "## External Systems\n\n- None.\n\n"
                "## Relationships\n\n- None.\n"
            )

            result = run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    f"home={home}",
                    "--member",
                    f"member={member}",
                    "--ticket-origin",
                    "member",
                ],
                root,
            )

            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
