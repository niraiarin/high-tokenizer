"""Dogfooding test: the pipeline processes its own DSL parser spec.

This is the bootstrap Stage 1 transition point: the pipeline uses itself
to specify, verify, and generate tests for its own components.
"""

from pathlib import Path

from pipeline.codegen.lean_gen import generate_lean
from pipeline.codegen.smt_gen import check_constraints
from pipeline.dsl.parser import parse_sexpr, parse_spec
from pipeline.testgen.pytest_gen import generate_tests

SPEC_FILE = Path(__file__).parent.parent.parent / "specs" / "dsl_parser.spec"


class TestDogfoodPipeline:
    """Full pipeline: DSL → AST → Lean → SMT → Test."""

    def test_parse_own_spec(self) -> None:
        """Step 1: DSL → AST — パイプラインが自分の仕様をパースできる。"""
        source = SPEC_FILE.read_text()
        sexpr = parse_sexpr(source)
        spec = parse_spec(sexpr)
        assert spec.well_formed()
        assert len(spec.items) == 3  # 2 types + 1 func

    def test_generate_lean_from_own_spec(self) -> None:
        """Step 2: AST → Lean — 自分の仕様から Lean コードを生成。"""
        source = SPEC_FILE.read_text()
        spec = parse_spec(parse_sexpr(source))
        lean_code = generate_lean(spec)
        assert "SExprInput_TypeSpec" in lean_code
        assert "parse_sexpr" in lean_code

    def test_smt_check_own_constraints(self) -> None:
        """Step 3: AST → SMT — 自分の型制約が充足可能。"""
        source = SPEC_FILE.read_text()
        spec = parse_spec(parse_sexpr(source))
        results = check_constraints(spec)
        assert results["SExprInput"].satisfiable is True
        assert results["SExprOutput"].satisfiable is True

    def test_generate_tests_from_own_spec(self) -> None:
        """Step 4: AST → Test — 自分の仕様からテストを自動生成。"""
        source = SPEC_FILE.read_text()
        spec = parse_spec(parse_sexpr(source))
        test_code = generate_tests(spec)
        assert "def test_parse_sexpr" in test_code
        compile(test_code, "<dogfood-generated>", "exec")

    def test_full_pipeline_end_to_end(self) -> None:
        """Full pipeline: DSL file → parse → Lean + SMT + Test."""
        source = SPEC_FILE.read_text()

        # DSL → AST
        spec = parse_spec(parse_sexpr(source))
        assert spec.well_formed()

        # AST → Lean
        lean_code = generate_lean(spec)
        assert len(lean_code) > 0

        # AST → SMT
        constraints = check_constraints(spec)
        assert all(r.satisfiable for r in constraints.values())

        # AST → Test
        test_code = generate_tests(spec)
        assert "def test_" in test_code
        compile(test_code, "<e2e>", "exec")
