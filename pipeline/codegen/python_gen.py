"""Generate Python skeleton code from SpecAST.

Corresponds to the AST → Code step in the spec_system.md pipeline:
  DSL → AST → Lean → SMT → Test → LLM → **Code** → Lean proof

Generates function skeletons with type hints, docstrings containing
pre/post conditions, and `raise NotImplementedError`. These skeletons
are the starting point for TDD: auto-generated tests (from pytest_gen)
will fail until the skeletons are filled in.
"""

from __future__ import annotations

from pipeline.dsl.ast import (
    FuncDecl,
    SpecAST,
    TypeDecl,
)

# Map DSL type names to Python type hints
_TYPE_MAP: dict[str, str] = {
    "Int": "int",
    "Bool": "bool",
    "String": "str",
    "Float": "float",
}


def _python_type(dsl_type: str) -> str:
    """Map a DSL type name to a Python type hint."""
    return _TYPE_MAP.get(dsl_type, dsl_type)


def _gen_type_alias(decl: TypeDecl) -> str:
    """Generate a Python type alias from a TypeDecl."""
    t = decl.type_expr
    base = _python_type(t.basetype)
    lines = []
    if t.predicates:
        pred_str = ", ".join(t.predicates)
        lines.append(f"# Type: {t.name} = {t.basetype} with constraints: {pred_str}")
    lines.append(f"type {t.name} = {base}")
    lines.append("")
    return "\n".join(lines)


def _gen_func_skeleton(decl: FuncDecl) -> str:
    """Generate a Python function skeleton from a FuncDecl."""
    f = decl.func_expr

    # Build parameter list with type hints
    params = []
    for p in f.inputs:
        py_type = _python_type(p.type_name)
        params.append(f"{p.name}: {py_type}")
    param_str = ", ".join(params)

    # Return type
    ret_type = _python_type(f.output) if f.output else "None"

    # Docstring with pre/post conditions
    doc_lines = [f'    """Auto-generated skeleton for {f.name}.']
    doc_lines.append("")
    if f.pre:
        doc_lines.append("    Pre-conditions:")
        for pre in f.pre:
            doc_lines.append(f"        {pre}")
    if f.post:
        doc_lines.append("    Post-conditions:")
        for post in f.post:
            doc_lines.append(f"        {post}")
    doc_lines.append('    """')

    lines = []
    lines.append(f"def {f.name}({param_str}) -> {ret_type}:")
    lines.extend(doc_lines)
    lines.append('    raise NotImplementedError("TDD: implement to make tests pass")')
    lines.append("")
    lines.append("")
    return "\n".join(lines)


def generate_python(spec: SpecAST) -> str:
    """Generate Python skeleton code from a SpecAST.

    Produces:
    - Type aliases for TypeDecls
    - Function skeletons with NotImplementedError for FuncDecls

    The generated code is the starting point for TDD (Phase A-3):
    auto-generated tests from pytest_gen will fail until these
    skeletons are implemented.

    Args:
        spec: Parsed specification.

    Returns:
        Python source code as a string.
    """
    sections: list[str] = []

    sections.append('"""Auto-generated implementation skeletons from DSL specification.')
    sections.append("")
    sections.append("TDD: all functions raise NotImplementedError.")
    sections.append("Run auto-generated tests, then implement until green.")
    sections.append('"""')
    sections.append("")
    sections.append("from __future__ import annotations")
    sections.append("")

    for item in spec.items:
        if isinstance(item, TypeDecl):
            sections.append(_gen_type_alias(item))
        elif isinstance(item, FuncDecl):
            sections.append(_gen_func_skeleton(item))

    return "\n".join(sections)
