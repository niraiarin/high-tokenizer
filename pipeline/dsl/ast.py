"""AST data structures for the spec DSL.

Mirrors the Lean definitions in SpecSystem/DSL/AST.lean.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- S-expression layer (raw parse output) ---


@dataclass(frozen=True)
class SExpr:
    """Base class for S-expression nodes. Mirrors Lean `SExpr`."""


@dataclass(frozen=True)
class Atom(SExpr):
    """Atomic value. Mirrors `SExpr.atom`."""

    value: str


@dataclass(frozen=True)
class SList(SExpr):
    """List of S-expressions. Mirrors `SExpr.list`."""

    items: tuple[SExpr, ...] = ()


# --- Spec AST layer (structured parse output) ---


@dataclass(frozen=True)
class ParamExpr:
    """Parameter: name and type. Mirrors Lean `ParamExpr`."""

    name: str
    type_name: str


@dataclass(frozen=True)
class TypeExpr:
    """Type declaration. Mirrors Lean `TypeExpr`."""

    name: str
    basetype: str
    predicates: tuple[str, ...] = ()

    def well_formed(self) -> bool:
        """Mirrors Lean `TypeExpr.wellFormed`."""
        return self.name != "" and self.basetype != ""


@dataclass(frozen=True)
class FuncExpr:
    """Function declaration. Mirrors Lean `FuncExpr`."""

    name: str
    inputs: tuple[ParamExpr, ...] = ()
    output: str = ""
    pre: tuple[str, ...] = ()
    post: tuple[str, ...] = ()

    def well_formed(self) -> bool:
        """Mirrors Lean `FuncExpr.wellFormed`."""
        return self.name != "" and len(self.inputs) > 0


@dataclass(frozen=True)
class SpecItem:
    """Base for spec items. Mirrors Lean `SpecItem`."""


@dataclass(frozen=True)
class TypeDecl(SpecItem):
    """Type declaration item. Mirrors `SpecItem.typeDecl`."""

    type_expr: TypeExpr = field(default_factory=lambda: TypeExpr("", ""))


@dataclass(frozen=True)
class FuncDecl(SpecItem):
    """Function declaration item. Mirrors `SpecItem.funcDecl`."""

    func_expr: FuncExpr = field(default_factory=lambda: FuncExpr(""))


@dataclass(frozen=True)
class SpecAST:
    """Top-level spec. Mirrors Lean `SpecAST`."""

    items: tuple[SpecItem, ...] = ()

    def well_formed(self) -> bool:
        """Mirrors Lean `SpecAST.wellFormed`."""
        return all(
            (isinstance(item, TypeDecl) and item.type_expr.well_formed())
            or (isinstance(item, FuncDecl) and item.func_expr.well_formed())
            for item in self.items
        )
