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

        for local_owner in (
            "`/to-spec` owns the specification shape",
            "`/to-tickets` owns the delivery-ticket shape",
            "`triage/AGENT-BRIEF.md` owns the Agent Brief shape",
        ):
            self.assertIn(local_owner, body)

        self.assertIn("domain-modeling/DOMAIN-MODEL-DELTA.md", body)

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
        self.assertIn(
            "An explicit standalone invocation grants canonical capture by default",
            skill,
        )
        self.assertIn(
            "A composed or model-invoked use returns each delta to the invoking "
            "workflow without writing canonical artifacts",
            skill,
        )
        self.assertIn(
            "does not select a planning persistence destination or depend on "
            "caller identity",
            skill,
        )
        for coupled_caller in (
            "/grill-with-docs",
            "/wayfinder",
        ):
            self.assertNotIn(coupled_caller, skill)

    def test_outer_planning_workflows_own_capture(self) -> None:
        grill = (ENGINEERING / "grill-with-docs" / "SKILL.md").read_text()
        self.assertIn("/grilling", grill)
        self.assertIn("/domain-modeling", grill)
        self.assertIn("current conversation", grill)
        self.assertIn("/to-spec", grill)
        self.assertIn("The outer workflow owns any durable capture", grill)

        wayfinder = (ENGINEERING / "wayfinder" / "SKILL.md").read_text()
        self.assertIn("/grill-with-docs", wayfinder)
        self.assertIn("Resolution draft", wayfinder)

        triage = (ENGINEERING / "triage" / "SKILL.md").read_text()
        self.assertIn("/grill-with-docs", triage)
        self.assertIn("Keep returned Domain Model Deltas in the current triage context", triage)
        self.assertIn("promote every relevant delta without reduction into the Agent Brief", triage)

        architecture = (
            ENGINEERING / "improve-codebase-architecture" / "SKILL.md"
        ).read_text()
        self.assertIn("run `/grill-with-docs` as an output-only planning session", architecture)
        self.assertIn("Do not grant canonical capture", architecture)
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

    def test_to_spec_accepts_conversation_or_durable_wayfinder_authority(self) -> None:
        spec = (ENGINEERING / "to-spec" / "SKILL.md").read_text()
        for required_clause in (
            "With no Wayfinder map reference",
            "load the map through the configured Work Tracker binding",
            "re-read every final `## Resolution` linked from its Decisions-so-far",
            "The linked Resolutions, not their one-line map gists",
            "return it to Wayfinder instead of guessing",
            "When both sources are supplied",
        ):
            self.assertIn(required_clause, spec)

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
