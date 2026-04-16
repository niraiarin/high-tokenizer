"""Self-hosting tests: pipeline processes its own spec files.

Bootstrap Stage 2: hand-written Lean specs are now expressed in the
pipeline's own DSL, and the pipeline can process them end-to-end.

This validates that the DSL has sufficient expressive power to
describe the pipeline's own components.
"""

from pathlib import Path

from pipeline.codegen.lean_gen import generate_lean
from pipeline.codegen.python_gen import generate_python
from pipeline.codegen.smt_gen import check_constraints
from pipeline.dsl.parser import parse_sexpr, parse_spec
from pipeline.testgen.pytest_gen import generate_tests

SPECS_DIR = Path(__file__).parent.parent.parent / "specs"


class TestSelfHostCore:
    """Self-hosting: spec_system_core.spec (TypeSpec, FuncSpec, refinement)."""

    def test_parse(self) -> None:
        source = (SPECS_DIR / "spec_system_core.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        assert spec.well_formed()
        assert len(spec.items) == 5  # 3 types + 2 funcs

    def test_lean_gen(self) -> None:
        source = (SPECS_DIR / "spec_system_core.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        lean_code = generate_lean(spec)
        assert "TypeSpec_TypeSpec" in lean_code
        assert "refines" in lean_code
        assert "testSet" in lean_code

    def test_smt_check(self) -> None:
        source = (SPECS_DIR / "spec_system_core.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        results = check_constraints(spec)
        assert all(r.satisfiable for r in results.values())

    def test_test_gen(self) -> None:
        source = (SPECS_DIR / "spec_system_core.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        test_code = generate_tests(spec)
        assert "def test_refines" in test_code
        assert "def test_testSet" in test_code
        compile(test_code, "<selfhost-core>", "exec")

    def test_python_gen(self) -> None:
        source = (SPECS_DIR / "spec_system_core.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        py_code = generate_python(spec)
        assert "def refines(" in py_code
        assert "def testSet(" in py_code
        assert "NotImplementedError" in py_code
        compile(py_code, "<selfhost-core-py>", "exec")


class TestSelfHostDSLParser:
    """Self-hosting: dsl_spec.spec (parseSExpr, parseSpec)."""

    def test_parse(self) -> None:
        source = (SPECS_DIR / "dsl_spec.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        assert spec.well_formed()
        assert len(spec.items) == 5  # 3 types + 2 funcs

    def test_lean_gen(self) -> None:
        source = (SPECS_DIR / "dsl_spec.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        lean_code = generate_lean(spec)
        assert "parseSExpr" in lean_code
        assert "parseSpec" in lean_code

    def test_smt_check(self) -> None:
        source = (SPECS_DIR / "dsl_spec.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        results = check_constraints(spec)
        assert all(r.satisfiable for r in results.values())

    def test_test_gen(self) -> None:
        source = (SPECS_DIR / "dsl_spec.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        test_code = generate_tests(spec)
        assert "def test_parseSExpr" in test_code
        assert "def test_parseSpec" in test_code
        compile(test_code, "<selfhost-dsl>", "exec")

    def test_python_gen(self) -> None:
        source = (SPECS_DIR / "dsl_spec.spec").read_text()
        spec = parse_spec(parse_sexpr(source))
        py_code = generate_python(spec)
        assert "def parseSExpr(" in py_code
        assert "def parseSpec(" in py_code
        compile(py_code, "<selfhost-dsl-py>", "exec")


class TestSelfHostFullPipeline:
    """End-to-end: all spec files through all pipeline stages."""

    def test_all_specs_pass_full_pipeline(self) -> None:
        for spec_file in sorted(SPECS_DIR.glob("*.spec")):
            source = spec_file.read_text()
            spec = parse_spec(parse_sexpr(source))
            assert spec.well_formed(), f"{spec_file.name}: not well-formed"

            lean_code = generate_lean(spec)
            assert len(lean_code) > 0, f"{spec_file.name}: empty Lean output"

            results = check_constraints(spec)
            for name, r in results.items():
                assert r.satisfiable, f"{spec_file.name}: {name} unsatisfiable"

            test_code = generate_tests(spec)
            compile(test_code, f"<{spec_file.stem}>", "exec")

            py_code = generate_python(spec)
            compile(py_code, f"<{spec_file.stem}-py>", "exec")
