#!/usr/bin/env python3
"""Validate a materialized Domain Federation without changing it."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CODE_HOST_HEADINGS = (
    "## Binding",
    "## Repository operations",
    "## Published Delivery Heads",
    "## Review Proposals",
    "## Review Feedback",
    "## Workflow Identity permissions",
    "## Binding validation",
)
WORK_TRACKER_HEADINGS = (
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
MAP_HEADINGS = ("## Contexts", "## External Systems", "## Relationships")
LOCAL_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\\\)")
FIELD = r"(?m)^-\s+{label}:\s+`([^`]+)`\s*$"
MAP_REPOSITORY = re.compile(
    r"(?m)^\s*-\s+(?:Owner|Participant):\s+`([^`]+)`;\s+"
    r"Remote:\s+`([^`]+)`;\s+Base Branch:\s+`([^`]+)`\."
)
CONTEXT_POINTER = re.compile(r"\[[^\]]+\]\(([^():\s]+):([^)\s]+)\)")


@dataclass(frozen=True)
class Repository:
    repository_id: str
    path: Path
    remote: str
    base_branch: str
    role: str
    home_id: str
    home_remote: str
    home_branch: str


def parse_location(value: str) -> tuple[str, Path]:
    repository_id, separator, raw_path = value.partition("=")
    if not separator or not repository_id or not raw_path:
        raise argparse.ArgumentTypeError("expected REPOSITORY_ID=PATH")
    return repository_id, Path(raw_path).resolve()


def read(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text()
    except OSError as error:
        errors.append(f"cannot read {path}: {error}")
        return ""


def field(text: str, label: str, source: Path, errors: list[str]) -> str:
    match = re.search(FIELD.format(label=re.escape(label)), text)
    if not match:
        errors.append(f"{source} has no {label} binding")
        return ""
    return match.group(1)


def git_output(path: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *arguments],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def load_repository(
    declared_id: str,
    path: Path,
    errors: list[str],
) -> Repository:
    code_host_path = path / "docs" / "agents" / "code-host.md"
    domain_path = path / "docs" / "agents" / "domain.md"
    code_host = read(code_host_path, errors)
    domain = read(domain_path, errors)

    for heading in CODE_HOST_HEADINGS:
        if heading not in code_host:
            errors.append(f"{code_host_path} is missing {heading}")

    repository_id = field(code_host, "Repository ID", code_host_path, errors)
    remote = field(code_host, "Remote", code_host_path, errors)
    base_branch = field(code_host, "Base Branch", code_host_path, errors)
    role = field(domain, "Role", domain_path, errors)
    home_id = field(domain, "Home Repository ID", domain_path, errors)
    home_remote = field(domain, "Home Remote", domain_path, errors)
    home_branch = field(domain, "Home Base Branch", domain_path, errors)

    if repository_id and repository_id != declared_id:
        errors.append(
            f"{declared_id} is configured as Repository ID {repository_id}"
        )
    origin = git_output(path, "remote", "get-url", "origin")
    if remote and origin != remote:
        errors.append(f"{declared_id} origin does not match its Remote binding")
    local_base = git_output(
        path,
        "rev-parse",
        "--verify",
        f"refs/heads/{base_branch}^{{commit}}",
    )
    remote_base = git_output(
        path,
        "rev-parse",
        "--verify",
        f"refs/remotes/origin/{base_branch}^{{commit}}",
    )
    if base_branch and not (local_base or remote_base):
        errors.append(
            f"{declared_id} configured Base Branch {base_branch} does not exist"
        )
    agents = read(path / "AGENTS.md", errors)
    for pointer in ("docs/agents/code-host.md", "docs/agents/domain.md"):
        if pointer not in agents:
            errors.append(f"{declared_id} AGENTS.md does not index {pointer}")

    persisted = "\n".join((agents, code_host, domain))
    if LOCAL_PATH.search(persisted):
        errors.append(f"{declared_id} configuration contains a machine-local path")
    return Repository(
        declared_id,
        path,
        remote,
        base_branch,
        role,
        home_id,
        home_remote,
        home_branch,
    )


def validate_ticket_origin(
    repository: Repository,
    errors: list[str],
) -> None:
    tracker_path = repository.path / "docs" / "agents" / "issue-tracker.md"
    labels_path = repository.path / "docs" / "agents" / "triage-labels.md"
    tracker = read(tracker_path, errors)
    for heading in WORK_TRACKER_HEADINGS:
        if heading not in tracker:
            errors.append(f"{tracker_path} is missing {heading}")
    if not labels_path.is_file():
        errors.append(f"{repository.repository_id} has no Routing Label mapping")

    agents = read(repository.path / "AGENTS.md", errors)
    for pointer in (
        "docs/agents/issue-tracker.md",
        "docs/agents/triage-labels.md",
    ):
        if pointer not in agents:
            errors.append(
                f"{repository.repository_id} AGENTS.md does not index {pointer}"
            )
    persisted = "\n".join((agents, tracker, read(labels_path, errors)))
    if LOCAL_PATH.search(persisted):
        errors.append(
            f"{repository.repository_id} Ticket Origin configuration "
            "contains a machine-local path"
        )


def validate(arguments: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    home_id, home_path = arguments.home
    member_locations: dict[str, Path] = {}
    for repository_id, path in arguments.member:
        if repository_id in member_locations:
            errors.append(f"{repository_id} is supplied more than once")
            continue
        member_locations[repository_id] = path
    if home_id in member_locations:
        errors.append("the Home cannot also be supplied as a member")
    repositories = {
        home_id: load_repository(home_id, home_path, errors),
        **{
            repository_id: load_repository(repository_id, path, errors)
            for repository_id, path in member_locations.items()
        },
    }
    ticket_origins: set[str] = set()
    for repository_id in arguments.ticket_origin:
        if repository_id in ticket_origins:
            errors.append(
                f"{repository_id} is supplied as Ticket Origin more than once"
            )
        elif repository_id not in repositories:
            errors.append(f"Ticket Origin uses unknown Repository ID {repository_id}")
        else:
            ticket_origins.add(repository_id)
    home = repositories[home_id]
    if home.role != "Home":
        errors.append(f"{home_id} Domain Federation Role is not Home")
    expected_home = (home_id, home.remote, home.base_branch)
    actual_home = (home.home_id, home.home_remote, home.home_branch)
    if actual_home != expected_home:
        errors.append(f"{home_id} Home binding is not self-reciprocal")

    for repository_id, repository in repositories.items():
        if repository_id in ticket_origins:
            validate_ticket_origin(repository, errors)
            continue
        for forbidden in ("issue-tracker.md", "triage-labels.md"):
            if (repository.path / "docs" / "agents" / forbidden).exists():
                errors.append(
                    f"{repository_id} is not a confirmed Ticket Origin and "
                    f"must not own {forbidden}"
                )

    for repository_id in member_locations:
        member = repositories[repository_id]
        if member.role != "Member":
            errors.append(f"{repository_id} Domain Federation Role is not Member")
        if member.home_id != home_id:
            errors.append(f"{repository_id} Home Repository ID is not {home_id}")
        if (member.home_remote, member.home_branch) != (
            home.remote,
            home.base_branch,
        ):
            errors.append(f"{repository_id} Home identity is not portable and exact")

    map_path = home.path / "CONTEXT-MAP.md"
    context_map = read(map_path, errors)
    for heading in MAP_HEADINGS:
        if heading not in context_map:
            errors.append(f"{map_path} is missing {heading}")
    if LOCAL_PATH.search(context_map):
        errors.append(f"{map_path} contains a machine-local path")

    mapped: dict[str, list[tuple[str, str]]] = {}
    for repository_id, remote, branch in MAP_REPOSITORY.findall(context_map):
        mapped.setdefault(repository_id, []).append((remote, branch))
    for repository_id, member_path in member_locations.items():
        member = repositories[repository_id]
        identities = mapped.get(repository_id, [])
        if not identities:
            errors.append(f"{repository_id} has no exact portable identity in the Home map")
        elif any(
            identity != (member.remote, member.base_branch)
            for identity in identities
        ):
            errors.append(
                f"{repository_id} has an inconsistent portable identity "
                "in the Home map"
            )

    for repository_id, relative_path in CONTEXT_POINTER.findall(context_map):
        repository = repositories.get(repository_id)
        if repository is None:
            errors.append(f"Context pointer uses unknown Repository ID {repository_id}")
        elif not (repository.path / relative_path).is_file():
            errors.append(
                f"Context pointer does not resolve: {repository_id}:{relative_path}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate repository-owned Domain Federation bindings"
    )
    parser.add_argument("--home", required=True, type=parse_location)
    parser.add_argument(
        "--member",
        action="append",
        default=[],
        type=parse_location,
        metavar="REPOSITORY_ID=PATH",
    )
    parser.add_argument(
        "--ticket-origin",
        action="append",
        default=[],
        metavar="REPOSITORY_ID",
        help="human-confirmed Ticket Origin Repository ID; repeat as needed",
    )
    arguments = parser.parse_args()
    errors = validate(arguments)
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"Federation valid: 1 home, {len(arguments.member)} "
        f"member{'s' if len(arguments.member) != 1 else ''}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
