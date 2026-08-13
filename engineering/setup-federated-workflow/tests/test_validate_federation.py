from __future__ import annotations

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


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
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
) -> None:
    root.mkdir()
    run(["git", "init", "-b", base_branch], root)
    run(["git", "remote", "add", "origin", remote], root)
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
        (root / "docs" / "agents" / "issue-tracker.md").write_text(
            "# Work Tracker: GitLab\n\n"
            "## Binding\n## Ticket operations\n## Routing\n## Dependencies\n"
            "## Claims\n## Delivery dispatch\n## Coordination log\n"
            "## Triage request surfaces\n## Wayfinding operations\n"
            "## Workflow Identity permissions\n## Binding validation\n"
        )
        (root / "docs" / "agents" / "triage-labels.md").write_text(
            "# Routing Labels\n"
        )
    run(["git", "config", "user.name", "Test User"], root)
    run(["git", "config", "user.email", "test@example.test"], root)
    run(["git", "add", "."], root)
    run(["git", "commit", "-m", "test fixture"], root)


class ValidateFederationCliTests(unittest.TestCase):
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
            run(["git", "switch", "-c", "ai/federation-setup"], home)
            run(["git", "switch", "-c", "ai/federation-setup"], member)
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
                    "--member",
                    f"member={member}",
                ],
                root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("member Home Repository ID is not home", result.stderr)
            self.assertIn("machine-local path", result.stderr)


if __name__ == "__main__":
    unittest.main()
