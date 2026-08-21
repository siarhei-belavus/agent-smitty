# Test surface

Exercise a module only through its interface at its seam. Assert behavior observable to a caller, not private state, internal ports, collaborator calls, call sequences, or implementation structure. Behavior-preserving refactors must not break the tests.

Acceptance criteria, domain invariants, and credible failures determine the required cases. A past bug may motivate a regression test, but the test names and asserts the behavior that must hold rather than the historical implementation mistake.

For an effectful module, invoke its interface and observe the resulting state or message through a stand-in for the declared external system.
