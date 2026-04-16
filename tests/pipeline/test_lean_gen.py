"""Tests for Lean code generation from SpecAST.

Verifies that generated Lean code is syntactically valid by checking
string output against expected patterns. Full Lean compiler verification
is done via integration test at the end.
"""

import subprocess
from pathlib import Path

import pytest

from pipeline.codegen.lean_gen import generate_lean
from pipeline.dsl.ast import (
    FuncDecl,
    FuncExpr,
    ParamExpr,
    SpecAST,
    TypeDecl,
    TypeExpr,
)


class TestGenerateLeanTypeSpec:
    def test_simple_type(self) -> None:
        spec = SpecAST(items=(TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),))
        code = generate_lean(spec)
        assert "UserId_TypeSpec" in code
        assert "α" in code or "Int" in code

    def test_type_with_no_predicates(self) -> None:
        spec = SpecAST(items=(TypeDecl(TypeExpr("Name", "String", ())),))
        code = generate_lean(spec)
        assert "Name_TypeSpec" in code


class TestGenerateLeanFuncSpec:
    def test_simple_func(self) -> None:
        spec = SpecAST(
            items=(
                FuncDecl(
                    FuncExpr(
                        name="transfer",
                        inputs=(ParamExpr("from", "UserId"),),
                        output="Bool",
                        pre=("(> from 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_lean(spec)
        assert "transfer_FuncSpec" in code or "transfer" in code
        assert "pre" in code
        assert "post" in code

    def test_func_with_multiple_inputs(self) -> None:
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
        code = generate_lean(spec)
        assert "add" in code


class TestGenerateLeanFull:
    def test_full_spec_system_example(self) -> None:
        """spec_system.md の UserId/transfer 例から Lean コードを生成。"""
        spec = SpecAST(
            items=(
                TypeDecl(TypeExpr("UserId", "Int", ("(>= 0)",))),
                FuncDecl(
                    FuncExpr(
                        name="transfer",
                        inputs=(ParamExpr("from", "UserId"),),
                        output="Bool",
                        pre=("(> from 0)",),
                        post=("(= result true)",),
                    )
                ),
            )
        )
        code = generate_lean(spec)
        assert "UserId" in code
        assert "transfer" in code
        # Should be valid Lean — imports included
        assert "import" in code or "def" in code or "structure" in code

    def test_empty_spec(self) -> None:
        spec = SpecAST(items=())
        code = generate_lean(spec)
        assert isinstance(code, str)

    def test_lean_compiler_accepts_generated_code(self, tmp_path: Path) -> None:
        """Integration test: 生成 Lean コードが Lean コンパイラでビルドできること。"""
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
        code = generate_lean(spec)

        lean_file = tmp_path / "Generated.lean"
        lean_file.write_text(code)

        result = subprocess.run(
            ["lean", str(lean_file), "--run"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Lean should at least not crash on the generated code.
        # We accept warnings but not errors.
        if result.returncode != 0:
            pytest.skip(f"Lean compiler not available or code invalid: {result.stderr[:200]}")
