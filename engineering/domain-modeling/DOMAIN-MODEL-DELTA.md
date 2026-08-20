# Domain Model Delta

A Domain Model Delta is the public result of confirming a domain-language or architecture change through the `domain-modeling` skill. It is a document-ready semantic payload that a caller can capture, promote, or apply without reconstructing the modeling conversation.

As applicable, a complete delta records:

- owning Repository ID and Canonical Context Pointer;
- add, change, or supersede operation;
- exact terms and definitions;
- relationships, invariants, boundaries, scenarios, and counterexamples;
- rationale and rejected alternatives;
- complete architecture-decision rationale when the ADR threshold was met;
- originating decision provenance;
- canonical documentation obligations; and
- contradiction conditions that require escalation rather than reinterpretation.

A summary or pointer may index a delta, but cannot replace its document-ready semantics. The delta remains the same public result whether an authorized standalone invocation applies it immediately to canonical documentation or an invoking workflow captures it elsewhere.
