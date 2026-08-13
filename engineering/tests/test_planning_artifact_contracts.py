from pathlib import Path
import unittest


ENGINEERING = Path(__file__).resolve().parents[1]
CONTRACT = ENGINEERING / "PLANNING-ARTIFACT-CONTRACTS.md"
DOMAIN_MODELING = ENGINEERING / "domain-modeling" / "SKILL.md"
DOMAIN_MODEL_DELTA = ENGINEERING / "domain-modeling" / "DOMAIN-MODEL-DELTA.md"


class PlanningArtifactContractTests(unittest.TestCase):
    def test_shared_contract_owns_only_shared_records_and_invariants(self) -> None:
        self.assertTrue(CONTRACT.is_file())

        body = CONTRACT.read_text()
        for heading in (
            "### Repository Reference",
            "### Context Scope",
            "### Settled Seam",
            "### Validation Obligation",
            "### Repository Scope entry",
            "### Dependency",
            "## Composition invariants",
        ):
            self.assertIn(heading, body)

        for artifact_specific_heading in (
            "## Specification contract",
            "## Executable delivery-ticket contract",
            "## Executable Agent Brief contract",
        ):
            self.assertNotIn(artifact_specific_heading, body)

        self.assertIn("domain-modeling/DOMAIN-MODEL-DELTA.md", body)
        self.assertNotIn("### Domain Model Delta", body)

    def test_domain_modeling_owns_its_output_without_knowing_callers(self) -> None:
        self.assertTrue(DOMAIN_MODEL_DELTA.is_file())
        delta = DOMAIN_MODEL_DELTA.read_text()
        for field in (
            "owning Repository ID and Canonical Context Pointer",
            "add, change, or supersede operation",
            "exact terms and definitions",
            "relationships, invariants, boundaries, scenarios, and counterexamples",
            "rationale and rejected alternatives",
            "originating decision provenance",
            "canonical documentation obligations",
            "contradiction conditions",
        ):
            self.assertIn(field, delta)

        skill = DOMAIN_MODELING.read_text()
        self.assertIn("DOMAIN-MODEL-DELTA.md", skill)
        self.assertIn("explicit standalone invocation", skill)
        self.assertIn("canonical capture", skill)
        self.assertIn("return", skill)
        for caller_detail in (
            "/grill-with-docs",
            "/wayfinder",
            "Resolution draft",
            "Work Tracker",
        ):
            self.assertNotIn(caller_detail, skill)

    def test_outer_planning_workflows_own_capture(self) -> None:
        grill = (ENGINEERING / "grill-with-docs" / "SKILL.md").read_text()
        self.assertIn("/grilling", grill)
        self.assertIn("/domain-modeling", grill)
        self.assertIn("current conversation", grill)
        self.assertIn("/to-spec", grill)
        self.assertNotIn("Resolution draft", grill)
        self.assertNotIn("Work Tracker", grill)

        wayfinder = (ENGINEERING / "wayfinder" / "SKILL.md").read_text()
        self.assertIn("/grill-with-docs", wayfinder)
        self.assertIn("Resolution draft", wayfinder)

        triage = (ENGINEERING / "triage" / "SKILL.md").read_text()
        self.assertIn("/grill-with-docs", triage)
        self.assertNotIn("run the `/grilling` and `/domain-modeling` skills together", triage)

        architecture = (
            ENGINEERING / "improve-codebase-architecture" / "SKILL.md"
        ).read_text()
        self.assertIn("do not grant canonical capture", architecture)
        self.assertIn("current conversation", architecture)

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
