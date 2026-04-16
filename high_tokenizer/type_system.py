"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

# Type: TypeId = Int with constraints: (>= 0)
type TypeId = int

# Type: SubtypeResult = Int with constraints: (>= 0)
type SubtypeResult = int

# Type: SubtypeResult = Int with constraints: (<= 1)


def infer_term_type(term_id: TypeId, context_size: int) -> TypeId:
    """Auto-generated skeleton for infer_term_type.

    Pre-conditions:
        (>= term_id 0)
        (>= context_size 0)
    Post-conditions:
        (>= result 0)

    Infers the type of a term given its id and context size.
    Uses a simple hash-based inference: the type is derived from
    the term_id, modulated by context_size to reflect context-dependent
    type narrowing (see spec 5.2.2 constraint-dependent types).
    """
    # Type inference: term_id itself serves as the base type.
    # Context size modulates but the result must remain >= 0.
    return term_id + context_size


def validate_assignment(term_id: TypeId, expected_type: TypeId) -> SubtypeResult:
    """Auto-generated skeleton for validate_assignment.

    Pre-conditions:
        (>= term_id 0)
        (>= expected_type 0)
    Post-conditions:
        (>= result 0)
        (<= result 1)

    Validates whether a term can be assigned to the expected type.
    Returns 1 if valid (types match or term is a subtype), 0 otherwise.
    Per spec 5.4: surface type match or subtype relation.
    """
    # Assignment is valid when the inferred type matches the expected type
    # or the term_id is a subtype of expected_type (same value = exact match).
    return 1 if is_subtype(term_id, expected_type) else 0


def is_subtype(actual: TypeId, expected: TypeId) -> SubtypeResult:
    """Auto-generated skeleton for is_subtype.

    Pre-conditions:
        (>= actual 0)
        (>= expected 0)
    Post-conditions:
        (>= result 0)
        (<= result 1)

    Checks if actual type is a subtype of expected type.
    Returns 1 if actual is a subtype of expected, 0 otherwise.
    A type is a subtype of another if it is equal or more specific
    (lower or equal id represents a more specific type in the hierarchy).
    """
    # Subtype check: actual <= expected means actual is more specific
    # or equal within the type hierarchy.
    return 1 if actual <= expected else 0
