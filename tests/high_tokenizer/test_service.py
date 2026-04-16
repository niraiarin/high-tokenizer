"""Tests for the orchestration service layer.

Integrates all 8 modules into a unified API.
Reference: docs/05_api_specification.md §3.
"""

from high_tokenizer.service import (
    abstract_text,
    batch_abstract,
    batch_expand,
    estimate_complexity,
    evaluate_mdl,
    expand_term,
    health_check,
    validate_expression,
)


class TestHealthCheck:
    def test_returns_ok(self) -> None:
        result = health_check()
        assert result["status"] == "ok"


class TestAbstractText:
    def test_returns_candidates(self) -> None:
        result = abstract_text(concepts=[1, 2, 3], context=[])
        assert "candidates" in result
        assert isinstance(result["candidates"], list)
        assert result["candidate_count"] >= 0

    def test_empty_concepts(self) -> None:
        result = abstract_text(concepts=[], context=[])
        assert result["candidate_count"] == 0


class TestExpandTerm:
    def test_returns_expansion(self) -> None:
        result = expand_term(term_id=1, granularity=2)
        assert "expansion_size" in result
        assert result["expansion_size"] >= 0

    def test_granularity_affects_size(self) -> None:
        r1 = expand_term(term_id=1, granularity=1)
        r2 = expand_term(term_id=1, granularity=3)
        assert r2["expansion_size"] >= r1["expansion_size"]


class TestValidateExpression:
    def test_returns_validation(self) -> None:
        result = validate_expression(term_id=1, context_size=5)
        assert "is_valid" in result
        assert "type_preserved" in result
        assert isinstance(result["is_valid"], bool)

    def test_base_concept_is_valid(self) -> None:
        result = validate_expression(term_id=0, context_size=0)
        assert result["is_valid"] is True


class TestEstimateComplexity:
    def test_returns_profile(self) -> None:
        result = estimate_complexity(concept_count=3, context_size=2)
        assert "total_cost" in result
        assert result["total_cost"] >= 0


class TestEvaluateMDL:
    def test_returns_score(self) -> None:
        result = evaluate_mdl(source_cost=10.0, candidate_cost=5.0, violation_penalty=0.0)
        assert "mdl_score" in result
        assert result["mdl_score"] >= 0


class TestBatchAbstract:
    def test_batch_returns_list(self) -> None:
        inputs = [
            {"concepts": [1, 2], "context": []},
            {"concepts": [3, 4, 5], "context": [1]},
        ]
        results = batch_abstract(inputs)
        assert len(results) == 2
        assert all("candidates" in r for r in results)


class TestBatchExpand:
    def test_batch_returns_list(self) -> None:
        inputs = [
            {"term_id": 1, "granularity": 1},
            {"term_id": 2, "granularity": 2},
        ]
        results = batch_expand(inputs)
        assert len(results) == 2
        assert all("expansion_size" in r for r in results)
