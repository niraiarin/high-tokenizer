"""Generate Lean 4 code from SpecAST.

Transforms SpecAST (parsed from DSL) into Lean 4 source code containing
TypeSpec and FuncSpec definitions that can be verified by the Lean compiler.

Corresponds to the AST → Lean step in the spec_system.md pipeline:
  DSL → AST → **Lean** → SMT → Test → LLM → Code → Lean proof
"""

from __future__ import annotations

from pipeline.dsl.ast import (
    Atom,
    FuncDecl,
    SExpr,
    SList,
    SpecAST,
    TypeDecl,
)
from pipeline.dsl.parser import parse_sexpr


def _lean_safe_name(name: str) -> str:
    """Make a name safe for Lean identifiers (replace hyphens, etc.)."""
    return name.replace("-", "_").replace(" ", "_")


# ============================================================
# Predicate template library (#6)
# Converts DSL predicate S-expressions to Lean Prop strings.
# ============================================================

_LEAN_OPS: dict[str, str] = {
    ">": ">",
    ">=": "≥",
    "<": "<",
    "<=": "≤",
    "=": "=",
    "!=": "≠",
}


def _pred_to_lean(pred_str: str, var: str = "x") -> str | None:
    """Convert a predicate string like '(> x 0)' to a Lean expression.

    Supports: comparison operators with numeric literals.
    Returns None if the predicate can't be parsed.
    """
    try:
        sexpr = parse_sexpr(pred_str)
    except ValueError:
        return None

    return _sexpr_pred_to_lean(sexpr, var)


def _sexpr_pred_to_lean(sexpr: SExpr, default_var: str = "x") -> str | None:
    """Convert a parsed predicate SExpr to Lean Prop string."""
    if not isinstance(sexpr, SList) or len(sexpr.items) < 2:
        return None

    op_node = sexpr.items[0]
    if not isinstance(op_node, Atom):
        return None

    op = op_node.value

    # Logical connectives
    if op == "and" and len(sexpr.items) >= 3:
        parts = [_sexpr_pred_to_lean(item, default_var) for item in sexpr.items[1:]]
        valid = [p for p in parts if p is not None]
        return " ∧ ".join(valid) if valid else None

    if op == "or" and len(sexpr.items) >= 3:
        parts = [_sexpr_pred_to_lean(item, default_var) for item in sexpr.items[1:]]
        valid = [p for p in parts if p is not None]
        return " ∨ ".join(valid) if valid else None

    if op == "not" and len(sexpr.items) == 2:
        inner = _sexpr_pred_to_lean(sexpr.items[1], default_var)
        return f"¬({inner})" if inner else None

    # Comparison operators
    if op in _LEAN_OPS and len(sexpr.items) >= 2:
        lean_op = _LEAN_OPS[op]
        args = sexpr.items[1:]

        # 2-token form: (>= 0) → x ≥ 0
        if len(args) == 1 and isinstance(args[0], Atom):
            return f"{default_var} {lean_op} {args[0].value}"

        # 3-token form: (> x 0) → x > 0
        if len(args) == 2 and isinstance(args[0], Atom) and isinstance(args[1], Atom):
            return f"{args[0].value} {lean_op} {args[1].value}"

    return None


# ============================================================
# Type and function spec generation
# ============================================================


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
        lean_preds = [_pred_to_lean(p, "x") for p in t.predicates]
        valid_preds = [p for p in lean_preds if p is not None]
        if valid_preds:
            inv_expr = " ∧ ".join(valid_preds)
            lines.append(f"  inv := fun x => {inv_expr}")
        else:
            pred_comment = ", ".join(t.predicates)
            lines.append(f"  inv := fun x => True  -- unparseable predicates: {pred_comment}")
    else:
        lines.append("  inv := fun _ => True")

    return "\n".join(lines)


def _gen_func_spec(decl: FuncDecl) -> str:
    """Generate Lean FuncSpec definition from a FuncDecl."""
    f = decl.func_expr
    name = _lean_safe_name(f.name)

    # (#3) Product type for multi-input functions
    input_types = [_lean_safe_name(p.type_name) for p in f.inputs]
    product_comment = ""
    if len(input_types) == 0:
        input_spec = "default_TypeSpec"
    elif len(input_types) == 1:
        input_spec = f"{input_types[0]}_TypeSpec"
    else:
        # Multi-input: generate product TypeSpec inline comment, use first for now
        # Full product type support requires TypeSpec for (A × B), deferred to eDSL
        input_spec = f"{input_types[0]}_TypeSpec"
        type_list = ", ".join(input_types)
        product_comment = (
            f"  -- NOTE: multi-input ({type_list}), first type only. Product type in eDSL (#21)"
        )

    output_spec = f"{_lean_safe_name(f.output)}_TypeSpec" if f.output else "default_TypeSpec"

    # (#6) Predicate encoding
    param_names = [p.name for p in f.inputs]
    lambda_var = param_names[0] if param_names else "_"

    pre_exprs = [_pred_to_lean(p, lambda_var) for p in f.pre]
    valid_pre = [p for p in pre_exprs if p is not None]
    if valid_pre:
        pre_str = " ∧ ".join(valid_pre)
        pre_line = f"  pre := fun {lambda_var} => {pre_str}"
    else:
        pre_line = "  pre := fun _ => True"

    post_exprs = [_pred_to_lean(p, "y") for p in f.post]
    valid_post = [p for p in post_exprs if p is not None]
    if valid_post:
        post_str = " ∧ ".join(valid_post)
        post_line = f"  post := fun _ y => {post_str}"
    else:
        post_line = "  post := fun _ _ => True"

    lines = [
        f"/-- FuncSpec for {f.name} -/",
    ]
    if len(input_types) > 1 and product_comment:
        lines.append(product_comment)
    lines.extend(
        [
            f"def {name}_FuncSpec : FuncSpec {input_spec} {output_spec} where",
            "  f := fun _ => default  -- placeholder implementation",
            pre_line,
            post_line,
            "  sound := by sorry  -- proof obligation: implementation must satisfy post",
        ]
    )

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

    # Header + import
    sections.append("import SpecSystem.Basic")
    sections.append("")
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
