"""Generate Lean 4 code from SpecAST.

Transforms SpecAST (parsed from DSL) into Lean 4 source code containing
TypeSpec and FuncSpec definitions that can be verified by the Lean compiler.

Corresponds to the AST → Lean step in the spec_system.md pipeline:
  DSL → AST → **Lean** → SMT → Test → LLM → Code → Lean proof
"""

from __future__ import annotations

from pipeline.dsl.ast import (
    FuncDecl,
    SpecAST,
    TypeDecl,
)


def _lean_safe_name(name: str) -> str:
    """Make a name safe for Lean identifiers (replace hyphens, etc.)."""
    return name.replace("-", "_").replace(" ", "_")


def _gen_type_spec(decl: TypeDecl) -> str:
    """Generate Lean TypeSpec definition from a TypeDecl."""
    t = decl.type_expr
    name = _lean_safe_name(t.name)
    lines = [
        f"/-- TypeSpec for {t.name}: base type {t.basetype} -/",
        f"def {name}_TypeSpec : TypeSpec where",
        f"  α := {t.basetype}",
    ]

    if t.predicates:
        pred_comment = ", ".join(t.predicates)
        lines.append(f"  inv := fun x => True  -- TODO: encode predicates: {pred_comment}")
    else:
        lines.append("  inv := fun _ => True")

    return "\n".join(lines)


def _gen_func_spec(decl: FuncDecl) -> str:
    """Generate Lean FuncSpec definition from a FuncDecl."""
    f = decl.func_expr
    name = _lean_safe_name(f.name)

    # Determine input/output type names
    input_types = [p.type_name for p in f.inputs]
    input_spec = f"{input_types[0]}_TypeSpec" if input_types else "default_TypeSpec"
    output_spec = f"{f.output}_TypeSpec" if f.output else "default_TypeSpec"

    pre_comment = ", ".join(f.pre) if f.pre else "True"
    post_comment = ", ".join(f.post) if f.post else "True"

    lines = [
        f"/-- FuncSpec for {f.name} -/",
        f"def {name}_FuncSpec : FuncSpec {input_spec} {output_spec} where",
        "  f := fun _ => default  -- placeholder implementation",
        f"  pre := fun _ => True  -- TODO: encode: {pre_comment}",
        f"  post := fun _ _ => True  -- TODO: encode: {post_comment}",
        "  sound := fun _ _ => trivial",
    ]

    return "\n".join(lines)


def generate_lean(spec: SpecAST) -> str:
    """Generate complete Lean 4 source file from a SpecAST.

    The generated code imports SpecSystem.Basic for TypeSpec/FuncSpec definitions
    and produces type/function specifications that the Lean compiler can check.

    Args:
        spec: Parsed specification AST.

    Returns:
        Lean 4 source code as a string.
    """
    sections: list[str] = []

    # Header
    sections.append("-- Auto-generated from DSL specification")
    sections.append("-- Do not edit manually; regenerate from .spec files")
    sections.append("")

    # Collect needed default TypeSpecs for output types
    output_types: set[str] = set()
    for item in spec.items:
        if isinstance(item, FuncDecl) and item.func_expr.output:
            output_types.add(item.func_expr.output)

    # Check which output types don't have explicit TypeDecls
    declared_types = {item.type_expr.name for item in spec.items if isinstance(item, TypeDecl)}
    missing_output_types = output_types - declared_types

    # Generate default TypeSpecs for undeclared output types
    for type_name in sorted(missing_output_types):
        safe_name = _lean_safe_name(type_name)
        sections.append(f"/-- Default TypeSpec for {type_name} -/")
        sections.append(f"def {safe_name}_TypeSpec : TypeSpec where")
        sections.append(f"  α := {type_name}")
        sections.append("  inv := fun _ => True")
        sections.append("")

    # Generate declarations
    for item in spec.items:
        if isinstance(item, TypeDecl):
            sections.append(_gen_type_spec(item))
            sections.append("")
        elif isinstance(item, FuncDecl):
            sections.append(_gen_func_spec(item))
            sections.append("")

    return "\n".join(sections)
