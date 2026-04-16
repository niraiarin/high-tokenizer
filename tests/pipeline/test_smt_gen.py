"""Tests for Z3 SMT query generation and refinement verification."""

from pipeline.codegen.smt_gen import check_constraints, check_refinement
from pipeline.dsl.ast import (
    FuncExpr,
    ParamExpr,
    SpecAST,
    TypeDecl,
    TypeExpr,
)


class TestCheckConstraints:
    def test_satisfiable_type_constraint(self) -> None:
        """(>= 0) on Int is satisfiable."""
        spec = SpecAST(items=(TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),))
        result = check_constraints(spec)
        assert result["UserId"].satisfiable is True

    def test_unsatisfiable_constraint(self) -> None:
        """(> x 0) AND (< x 0) is unsatisfiable."""
        spec = SpecAST(items=(TypeDecl(TypeExpr("Impossible", "Int", ("(> 0)", "(< 0)"))),))
        result = check_constraints(spec)
        assert result["Impossible"].satisfiable is False

    def test_no_constraints(self) -> None:
        """Type with no predicates is trivially satisfiable."""
        spec = SpecAST(items=(TypeDecl(TypeExpr("Name", "String", ())),))
        result = check_constraints(spec)
        assert result["Name"].satisfiable is True


class TestCheckRefinement:
    def test_identical_specs_refine(self) -> None:
        """f ≤ f (reflexivity)."""
        f = FuncExpr(
            name="f",
            inputs=(ParamExpr("x", "Int"),),
            output="Bool",
            pre=("(> x 0)",),
            post=("(= result true)",),
        )
        result = check_refinement(f, f)
        assert result.refines is True

    def test_weaker_pre_refines(self) -> None:
        """f with pre (> x 0) refines g with pre (> x 10).

        pre_g ⇒ pre_f: (> x 10) ⇒ (> x 0) ✓
        """
        f = FuncExpr(
            name="f",
            inputs=(ParamExpr("x", "Int"),),
            output="Bool",
            pre=("(> x 0)",),
            post=("(= result true)",),
        )
        g = FuncExpr(
            name="g",
            inputs=(ParamExpr("x", "Int"),),
            output="Bool",
            pre=("(> x 10)",),
            post=("(= result true)",),
        )
        result = check_refinement(f, g)
        assert result.refines is True

    def test_stronger_pre_does_not_refine(self) -> None:
        """f with pre (> x 10) does NOT refine g with pre (> x 0).

        pre_g ⇒ pre_f: (> x 0) ⇏ (> x 10) ✗
        """
        f = FuncExpr(
            name="f",
            inputs=(ParamExpr("x", "Int"),),
            output="Bool",
            pre=("(> x 10)",),
            post=("(= result true)",),
        )
        g = FuncExpr(
            name="g",
            inputs=(ParamExpr("x", "Int"),),
            output="Bool",
            pre=("(> x 0)",),
            post=("(= result true)",),
        )
        result = check_refinement(f, g)
        assert result.refines is False
