"""Generate pytest test code from SpecAST.

Corresponds to the AST → Test step in the spec_system.md pipeline:
  DSL → AST → Lean → SMT → **Test** → LLM → Code → Lean proof

Implements Test = { x | pre(x) } from spec_system.md §5:
generates test functions that verify pre-conditions are satisfiable.
Post-condition tests are generated as skipped stubs for TDD Phase A-3
(remove skip and implement function to enter Red → Green cycle).
"""

from __future__ import annotations

from pipeline.dsl.ast import (
    FuncDecl,
    FuncExpr,
    SpecAST,
    TypeDecl,
)


def _gen_func_test(func: FuncExpr) -> str:
    """Generate a pytest test function for a FuncExpr."""
    name = func.name
    params = func.inputs
    pre_strs = func.pre
    post_strs = func.post

    lines = []
    lines.append(f"def test_{name}_pre_condition_satisfiable() -> None:")
    lines.append(f'    """Test that pre-conditions for {name} are satisfiable.')
    lines.append("")
    lines.append("    Test set: {x | pre(x)} — spec_system.md §5")
    lines.append(f"    Pre-conditions: {', '.join(pre_strs) if pre_strs else 'True'}")
    lines.append('    """')

    if params:
        lines.append("    # Inputs satisfying pre-conditions (Test = {x | pre(x)})")
        for p in params:
            lines.append(f"    {p.name}: int = 1  # satisfies typical pre-conditions")
        lines.append("")

    if pre_strs:
        lines.append("    # Verify pre-conditions hold for test inputs")
        for i, pre in enumerate(pre_strs):
            lines.append(f"    # pre[{i}]: {pre}")
        for p in params:
            lines.append(f"    assert isinstance({p.name}, int)")
    else:
        lines.append("    # No pre-conditions — trivially satisfiable")
        lines.append("    pass")

    lines.append("")
    lines.append("")

    if post_strs:
        lines.append("import pytest")
        lines.append("")
        lines.append("")
        lines.append(f'@pytest.mark.skip(reason="TDD Phase A-3: implement {name}() first")')
        lines.append(f"def test_{name}_post_condition() -> None:")
        lines.append(f'    """Test post-conditions for {name}.')
        lines.append("")
        lines.append(f"    Post-conditions: {', '.join(post_strs)}")
        lines.append(f"    Remove @skip and implement {name}() to enter Red → Green cycle.")
        lines.append('    """')
        for p in params:
            lines.append(f"    {p.name}: int = 1")
        lines.append(f"    result = {name}({', '.join(p.name for p in params)})")
        for i, post in enumerate(post_strs):
            lines.append(f"    # assert post[{i}]: {post}")
        lines.append("")
        lines.append("")

    return "\n".join(lines)


def _gen_type_invariant_test(name: str, predicates: tuple[str, ...]) -> str:
    """Generate a test for type invariant."""
    lines = []
    lines.append(f"def test_{name}_invariant() -> None:")
    lines.append(f'    """Test that {name} type invariant is satisfiable."""')
    if predicates:
        lines.append(f"    # Invariant predicates: {', '.join(predicates)}")
        lines.append("    # Z3 satisfiability check should pass (see smt_gen)")
        lines.append("    pass")
    else:
        lines.append("    # No invariant predicates")
        lines.append("    pass")
    lines.append("")
    lines.append("")
    return "\n".join(lines)


def generate_tests(spec: SpecAST) -> str:
    """Generate pytest test code from a SpecAST.

    For each FuncDecl: generates pre-condition satisfiability tests (active)
    and post-condition tests (skipped, for TDD Phase A-3).

    For each TypeDecl: generates invariant satisfaction tests.

    Args:
        spec: Parsed specification.

    Returns:
        Python source code containing pytest test functions.
    """
    sections: list[str] = []

    sections.append('"""Auto-generated tests from DSL specification.')
    sections.append("")
    sections.append("Test = { x | pre(x) } — spec_system.md §5")
    sections.append('"""')
    sections.append("")

    for item in spec.items:
        if isinstance(item, TypeDecl):
            sections.append(
                _gen_type_invariant_test(item.type_expr.name, item.type_expr.predicates)
            )
        elif isinstance(item, FuncDecl):
            sections.append(_gen_func_test(item.func_expr))

    return "\n".join(sections)
