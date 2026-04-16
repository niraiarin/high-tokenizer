"""Z3 SMT query generation and constraint/refinement verification.

Corresponds to the AST → SMT step in the spec_system.md pipeline:
  DSL → AST → Lean → **SMT** → Test → LLM → Code → Lean proof

Also implements refinement partial order verification (spec_system.md §4):
  f ≤ g ⟺ pre_g ⇒ pre_f ∧ post_f ⇒ post_g
"""

from __future__ import annotations

from dataclasses import dataclass

import z3

from pipeline.dsl.ast import (
    FuncExpr,
    SpecAST,
    TypeDecl,
)


@dataclass(frozen=True)
class ConstraintResult:
    """Result of checking type constraints."""

    satisfiable: bool
    model: str | None = None


@dataclass(frozen=True)
class RefinementResult:
    """Result of checking refinement f ≤ g."""

    refines: bool
    counterexample: str | None = None


def _parse_predicate_to_z3(pred_str: str, var: z3.ArithRef) -> z3.BoolRef | None:
    """Parse a simple predicate string like '(> x 0)' or '(>= 0)' into a Z3 expression.

    Supports: >, >=, <, <=, = with numeric literals.
    """
    # Strip outer parens
    pred = pred_str.strip()
    if pred.startswith("(") and pred.endswith(")"):
        pred = pred[1:-1].strip()

    parts = pred.split()
    if len(parts) < 2:
        return None

    op = parts[0]

    # Find the numeric value (could be 2nd or 3rd token)
    value = None
    for p in parts[1:]:
        try:
            value = int(p)
            break
        except ValueError:
            continue

    if value is None:
        return None

    ops = {
        ">": lambda v, val: v > val,
        ">=": lambda v, val: v >= val,
        "<": lambda v, val: v < val,
        "<=": lambda v, val: v <= val,
        "=": lambda v, val: v == val,
        "!=": lambda v, val: v != val,
    }

    if op in ops:
        return ops[op](var, value)
    return None


def check_constraints(spec: SpecAST) -> dict[str, ConstraintResult]:
    """Check satisfiability of type constraints using Z3.

    For each TypeDecl, checks if its predicates are simultaneously satisfiable.

    Args:
        spec: Parsed specification.

    Returns:
        Dict mapping type name → ConstraintResult.
    """
    results: dict[str, ConstraintResult] = {}

    for item in spec.items:
        if not isinstance(item, TypeDecl):
            continue

        t = item.type_expr
        solver = z3.Solver()
        x = z3.Int("x")

        if not t.predicates:
            results[t.name] = ConstraintResult(satisfiable=True)
            continue

        constraints = []
        for pred in t.predicates:
            z3_expr = _parse_predicate_to_z3(pred, x)
            if z3_expr is not None:
                constraints.append(z3_expr)

        if not constraints:
            results[t.name] = ConstraintResult(satisfiable=True)
            continue

        solver.add(*constraints)
        if solver.check() == z3.sat:
            model = solver.model()
            results[t.name] = ConstraintResult(satisfiable=True, model=str(model))
        else:
            results[t.name] = ConstraintResult(satisfiable=False)

    return results


def check_refinement(f: FuncExpr, g: FuncExpr) -> RefinementResult:
    """Check if f refines g using Z3.

    f ≤ g ⟺ (∀x. pre_g(x) ⇒ pre_f(x)) ∧ (∀x,y. post_f(x,y) ⇒ post_g(x,y))

    We check the negation: ¬(f ≤ g) iff ∃x where pre_g(x) ∧ ¬pre_f(x),
    or ∃x,y where post_f(x,y) ∧ ¬post_g(x,y).

    For simplicity, we currently only check pre-condition weakening
    (the first conjunct), since post-conditions in our DSL are
    string expressions not yet fully parseable to Z3.

    Args:
        f: The candidate refinement.
        g: The specification being refined.

    Returns:
        RefinementResult indicating whether f ≤ g holds.
    """
    solver = z3.Solver()
    x = z3.Int("x")

    # Check pre_g ⇒ pre_f by checking unsatisfiability of pre_g ∧ ¬pre_f
    pre_f_exprs = [_parse_predicate_to_z3(p, x) for p in f.pre]
    pre_g_exprs = [_parse_predicate_to_z3(p, x) for p in g.pre]

    pre_f_z3 = [e for e in pre_f_exprs if e is not None]
    pre_g_z3 = [e for e in pre_g_exprs if e is not None]

    if not pre_f_z3 and not pre_g_z3:
        # Both have trivial preconditions
        return RefinementResult(refines=True)

    if not pre_g_z3:
        # g has trivial precondition, f refines g iff f also has trivial precondition
        return RefinementResult(refines=not pre_f_z3)

    # Check: ∃x. pre_g(x) ∧ ¬pre_f(x)  (counterexample to pre_g ⇒ pre_f)
    for pg in pre_g_z3:
        solver.add(pg)

    if pre_f_z3:
        # Negate conjunction of pre_f
        solver.add(z3.Not(z3.And(*pre_f_z3)))
    else:
        # pre_f is trivially True, so ¬pre_f is False — no counterexample
        return RefinementResult(refines=True)

    if solver.check() == z3.sat:
        model = solver.model()
        return RefinementResult(refines=False, counterexample=str(model))

    return RefinementResult(refines=True)
