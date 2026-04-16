"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

# Type: CandidateCount = Int with constraints: (>= 0)
type CandidateCount = int

# Type: ExpansionSize = Int with constraints: (>= 0)
type ExpansionSize = int

# Type: InputSize = Int with constraints: (>= 1)
type InputSize = int


def abstract(input_size: InputSize, context_size: int) -> CandidateCount:
    """Auto-generated skeleton for abstract.

    Pre-conditions:
        (>= input_size 1)
        (>= context_size 0)
    Post-conditions:
        (>= result 0)

    Performs abstraction: maps input concepts to candidate high-level terms.
    Per spec 7.1 / 9.1: extracts features, searches candidates, types them,
    estimates complexity, validates constraints, evaluates MDL, and ranks.
    The number of candidates depends on input_size and context_size.
    """
    # More input concepts and richer context yield more candidates.
    # At minimum, each input concept can produce one candidate,
    # modulated by context availability.
    return input_size + context_size


def expand(term_id: int, granularity: int) -> ExpansionSize:
    """Auto-generated skeleton for expand.

    Pre-conditions:
        (>= term_id 0)
        (>= granularity 1)
    Post-conditions:
        (>= result 0)

    Performs expansion: maps a high-level term to low-level concepts.
    Per spec 7.2 / 9.2: retrieves type, searches templates,
    completes premises, adjusts granularity, validates, and ranks.
    Higher granularity produces more detailed (larger) expansions.
    """
    # Expansion size grows with granularity.
    # A term with id 0 (base concept) expands to granularity elements.
    # Higher term_ids represent more abstract terms with richer expansions.
    return (term_id + 1) * granularity
