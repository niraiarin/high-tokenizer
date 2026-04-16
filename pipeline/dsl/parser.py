"""S-expression and spec DSL parser.

Implements the functions specified by Lean FuncSpecs:
- parse_sexpr: String → SExpr  (parseSExprSpec)
- parse_spec:  SExpr → SpecAST (parseSpecSpec)
"""

from __future__ import annotations

from pipeline.dsl.ast import (
    Atom,
    FuncDecl,
    FuncExpr,
    ParamExpr,
    SExpr,
    SList,
    SpecAST,
    SpecItem,
    TypeDecl,
    TypeExpr,
)

# ============================================================
# S-expression tokenizer + parser
# ============================================================


def _tokenize(source: str) -> list[str]:
    """Tokenize S-expression source into a list of tokens.

    Splits on whitespace and treats '(' and ')' as individual tokens.
    """
    tokens: list[str] = []
    current = ""
    for ch in source:
        if ch in ("(", ")"):
            if current:
                tokens.append(current)
                current = ""
            tokens.append(ch)
        elif ch in (" ", "\t", "\n", "\r"):
            if current:
                tokens.append(current)
                current = ""
        else:
            current += ch
    if current:
        tokens.append(current)
    return tokens


def parse_sexpr(source: str) -> SExpr:
    """Parse an S-expression string into an SExpr AST.

    Corresponds to Lean `parseSExprSpec`:
    - pre: isWellFormedSExpr (non-empty, balanced parentheses)
    - post: valid SExpr tree

    Raises:
        ValueError: If source is empty/whitespace-only or has unbalanced parentheses.
    """
    tokens = _tokenize(source)
    if not tokens:
        raise ValueError("Empty input is not a well-formed S-expression")

    pos = 0

    def _parse() -> SExpr:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of input")

        token = tokens[pos]

        if token == "(":
            pos += 1
            items: list[SExpr] = []
            while pos < len(tokens) and tokens[pos] != ")":
                items.append(_parse())
            if pos >= len(tokens):
                raise ValueError("Unmatched opening parenthesis")
            pos += 1  # consume ')'
            return SList(tuple(items))

        if token == ")":
            raise ValueError("Unexpected closing parenthesis")

        pos += 1
        return Atom(token)

    result = _parse()

    if pos < len(tokens):
        raise ValueError("Unexpected tokens after expression")

    return result


# ============================================================
# Spec parser: SExpr → SpecAST
# ============================================================


def _sexpr_to_str(sexpr: SExpr) -> str:
    """Convert an S-expression back to string form (for predicate storage)."""
    if isinstance(sexpr, Atom):
        return sexpr.value
    if isinstance(sexpr, SList):
        inner = " ".join(_sexpr_to_str(item) for item in sexpr.items)
        return f"({inner})"
    raise TypeError(f"Unknown SExpr type: {type(sexpr)}")


def _parse_type_decl(items: tuple[SExpr, ...]) -> TypeDecl:
    """Parse (type NAME BASETYPE predicate*) into TypeDecl."""
    if len(items) < 3:
        raise ValueError("type declaration requires at least name and basetype")

    name_node, basetype_node = items[1], items[2]
    if not isinstance(name_node, Atom) or not isinstance(basetype_node, Atom):
        raise ValueError("type name and basetype must be atoms")

    predicates = tuple(_sexpr_to_str(items[i]) for i in range(3, len(items)))

    return TypeDecl(
        TypeExpr(
            name=name_node.value,
            basetype=basetype_node.value,
            predicates=predicates,
        )
    )


def _parse_func_decl(items: tuple[SExpr, ...]) -> FuncDecl:
    """Parse (func NAME clause+) into FuncDecl."""
    if len(items) < 2:
        raise ValueError("func declaration requires at least a name")

    name_node = items[1]
    if not isinstance(name_node, Atom):
        raise ValueError("func name must be an atom")

    inputs: list[ParamExpr] = []
    output = ""
    pre: list[str] = []
    post: list[str] = []

    for clause in items[2:]:
        if not isinstance(clause, SList) or len(clause.items) < 2:
            raise ValueError(f"Invalid func clause: {clause}")

        keyword = clause.items[0]
        if not isinstance(keyword, Atom):
            raise ValueError(f"Clause keyword must be an atom: {keyword}")

        match keyword.value:
            case "input":
                for param in clause.items[1:]:
                    if isinstance(param, SList) and len(param.items) == 2:
                        pname, ptype = param.items
                        if isinstance(pname, Atom) and isinstance(ptype, Atom):
                            inputs.append(ParamExpr(pname.value, ptype.value))
            case "output":
                if isinstance(clause.items[1], Atom):
                    output = clause.items[1].value
            case "pre":
                pre.append(_sexpr_to_str(clause.items[1]))
            case "post":
                post.append(_sexpr_to_str(clause.items[1]))

    return FuncDecl(
        FuncExpr(
            name=name_node.value,
            inputs=tuple(inputs),
            output=output,
            pre=tuple(pre),
            post=tuple(post),
        )
    )


def parse_spec(sexpr: SExpr) -> SpecAST:
    """Parse an SExpr into a SpecAST.

    Corresponds to Lean `parseSpecSpec`:
    - pre: isSpecSExpr (input is `(spec ...)` form)
    - post: wellFormed (output SpecAST passes well-formedness checks)

    Raises:
        ValueError: If sexpr is not a (spec ...) list or contains unknown declarations.
    """
    if not isinstance(sexpr, SList):
        raise ValueError("Spec must be a list S-expression")

    if not sexpr.items or not isinstance(sexpr.items[0], Atom) or sexpr.items[0].value != "spec":
        raise ValueError("Spec must start with 'spec' keyword")

    items: list[SpecItem] = []

    for decl in sexpr.items[1:]:
        if not isinstance(decl, SList) or not decl.items:
            raise ValueError(f"Invalid declaration: {decl}")

        keyword = decl.items[0]
        if not isinstance(keyword, Atom):
            raise ValueError(f"Declaration keyword must be an atom: {keyword}")

        match keyword.value:
            case "type":
                items.append(_parse_type_decl(decl.items))
            case "func":
                items.append(_parse_func_decl(decl.items))
            case _:
                raise ValueError(f"Unknown declaration type: {keyword.value}")

    return SpecAST(items=tuple(items))
