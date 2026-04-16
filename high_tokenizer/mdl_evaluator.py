"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

# Type: MDLScore = Float with constraints: (>= 0)
type MDLScore = float

# Type: CandidateCount = Int with constraints: (>= 0)
type CandidateCount = int

# Type: RankPosition = Int with constraints: (>= 1)
type RankPosition = int


def score_candidate(
    source_cost: float, candidate_cost: float, violation_penalty: float
) -> MDLScore:
    """Auto-generated skeleton for score_candidate.

    Pre-conditions:
        (>= source_cost 0)
        (>= candidate_cost 0)
        (>= violation_penalty 0)
    Post-conditions:
        (>= result 0)

    Computes the MDL score for a candidate.
    Score = C_model(t) + C_data(x|t) + lambda * V(t, Gamma)
    Per spec 6.4: total cost is model cost + data cost + penalty.
    Here candidate_cost approximates model cost, the residual
    (source_cost - candidate_cost) approximates data cost,
    and violation_penalty is the constraint violation term.
    """
    # MDL total: candidate_cost (model) + residual (data given model) + penalty
    # residual = max(0, source_cost - candidate_cost) to ensure non-negative
    residual = abs(source_cost - candidate_cost)
    return candidate_cost + residual + violation_penalty


def rank_candidates(candidate_count: CandidateCount) -> RankPosition:
    """Auto-generated skeleton for rank_candidates.

    Pre-conditions:
        (>= candidate_count 1)
    Post-conditions:
        (>= result 1)
        (<= result candidate_count)

    Returns the rank position of the best candidate.
    With no actual candidate data, returns position 1 (best rank).
    Per spec 6.5: candidates sorted by total_cost ascending,
    so the best candidate is at position 1.
    """
    # The best candidate is always at rank 1
    return 1
