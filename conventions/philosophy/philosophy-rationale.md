# Convention philosophy rationale

*Last updated: 2026-09-12*

> Why WoW2 authors its own conventions rather than adopting another ecosystem's rules wholesale.

## Why

WoW2 has its own philosophy. It combines other philosophies, knowledge, conventions and practical experience
into a coherent way of building. Microsoft guidance, books and blogs contribute evidence and ideas;
their authorship does not determine which rule fits WoW2.

A framework recommendation can identify a useful risk without deciding the house convention. The decision
depends on the concrete behavior, the workflows WoW2 wants, and the cost of the available mitigations.

For example, preferring records for data-oriented models and convenient `with` copies is a design benefit
to weigh. A recommendation to prefer classes for ORM entities is an input to that comparison, not its result.
Language and runtime behavior still constrain what either design can deliver.

The operative rules live in [convention philosophy](philosophy.md).
