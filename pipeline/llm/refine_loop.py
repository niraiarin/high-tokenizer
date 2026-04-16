"""LLM refinement loop: S_{n+1} = Fix(LLM(S_n), Verify).

Corresponds to the LLM step in the spec_system.md pipeline:
  DSL → AST → Lean → SMT → Test → **LLM** → Code → Lean proof

The loop:
1. Verify current spec (parse + constraint check)
2. If valid → converged (fixed point reached)
3. If invalid → call LLM with error feedback → get refined spec
4. Repeat until converged or max_rounds exceeded

LLM provider: Claude API (Anthropic SDK) — injected as `llm_fn`
for testability (mock in tests, real client in production).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

from pipeline.codegen.smt_gen import check_constraints
from pipeline.dsl.parser import parse_sexpr, parse_spec


@dataclass(frozen=True)
class VerifyResult:
    """Result of verifying a spec in one round."""

    valid: bool
    errors: tuple[str, ...] = ()
    spec_text: str = ""


@dataclass(frozen=True)
class RefineResult:
    """Result of the refinement loop."""

    converged: bool
    spec_text: str
    rounds: int
    history: tuple[VerifyResult, ...] = ()


def _verify_spec(spec_text: str) -> VerifyResult:
    """Verify a spec by parsing and checking constraints.

    Returns VerifyResult with errors if any step fails.
    """
    errors: list[str] = []

    # Step 1: Parse S-expression
    try:
        sexpr = parse_sexpr(spec_text)
    except ValueError as e:
        return VerifyResult(valid=False, errors=(f"Parse error: {e}",), spec_text=spec_text)

    # Step 2: Parse spec structure
    try:
        spec_ast = parse_spec(sexpr)
    except ValueError as e:
        return VerifyResult(valid=False, errors=(f"Spec error: {e}",), spec_text=spec_text)

    # Step 3: Check well-formedness
    if not spec_ast.well_formed():
        errors.append("Spec AST is not well-formed")

    # Step 4: Check constraints via Z3
    try:
        constraint_results = check_constraints(spec_ast)
        for name, result in constraint_results.items():
            if not result.satisfiable:
                errors.append(f"Unsatisfiable constraints for type {name}")
    except Exception as e:
        errors.append(f"Constraint check error: {e}")

    if errors:
        return VerifyResult(valid=False, errors=tuple(errors), spec_text=spec_text)

    return VerifyResult(valid=True, spec_text=spec_text)


def _build_prompt(spec_text: str, verify_result: VerifyResult) -> str:
    """Build a prompt for the LLM to fix/refine a spec."""
    lines = [
        "The following DSL specification has errors."
        " Please fix it and return ONLY the corrected spec.",
        "",
        "## Current spec:",
        "```lisp",
        spec_text,
        "```",
        "",
        "## Errors found:",
    ]
    for error in verify_result.errors:
        lines.append(f"- {error}")
    lines.append("")
    lines.append("## Instructions:")
    lines.append("- Return ONLY the corrected (spec ...) S-expression")
    lines.append("- Do not include any explanation or markdown formatting")
    lines.append("- Ensure all type declarations have non-empty name and basetype")
    lines.append("- Ensure all function declarations have at least one input parameter")
    lines.append("- Ensure type constraints are satisfiable")

    return "\n".join(lines)


def _extract_spec(llm_output: str) -> str:
    """Extract spec S-expression from LLM output.

    Handles cases where LLM wraps output in markdown code blocks.
    """
    text = llm_output.strip()

    # Strip markdown code blocks if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last ``` lines
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    # Find the (spec ...) expression
    start = text.find("(spec")
    if start == -1:
        return text  # Return as-is, let verify catch errors

    # Find matching close paren
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    return text[start:]  # Unbalanced, let verify catch


def refine_spec(
    initial_spec: str,
    llm_fn: Callable[[str], str],
    max_rounds: int = 5,
) -> RefineResult:
    """Run the refinement loop: S_{n+1} = Fix(LLM(S_n), Verify).

    Args:
        initial_spec: Initial DSL spec text.
        llm_fn: Function that takes a prompt and returns LLM response.
            Injected for testability (mock in tests, Claude API in production).
        max_rounds: Maximum number of refinement rounds (k in the spec).

    Returns:
        RefineResult with convergence status, final spec, and history.
    """
    current_spec = initial_spec
    history: list[VerifyResult] = []

    for round_num in range(1, max_rounds + 1):
        # Verify current spec
        verify = _verify_spec(current_spec)
        history.append(verify)

        if verify.valid:
            # Fixed point reached
            return RefineResult(
                converged=True,
                spec_text=current_spec,
                rounds=round_num,
                history=tuple(history),
            )

        # Call LLM to refine
        prompt = _build_prompt(current_spec, verify)
        llm_output = llm_fn(prompt)
        current_spec = _extract_spec(llm_output)

    # Max rounds exceeded
    return RefineResult(
        converged=False,
        spec_text=current_spec,
        rounds=max_rounds,
        history=tuple(history),
    )
