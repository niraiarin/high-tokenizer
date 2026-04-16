/-!
# SpecSystem.DSL.AST

DSL パーサーが出力する抽象構文木の型定義。
spec_system.md §3 の S式 DSL に対応する AST ノード。

## DSL 構文例
```lisp
(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from UserId))
    (output Bool)
    (pre (> from 0))
    (post (= result true))))
```
-/

/-- S式の値（パーサーの直接出力） -/
inductive SExpr where
  | atom : String → SExpr
  | list : List SExpr → SExpr
  deriving Repr, BEq

/-- 型式: 型名と述語制約 -/
structure TypeExpr where
  name : String
  basetype : String
  predicates : List String
  deriving Repr, BEq

/-- パラメータ: 名前と型 -/
structure ParamExpr where
  name : String
  typeName : String
  deriving Repr, BEq

/-- 関数式: 関数名、入力、出力、事前条件、事後条件 -/
structure FuncExpr where
  name : String
  inputs : List ParamExpr
  output : String
  pre : List String
  post : List String
  deriving Repr, BEq

/-- 仕様のトップレベルノード -/
inductive SpecItem where
  | typeDecl : TypeExpr → SpecItem
  | funcDecl : FuncExpr → SpecItem
  deriving Repr, BEq

/-- 仕様全体: SpecItem のリスト -/
structure SpecAST where
  items : List SpecItem
  deriving Repr, BEq

/-- AST の well-formedness: 型宣言は空でない名前を持つ -/
def TypeExpr.wellFormed (t : TypeExpr) : Prop :=
  t.name ≠ "" ∧ t.basetype ≠ ""

/-- AST の well-formedness: 関数宣言は空でない名前と少なくとも 1 つの入���を持つ -/
def FuncExpr.wellFormed (f : FuncExpr) : Prop :=
  f.name ≠ "" ∧ f.inputs.length > 0

/-- 仕様全体の well-formedness: 全アイテムが well-formed -/
def SpecAST.wellFormed (spec : SpecAST) : Prop :=
  ∀ item ∈ spec.items,
    match item with
    | SpecItem.typeDecl t => t.wellFormed
    | SpecItem.funcDecl f => f.wellFormed
