from pathlib import Path
import unittest


ENGINEERING = Path(__file__).resolve().parents[1]
CONTRACT = ENGINEERING / "PLANNING-ARTIFACT-CONTRACTS.md"
OLD_CONTRACT = ENGINEERING / "FEDERATED-AUTHORITY.md"


class PlanningArtifactContractTests(unittest.TestCase):
    def test_stable_contract_is_the_only_shared_owner(self) -> None:
        self.assertTrue(CONTRACT.is_file())
        self.assertFalse(OLD_CONTRACT.exists())

        body = CONTRACT.read_text()
        for heading in (
            "### Repository Reference",
            "### Context Scope",
            "### Domain Model Delta",
            "### Settled Seam",
            "### Validation Obligation",
            "### Repository Scope entry",
            "### Dependency",
            "## Composition invariants",
        ):
            self.assertIn(heading, body)

        for superseded_artifact_contract in (
            "## Specification contract",
            "## Executable delivery-ticket contract",
            "## Executable Agent Brief contract",
        ):
            self.assertNotIn(superseded_artifact_contract, body)

    def test_every_consumer_reads_the_shared_contract(self) -> None:
        consumers = (
            ENGINEERING / "to-spec" / "SKILL.md",
            ENGINEERING / "to-tickets" / "SKILL.md",
            ENGINEERING / "triage" / "SKILL.md",
            ENGINEERING / "triage" / "AGENT-BRIEF.md",
        )

        for consumer in consumers:
            with self.subTest(consumer=consumer):
                self.assertIn(
                    "PLANNING-ARTIFACT-CONTRACTS.md", consumer.read_text()
                )

        for markdown in ENGINEERING.rglob("*.md"):
            with self.subTest(markdown=markdown):
                self.assertNotIn("FEDERATED-AUTHORITY.md", markdown.read_text())

    def test_artifact_shapes_have_local_owners(self) -> None:
        spec = (ENGINEERING / "to-spec" / "SKILL.md").read_text()
        ticket = (ENGINEERING / "to-tickets" / "SKILL.md").read_text()
        brief = (ENGINEERING / "triage" / "AGENT-BRIEF.md").read_text()

        for heading in (
            "## Problem Statement",
            "## Solution",
            "## User Stories",
            "## Repository References",
            "## Context Scope",
            "## Implementation Decisions",
            "## Testing Decisions",
            "## Out of Scope",
            "## Further Notes",
        ):
            self.assertEqual(spec.count(heading), 1, heading)

        self.assertEqual(ticket.count("<ticket-body-template>"), 1)
        self.assertEqual(ticket.count("</ticket-body-template>"), 1)
        self.assertNotIn("<local-ticket-template>", ticket)
        self.assertNotIn("<issue-template>", ticket)
        for heading in (
            "## Parent",
            "## What to build",
            "## Acceptance criteria",
            "## Repository References",
            "## Repository Scope",
            "## Context Scope",
            "## Cross-Repository Seams",
            "## Blocked by",
        ):
            self.assertEqual(ticket.count(heading), 1, heading)

        for heading in (
            "### What to build",
            "### Acceptance criteria",
            "### Repository References",
            "### Repository Scope",
            "### Context Scope",
            "### Cross-Repository Seams",
            "### Out of scope",
            "### Blocked by",
        ):
            self.assertEqual(brief.count(heading), 1, heading)


if __name__ == "__main__":
    unittest.main()
