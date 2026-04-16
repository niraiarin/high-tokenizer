"""Tests for LLM refinement loop.

Tests use a mock LLM client to avoid requiring API keys.
The loop's contract: S_{n+1} = Fix(LLM(S_n), Verify)
"""

from unittest.mock import MagicMock

from pipeline.llm.refine_loop import VerifyResult, refine_spec

VALID_SPEC = """(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from_acct UserId))
    (output Bool)
    (pre (> from_acct 0))
    (post (= result true))))"""

INVALID_SPEC = "(spec (unknown x))"


class TestRefineLoop:
    def test_already_valid_spec_converges_immediately(self) -> None:
        """If spec is already valid, loop returns it unchanged."""
        mock_llm = MagicMock()
        mock_llm.return_value = VALID_SPEC  # LLM returns same spec

        result = refine_spec(
            initial_spec=VALID_SPEC,
            llm_fn=mock_llm,
            max_rounds=5,
        )
        assert result.converged is True
        assert result.spec_text == VALID_SPEC
        assert result.rounds <= 1

    def test_llm_fixes_invalid_spec(self) -> None:
        """LLM is called to fix an invalid spec, returns valid one."""
        call_count = 0

        def mock_llm(prompt: str) -> str:
            nonlocal call_count
            call_count += 1
            # On first call, return the valid spec
            return VALID_SPEC

        result = refine_spec(
            initial_spec=INVALID_SPEC,
            llm_fn=mock_llm,
            max_rounds=5,
        )
        assert result.converged is True
        assert call_count >= 1

    def test_max_rounds_exceeded(self) -> None:
        """If LLM never produces valid spec, loop stops at max_rounds."""

        def mock_llm(prompt: str) -> str:
            return INVALID_SPEC  # Always returns invalid

        result = refine_spec(
            initial_spec=INVALID_SPEC,
            llm_fn=mock_llm,
            max_rounds=3,
        )
        assert result.converged is False
        assert result.rounds == 3

    def test_verify_result_captures_errors(self) -> None:
        """Verify step captures parse/constraint errors."""
        call_log: list[str] = []

        def mock_llm(prompt: str) -> str:
            call_log.append(prompt)
            return VALID_SPEC

        refine_spec(
            initial_spec="(spec (bad",  # Malformed
            llm_fn=mock_llm,
            max_rounds=5,
        )
        # LLM should have been called with error feedback
        assert len(call_log) >= 1
        assert "error" in call_log[0].lower() or "fail" in call_log[0].lower()

    def test_result_includes_verify_history(self) -> None:
        """Result includes verification history for each round."""
        result = refine_spec(
            initial_spec=VALID_SPEC,
            llm_fn=lambda _: VALID_SPEC,
            max_rounds=5,
        )
        assert len(result.history) >= 1
        assert isinstance(result.history[0], VerifyResult)
