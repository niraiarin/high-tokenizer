"""Tests for Python skeleton code generation from SpecAST."""

from pipeline.codegen.python_gen import generate_python
from pipeline.dsl.ast import (
    FuncDecl,
    FuncExpr,
    ParamExpr,
    SpecAST,
    TypeDecl,
    TypeExpr,
)


class TestGeneratePythonSkeleton:
    def test_func_skeleton(self) -> None:
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
        code = generate_python(spec)
        assert "def transfer(" in code
        assert "from_acct" in code
        assert "NotImplementedError" in code

    def test_func_with_type_hints(self) -> None:
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="add",
                        inputs=(ParamExpr("x", "Int"), ParamExpr("y", "Int")),
                        output="Int",
                        pre=(),
                        post=(),
                    )
                ),
            )
        )
        code = generate_python(spec)
        assert "def add(" in code
        assert "int" in code  # type hint mapped

    def test_type_generates_dataclass(self) -> None:
        spec = SpecAST(items=(TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),))
        code = generate_python(spec)
        # Should generate a type alias or NewType
        assert "UserId" in code

    def test_full_spec_system_example(self) -> None:
        spec = SpecAST(
            items=(
                TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),
                FuncDecl(
                    FuncExpr(
                        name="transfer",
                        inputs=(ParamExpr("from_acct", "UserId"),),
                        output="Bool",
                        pre=("(> from_acct 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_python(spec)
        assert "UserId" in code
        assert "def transfer(" in code
        compile(code, "<generated>", "exec")

    def test_empty_spec(self) -> None:
        code = generate_python(SpecAST(items=()))
        assert isinstance(code, str)
        compile(code, "<generated>", "exec")

    def test_docstring_includes_pre_post(self) -> None:
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="validate",
                        inputs=(ParamExpr("x", "Int"),),
                        output="Bool",
                        pre=("(> x 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_python(spec)
        assert "Pre:" in code or "pre" in code.lower()
        assert "Post:" in code or "post" in code.lower()
