"""Tests for DSL parser, derived from Lean FuncSpec.

Test derivation from SpecSystem/DSL/Spec.lean:
- parseSExprSpec: pre = isWellFormedSExpr, post = True (structural correctness)
- parseSpecSpec: pre = isSpecSExpr, post = wellFormed
- testSet = { x | pre(x) }

Test categories (from 04_implementation_spec.md §11.4):
- Normal: well-formed S-expressions with valid spec structure
- Boundary: empty lists, deep nesting, edge cases
- Error: malformed brackets, unknown keywords
"""

import pytest

from pipeline.dsl.ast import (
    Atom,
    FuncDecl,
    ParamExpr,
    SList,
    SpecAST,
    TypeDecl,
)
from pipeline.dsl.parser import parse_sexpr, parse_spec

# ============================================================
# S-expression parser tests (from parseSExprSpec)
# pre: isWellFormedSExpr — input is non-empty well-formed S-expr
# ============================================================


class TestParseSExpr:
    """Tests derived from parseSExprSpec.pre = isWellFormedSExpr."""

    # --- Normal cases ---

    def test_atom(self) -> None:
        assert parse_sexpr("hello") == Atom("hello")

    def test_number_atom(self) -> None:
        assert parse_sexpr("42") == Atom("42")

    def test_empty_list(self) -> None:
        assert parse_sexpr("()") == SList(())

    def test_simple_list(self) -> None:
        assert parse_sexpr("(a b c)") == SList((Atom("a"), Atom("b"), Atom("c")))

    def test_nested_list(self) -> None:
        result = parse_sexpr("(a (b c))")
        assert result == SList((Atom("a"), SList((Atom("b"), Atom("c")))))

    def test_spec_system_example(self) -> None:
        """spec_system.md §3 の例がパースできること。"""
        source = """(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from UserId))
    (output Bool)
    (pre (> from 0))
    (post (= result true))))"""
        result = parse_sexpr(source)
        assert isinstance(result, SList)
        assert len(result.items) == 3  # spec, type decl, func decl
        assert result.items[0] == Atom("spec")

    # --- Boundary cases ---

    def test_whitespace_handling(self) -> None:
        assert parse_sexpr("  hello  ") == Atom("hello")

    def test_multiline(self) -> None:
        result = parse_sexpr("(a\n  b\n  c)")
        assert result == SList((Atom("a"), Atom("b"), Atom("c")))

    def test_deeply_nested(self) -> None:
        result = parse_sexpr("(((a)))")
        assert result == SList((SList((SList((Atom("a"),)),)),))

    def test_operators_as_atoms(self) -> None:
        result = parse_sexpr("(>= x 0)")
        assert result == SList((Atom(">="), Atom("x"), Atom("0")))

    # --- Error cases ---

    def test_empty_string_raises(self) -> None:
        """pre violation: empty string is not well-formed."""
        with pytest.raises(ValueError):
            parse_sexpr("")

    def test_unmatched_open_paren(self) -> None:
        with pytest.raises(ValueError):
            parse_sexpr("(a b")

    def test_unmatched_close_paren(self) -> None:
        with pytest.raises(ValueError):
            parse_sexpr("a b)")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_sexpr("   ")


# ============================================================
# Spec parser tests (from parseSpecSpec)
# pre: isSpecSExpr — input is (spec ...) form
# post: wellFormed — output SpecAST is well-formed
# ============================================================


class TestParseSpec:
    """Tests derived from parseSpecSpec.pre = isSpecSExpr, post = wellFormed."""

    def test_empty_spec(self) -> None:
        sexpr = SList((Atom("spec"),))
        result = parse_spec(sexpr)
        assert result == SpecAST(items=())
        assert result.well_formed()

    def test_type_decl(self) -> None:
        sexpr = SList(
            (
                Atom("spec"),
                SList((Atom("type"), Atom("UserId"), Atom("Int"), SList((Atom(">="), Atom("0"))))),
            )
        )
        result = parse_spec(sexpr)
        assert len(result.items) == 1
        item = result.items[0]
        assert isinstance(item, TypeDecl)
        assert item.type_expr.name == "UserId"
        assert item.type_expr.basetype == "Int"
        assert result.well_formed()

    def test_func_decl(self) -> None:
        sexpr = SList(
            (
                Atom("spec"),
                SList(
                    (
                        Atom("func"),
                        Atom("transfer"),
                        SList((Atom("input"), SList((Atom("from"), Atom("UserId"))))),
                        SList((Atom("output"), Atom("Bool"))),
                        SList((Atom("pre"), SList((Atom(">"), Atom("from"), Atom("0"))))),
                        SList((Atom("post"), SList((Atom("="), Atom("result"), Atom("true"))))),
                    )
                ),
            )
        )
        result = parse_spec(sexpr)
        assert len(result.items) == 1
        item = result.items[0]
        assert isinstance(item, FuncDecl)
        assert item.func_expr.name == "transfer"
        assert item.func_expr.inputs == (ParamExpr("from", "UserId"),)
        assert item.func_expr.output == "Bool"
        assert result.well_formed()

    def test_full_spec_system_example(self) -> None:
        """spec_system.md §3 の完全な例: type + func を含む spec。"""
        source = """(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from UserId))
    (output Bool)
    (pre (> from 0))
    (post (= result true))))"""
        sexpr = parse_sexpr(source)
        result = parse_spec(sexpr)
        assert len(result.items) == 2
        assert isinstance(result.items[0], TypeDecl)
        assert isinstance(result.items[1], FuncDecl)
        assert result.well_formed()

    # --- Error cases ---

    def test_non_spec_sexpr_raises(self) -> None:
        """pre violation: input is not (spec ...) form."""
        with pytest.raises(ValueError):
            parse_spec(SList((Atom("notspec"),)))

    def test_atom_input_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_spec(Atom("spec"))

    def test_unknown_decl_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_spec(SList((Atom("spec"), SList((Atom("unknown"), Atom("x"))))))
