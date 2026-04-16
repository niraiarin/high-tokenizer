# DSL 文法仕様

spec_system.md §3 の S式 DSL の完全な文法定義。

## EBNF

```ebnf
spec        = "(" "spec" spec_item* ")"
spec_item   = type_decl | func_decl
type_decl   = "(" "type" NAME NAME predicate* ")"
func_decl   = "(" "func" NAME func_clause+ ")"
func_clause = input_clause | output_clause | pre_clause | post_clause | inv_clause
input_clause  = "(" "input" param+ ")"
output_clause = "(" "output" NAME ")"
pre_clause    = "(" "pre" expr ")"
post_clause   = "(" "post" expr ")"
inv_clause    = "(" "inv" expr ")"
param         = "(" NAME NAME ")"
predicate     = "(" operator NAME value ")"
expr          = atom | "(" operator expr* ")"
atom          = NAME | NUMBER | STRING
operator      = ">" | ">=" | "<" | "<=" | "=" | "!=" | "and" | "or" | "not"
NAME          = /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER        = /[+-]?[0-9]+(\.[0-9]+)?/
STRING        = /"[^"]*"/
```

## 対応する Lean AST ノード

| DSL 構文 | Lean AST 型 |
|----------|-------------|
| `spec` | `SpecAST` |
| `type_decl` | `SpecItem.typeDecl (TypeExpr ...)` |
| `func_decl` | `SpecItem.funcDecl (FuncExpr ...)` |
| `param` | `ParamExpr` |
| S式全体 | `SExpr` (atom / list) |

## 例

```lisp
(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from UserId))
    (output Bool)
    (pre (> from 0))
    (post (= result true))))
```

→ `SpecAST { items: [typeDecl(UserId, Int, ["(>= 0)"]), funcDecl(transfer, ...)] }`
