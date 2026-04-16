"""Generate Python tests and implementation skeletons from all spec files.

Usage:
    uv run python scripts/generate_from_specs.py

Reads specs/high_tokenizer/*.spec and generates:
- tests/high_tokenizer/test_{name}.py  (auto-generated tests)
- high_tokenizer/{name}.py             (implementation skeletons)
"""

from pathlib import Path

from pipeline.codegen.python_gen import generate_python
from pipeline.dsl.parser import parse_sexpr, parse_spec
from pipeline.testgen.pytest_gen import generate_tests

SPECS_DIR = Path("specs/high_tokenizer")
TESTS_DIR = Path("tests/high_tokenizer")
IMPL_DIR = Path("high_tokenizer")


def main() -> None:
    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    for spec_file in sorted(SPECS_DIR.glob("*.spec")):
        name = spec_file.stem
        source = spec_file.read_text()
        spec_ast = parse_spec(parse_sexpr(source))

        # Generate tests
        test_code = generate_tests(spec_ast)
        test_file = TESTS_DIR / f"test_{name}.py"
        test_file.write_text(test_code)
        print(f"  tests: {test_file}")

        # Generate implementation skeleton
        impl_code = generate_python(spec_ast)
        impl_file = IMPL_DIR / f"{name}.py"
        impl_file.write_text(impl_code)
        print(f"  impl:  {impl_file}")

    print(f"\nGenerated from {len(list(SPECS_DIR.glob('*.spec')))} spec files.")


if __name__ == "__main__":
    main()
