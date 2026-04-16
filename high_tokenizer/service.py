"""Orchestration service layer for the high-tokenizer system.

Integrates all 8 modules into a unified API.
Reference: docs/05_api_specification.md §3.

Endpoints:
- health_check:         GET  /health
- abstract_text:        POST /abstract
- expand_term:          POST /expand
- validate_expression:  POST /validate
- estimate_complexity:  POST /complexity/estimate
- evaluate_mdl:         POST /mdl/evaluate
- batch_abstract:       POST /batch/abstract
- batch_expand:         POST /batch/expand
"""

from __future__ import annotations

from typing import Any

from high_tokenizer.complexity_estimator import estimate_concepts, estimate_term
from high_tokenizer.constraint_validator import validate_term
from high_tokenizer.engines import abstract, expand
from high_tokenizer.inference_control import (
    detectOverthinking,
    optimalStop,
)
from high_tokenizer.mdl_evaluator import score_candidate
from high_tokenizer.type_preservation import (
    checkCompositional,
    checkTypePreservation,
    computeExpansionDepth,
)
from high_tokenizer.type_system import infer_term_type, validate_assignment


def health_check() -> dict[str, str]:
    """GET /health — system health check."""
    return {"status": "ok"}


def abstract_text(concepts: list[int], context: list[int]) -> dict[str, Any]:
    """POST /abstract — compress concepts into high-order terms.

    Pipeline: concepts → complexity estimate → abstraction → MDL ranking.
    """
    if not concepts:
        return {"candidates": [], "candidate_count": 0, "complexity": 0.0}

    complexity = estimate_concepts(len(concepts), len(context))
    candidate_count = abstract(len(concepts), len(context))

    candidates = []
    for i in range(min(candidate_count, 10)):
        term_id = concepts[0] + i
        term_complexity = estimate_term(1, i)
        validation = validate_term(term_id, len(context))
        mdl = score_candidate(complexity, term_complexity, 0.0 if validation else 1.0)
        type_check = checkTypePreservation(term_id, len(context))

        candidates.append(
            {
                "term_id": term_id,
                "mdl_score": mdl,
                "is_valid": validation > 0,
                "type_preserved": type_check > 0,
            }
        )

    return {
        "candidates": candidates,
        "candidate_count": len(candidates),
        "complexity": complexity,
    }


def expand_term(term_id: int, granularity: int) -> dict[str, Any]:
    """POST /expand — expand a high-order term into low-order concepts.

    Includes depth tracking (§5.1.1b) and optimal stopping (§5.5.6).
    """
    expansion_size = expand(term_id, granularity)
    depth = computeExpansionDepth(max(1, expansion_size), max(2, granularity))
    optimal_step = optimalStop(max(1, granularity))
    overthinking = detectOverthinking(max(1, expansion_size), optimal_step)

    return {
        "expansion_size": expansion_size,
        "depth": depth,
        "optimal_step": optimal_step,
        "overthinking_score": overthinking,
    }


def validate_expression(term_id: int, context_size: int) -> dict[str, Any]:
    """POST /validate — check type and constraint consistency.

    Combines type system validation with type preservation check (§5.1.1).
    """
    term_validation = validate_term(term_id, context_size)
    type_id = infer_term_type(term_id, context_size)
    assignment_valid = validate_assignment(term_id, type_id)
    type_preserved = checkTypePreservation(term_id, context_size)
    compositional = checkCompositional(term_id, term_id)

    return {
        "is_valid": term_validation > 0 and assignment_valid > 0,
        "type_preserved": type_preserved > 0,
        "compositional": compositional > 0,
        "inferred_type": type_id,
        "violation_count": 0 if term_validation > 0 else 1,
    }


def estimate_complexity(concept_count: int, context_size: int) -> dict[str, Any]:
    """POST /complexity/estimate — estimate Kolmogorov complexity approximation."""
    total_cost = estimate_concepts(max(1, concept_count), context_size)
    return {
        "total_cost": total_cost,
        "concept_count": concept_count,
        "context_size": context_size,
    }


def evaluate_mdl(
    source_cost: float, candidate_cost: float, violation_penalty: float
) -> dict[str, Any]:
    """POST /mdl/evaluate — evaluate candidate using MDL principle."""
    mdl = score_candidate(source_cost, candidate_cost, violation_penalty)
    decision = "accept" if violation_penalty == 0 else "penalized"
    return {
        "mdl_score": mdl,
        "decision": decision,
        "source_cost": source_cost,
        "candidate_cost": candidate_cost,
    }


def batch_abstract(inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """POST /batch/abstract — batch abstraction."""
    return [abstract_text(**inp) for inp in inputs]


def batch_expand(inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """POST /batch/expand — batch expansion."""
    return [expand_term(**inp) for inp in inputs]
