# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](SKILL.md) — **module**, **interface**, **seam**, **adapter**.

## When deepening pays

Deepen a cluster when shallow modules split one logical responsibility, expose shared invariant knowledge, or force callers to coordinate behavior that belongs behind one interface. Proportional design favors deepening when it reduces total interface complexity and improves locality.

## Dependency strategies

Dependency category determines how the deepening is implemented and tested; it is neither justification for deepening nor a reason to avoid it.

### In-process

Pure computation, in-memory state, no I/O. Technically straightforward: merge the modules and test through the new interface directly. No adapter needed.

### Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Technically feasible when a suitable stand-in exists. Test the deepened module through its interface with the stand-in running behind it in the test suite. The dependency seam remains internal; no port appears at the module's external interface.

### Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam discipline

Apply the [adapter-count and internal-seam principles](SKILL.md#principles) when placing the port.

## Replace, don't layer

- Before replacing old tests, map every current acceptance criterion, established invariant, and credible failure they protect to observable behavior exercised through the deepened module's interface at its seam.
- Once that replacement coverage exists, delete every test that invokes a superseded shallow interface or tests through an internal seam. Do not preserve old tests as a historical layer.
- Write and retain replacement tests through the deepened module's interface. If necessary behavior cannot be exercised and observed there, reconsider the module's interface or logical ownership.
- For an effectful module, invoke only that interface, then observe the resulting state or message through a stand-in for the declared external system. The external effect is observable behavior; the internal port, adapter calls, and collaboration sequence are not test surfaces.
