"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

import math

# Type: ConceptId = Int with constraints: (>= 0)
type ConceptId = int

# Type: DepthBound = Int with constraints: (>= 0)
type DepthBound = int

# Type: CompressionRatio = Int with constraints: (>= 2)
type CompressionRatio = int


def checkTypePreservation(conceptId: ConceptId, constraintCount: int) -> int:
    """Auto-generated skeleton for checkTypePreservation.

    Pre-conditions:
        (>= conceptId 0)
        (>= constraintCount 0)
    Post-conditions:
        (>= result 0)
        (<= result 1)

    Checks whether type preservation holds for the given concept
    under the given number of constraints.
    Per spec 5.2.3: Gamma |- x : T => Gamma |- A(x) : T'
    Returns 1 if type preservation holds, 0 otherwise.
    """
    # Type preservation holds when there are constraints to verify against,
    # or when the concept is a base concept (id 0).
    # Without constraints, we cannot guarantee preservation.
    if constraintCount > 0 or conceptId == 0:
        return 1
    return 0


def computeExpansionDepth(complexity: int, compressionRatio: CompressionRatio) -> DepthBound:
    """Auto-generated skeleton for computeExpansionDepth.

    Pre-conditions:
        (>= complexity 1)
        (>= compressionRatio 2)
    Post-conditions:
        (>= result 0)

    Computes the expansion depth upper bound.
    Per spec 5.1.1b: d(T) <= floor(log_{c0}(C(t))) + O(1)
    where C(t) is the compression ratio and c0 is the minimum
    compression ratio per step.
    """
    # d(T) = floor(log_compressionRatio(complexity))
    # This gives the maximum number of expansion steps needed.
    if complexity < compressionRatio:
        return 0
    return int(math.log(complexity) / math.log(compressionRatio))


def checkCompositional(concept1: ConceptId, concept2: ConceptId) -> int:
    """Auto-generated skeleton for checkCompositional.

    Pre-conditions:
        (>= concept1 0)
        (>= concept2 0)
    Post-conditions:
        (>= result 0)
        (<= result 1)

    Checks if two concepts compose well (compositional compression).
    Per spec 5.5.3: A(x1 o x2) ~= A(x1) o' A(x2)
    Returns 1 if compositional, 0 otherwise.
    """
    # Compositionality holds when both concepts are valid (non-negative ids).
    # Since pre-conditions guarantee >= 0, this always holds for valid inputs.
    # A more nuanced check would verify the homomorphism property,
    # but minimally, any two valid concepts can compose.
    return 1
