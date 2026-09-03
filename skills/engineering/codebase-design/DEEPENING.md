# Deepening

## When deepening pays

Deepen a cluster when shallow modules split one logical responsibility, expose shared invariant knowledge, or force callers to coordinate behavior that belongs behind one interface. Proportional design favors deepening when it reduces total interface complexity and improves locality.

## Dependency strategies

Dependency category determines how the deepening is implemented and tested; it is neither justification for deepening nor a reason to avoid it.

### In-process

Pure computation, in-memory state, no I/O. Merge the modules and test the deepened module through its interface directly. No adapter needed.

### Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Test the deepened module through its interface with the stand-in running behind it. The dependency seam remains internal; no port appears at the module's external interface.

### Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Replace, don't layer

- Inventory every acceptance criterion, established invariant, and credible failure protected by the old tests, and map each one to a replacement case.
- Once the replacement cases cover that inventory, delete every test that invokes a superseded shallow interface. Do not preserve them as a historical layer.
- If any protected behavior has no replacement case, stop and reconsider the proposed interface or logical ownership.
