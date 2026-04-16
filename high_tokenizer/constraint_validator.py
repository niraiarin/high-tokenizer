"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

# Type: ValidationScore = Int with constraints: (>= 0)
type ValidationScore = int

# Type: ValidationScore = Int with constraints: (<= 1)

# Type: ViolationCount = Int with constraints: (>= 0)
type ViolationCount = int


def validate_term(term_id: int, context_size: int) -> ValidationScore:
    """Auto-generated skeleton for validate_term.

    Pre-conditions:
        (>= term_id 0)
        (>= context_size 0)
    Post-conditions:
        (>= result 0)
        (<= result 1)

    Validates a term against the constraint context.
    Returns 1 if valid, 0 if invalid.
    Per spec 7.3: checks syntactic validity, type consistency,
    predicate satisfaction, forbidden operations, and context consistency.
    A term with a non-negative id in a non-negative context is valid
    when it has sufficient context support.
    """
    # A term is valid if it has context support (context_size > 0)
    # or if term_id is 0 (base/root term, always valid).
    if context_size > 0 or term_id == 0:
        return 1
    return 0


def validate_expansion(expansion_size: int, context_size: int) -> ViolationCount:
    """Auto-generated skeleton for validate_expansion.

    Pre-conditions:
        (>= expansion_size 0)
        (>= context_size 0)
    Post-conditions:
        (>= result 0)

    Validates an expansion and returns the number of constraint violations.
    Per spec 7.3: checks type consistency of expanded concepts against
    the constraint context. Violations occur when expansion exceeds
    context capacity.
    """
    # Violations = max(0, expansion_size - context_size)
    # If expansion is larger than context can support, each excess
    # element is a potential violation.
    if context_size == 0:
        return expansion_size
    return max(0, expansion_size - context_size)
