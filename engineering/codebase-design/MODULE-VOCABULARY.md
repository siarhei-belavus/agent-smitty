# Module vocabulary

A **Module** is anything with an Interface and an implementation: a function, class, package, or tier-spanning slice.

An **Interface** is everything a caller must know to use a Module correctly, including its type-level surface, invariants, ordering constraints, error modes, required configuration, and performance characteristics.

A **Seam** is the location of a Module's Interface: a place where behavior can vary without editing in that place. Its placement is distinct from what belongs behind it. Reserve **boundary** for trust, deployment, or change-authority boundaries.

Use Module rather than component, service, or unit; Interface rather than API or signature; and Seam rather than boundary for interface location.
