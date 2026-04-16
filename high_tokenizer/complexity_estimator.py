"""Complexity estimator for concept compression.

Implements C(x) = αC_sym + βC_str + γC_dep + δC_ctx
from docs/04_implementation_spec.md §4.4.

Reference: specs/high_tokenizer/complexity_estimator.spec
"""

from __future__ import annotations


def estimate_concepts(concept_count: int, context_size: int) -> float:
    """Estimate complexity of a concept sequence.

    C(x) = α·C_sym + β·C_str + γ·C_dep + δ·C_ctx

    Pre: concept_count >= 1, context_size >= 0
    Post: result >= 0
    """
    alpha, beta, gamma, delta = 0.3, 0.3, 0.2, 0.2

    c_sym = float(concept_count)  # symbol length cost
    c_str = float(concept_count) * 1.5  # structural cost (nodes + edges)
    c_dep = float(concept_count) * 0.5  # dependency cost
    c_ctx = float(max(0, context_size - concept_count))  # context correction

    return alpha * c_sym + beta * c_str + gamma * c_dep + delta * c_ctx


def estimate_term(term_length: int, type_complexity: int) -> float:
    """Estimate complexity of a typed term.

    Pre: term_length >= 0, type_complexity >= 0
    Post: result >= 0
    """
    return float(term_length) + float(type_complexity) * 0.5
