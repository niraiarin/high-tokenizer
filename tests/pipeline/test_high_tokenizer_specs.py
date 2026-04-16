"""Tests for high-tokenizer formal specifications.

Phase A-2: spec-driven + test-driven specification of all components.
Each spec file is processed through the full pipeline:
  DSL → parse → Lean gen → SMT check → test gen → Python gen
"""

from pathlib import Path

import pytest

from pipeline.codegen.lean_gen import generate_lean
from pipeline.codegen.python_gen import generate_python
from pipeline.codegen.smt_gen import check_constraints
from pipeline.dsl.parser import parse_sexpr, parse_spec
from pipeline.testgen.pytest_gen import generate_tests

HT_SPECS_DIR = Path(__file__).parent.parent.parent / "specs" / "high_tokenizer"

# Collect all spec files
SPEC_FILES = sorted(HT_SPECS_DIR.glob("*.spec")) if HT_SPECS_DIR.exists() else []


@pytest.mark.parametrize("spec_file", SPEC_FILES, ids=lambda p: p.stem)
class TestHighTokenizerSpecs:
    """Parametrized tests: each spec file goes through full pipeline."""

    def test_parse(self, spec_file: Path) -> None:
        source = spec_file.read_text()
        spec = parse_spec(parse_sexpr(source))
        assert spec.well_formed(), f"{spec_file.name}: not well-formed"

    def test_lean_gen(self, spec_file: Path) -> None:
        source = spec_file.read_text()
        spec = parse_spec(parse_sexpr(source))
        lean_code = generate_lean(spec)
        assert len(lean_code) > 50, f"{spec_file.name}: Lean output too short"

    def test_smt_satisfiable(self, spec_file: Path) -> None:
        source = spec_file.read_text()
        spec = parse_spec(parse_sexpr(source))
        results = check_constraints(spec)
        for name, r in results.items():
            assert r.satisfiable, f"{spec_file.name}: {name} unsatisfiable"

    def test_test_gen_compiles(self, spec_file: Path) -> None:
        source = spec_file.read_text()
        spec = parse_spec(parse_sexpr(source))
        test_code = generate_tests(spec)
        compile(test_code, f"<{spec_file.stem}-tests>", "exec")

    def test_python_gen_compiles(self, spec_file: Path) -> None:
        source = spec_file.read_text()
        spec = parse_spec(parse_sexpr(source))
        py_code = generate_python(spec)
        compile(py_code, f"<{spec_file.stem}-impl>", "exec")


class TestHighTokenizerSpecsSummary:
    """Summary test: all spec files present and consistent."""

    def test_all_components_have_specs(self) -> None:
        expected = {
            "domain_model",
            "complexity_estimator",
            "type_system",
            "mdl_evaluator",
            "constraint_validator",
            "engines",
        }
        actual = {f.stem for f in SPEC_FILES}
        missing = expected - actual
        assert not missing, f"Missing spec files: {missing}"

    def test_all_specs_pass_full_pipeline(self) -> None:
        for spec_file in SPEC_FILES:
            source = spec_file.read_text()
            spec = parse_spec(parse_sexpr(source))
            assert spec.well_formed()
            assert all(r.satisfiable for r in check_constraints(spec).values())
            compile(generate_tests(spec), f"<{spec_file.stem}>", "exec")
            compile(generate_python(spec), f"<{spec_file.stem}>", "exec")
