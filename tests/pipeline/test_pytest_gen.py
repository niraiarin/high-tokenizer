"""Tests for automatic pytest test generation from FuncSpec."""

from pipeline.dsl.ast import (
    FuncDecl,
    FuncExpr,
    ParamExpr,
    SpecAST,
    TypeDecl,
    TypeExpr,
)
from pipeline.testgen.pytest_gen import generate_tests


class TestGenerateTests:
    def test_generates_test_function(self) -> None:
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="transfer",
                        inputs=(ParamExpr("from_acct", "Int"),),
                        output="Bool",
                        pre=("(> from_acct 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_tests(spec)
        assert "def test_transfer" in code
        assert "pre-condition" in code.lower() or "from_acct" in code

    def test_generates_pre_condition_test(self) -> None:
        """Test = { x | pre(x) }: should generate inputs satisfying pre."""
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="add",
                        inputs=(ParamExpr("x", "Int"), ParamExpr("y", "Int")),
                        output="Int",
                        pre=("(> x 0)", "(> y 0)"),
                        post=(),
                    )
                ),
            )
        )
        code = generate_tests(spec)
        assert "def test_add" in code
        # Should reference pre-conditions
        assert "x" in code and "y" in code

    def test_empty_spec_no_tests(self) -> None:
        spec = SpecAST(items=())
        code = generate_tests(spec)
        assert "def test_" not in code

    def test_type_only_spec(self) -> None:
        """TypeDecls don't generate function tests."""
        spec = SpecAST(items=(TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),))
        code = generate_tests(spec)
        # May generate invariant tests but not function tests
        assert isinstance(code, str)

    def test_generated_code_is_valid_python(self) -> None:
        """Generated test code should be compilable Python."""
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="transfer",
                        inputs=(ParamExpr("from_acct", "Int"),),
                        output="Bool",
                        pre=("(> from_acct 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_tests(spec)
        compile(code, "<generated>", "exec")  # Should not raise
