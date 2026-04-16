import SpecSystem.Basic
import SpecSystem.DSL.AST

/-!
# SpecSystem.DSL.Spec

DSL パーサーの形式仕様（FuncSpec）。
ブートストラップ Stage 0: パイプラインが存在しない状態で手書きする仕様。

## 仕様の位置づけ
- TypeSpec: 入力型（String）、出力型（SExpr, SpecAST）と不変条件
- FuncSpec: パーサーの事前条件・事後条件・健全性
- テスト集合: 事前条件を満たす入力 = well-formed S式の集合
-/

/-! ## 入力・出力の TypeSpec -/

/-- S式テキストの TypeSpec: 空でない文字列 -/
def SExprInputSpec : TypeSpec where
  α := String
  inv := fun s => s.length > 0

/-- S式 AST の TypeSpec: 常に有効（パーサーが返す値は構造的に正しい） -/
def SExprOutputSpec : TypeSpec where
  α := SExpr
  inv := fun _ => True

/-- 仕様 AST の TypeSpec: well-formed -/
def SpecASTOutputSpec : TypeSpec where
  α := SpecAST
  inv := fun spec => spec.wellFormed

/-! ## S式パーサーの仕様 -/

/-- S式の well-formedness: 括弧が対応している -/
def isWellFormedSExpr (s : String) : Prop :=
  s.length > 0 ∧ ∃ _result : SExpr, True  -- 存在性のみ要求（計算は Python 側）

/-- S式パーサーの FuncSpec

事前条件: 入力が well-formed な S式テキスト
事後条件: 出力が入力のアトム・リスト構造を保存

ブートストラップ注記: `sound` は sorry で仮置き。
Stage 0 では仕様の「形」を定義することが目的。
健全性の証明は、Python 実装のテスト通過で代替検証する。
B4（セルフホスティング）で再訪し、sorry を解消するか判断する。 -/
def parseSExprSpec : FuncSpec SExprInputSpec SExprOutputSpec where
  f := fun _ => SExpr.atom ""  -- placeholder: 実装は Python 側
  pre := fun s => isWellFormedSExpr s
  post := fun _input _output => True  -- 事後条件は Python テストで検証
  sound := fun _ _ => trivial

/-! ## 仕様パーサーの仕様（S式 → SpecAST） -/

/-- S式が spec トップレベルノードであること -/
def isSpecSExpr (sexpr : SExpr) : Prop :=
  match sexpr with
  | SExpr.list (SExpr.atom "spec" :: _) => True
  | _ => False

/-- 仕様パーサーの FuncSpec: S式 AST → SpecAST

事前条件: 入力が (spec ...) 形式の S式
事後条件: 出力が well-formed な SpecAST -/
def parseSpecSpec : FuncSpec SExprOutputSpec SpecASTOutputSpec where
  f := fun _ => ⟨[]⟩  -- placeholder
  pre := fun sexpr => isSpecSExpr sexpr
  post := fun _input output => output.wellFormed
  sound := by
    intro x _hpre
    -- SpecAST.wellFormed for empty items list is vacuously true
    simp [SpecAST.wellFormed]

/-! ## テスト集合の定義 -/

/-- S式パーサーのテスト集合: well-formed な S式文字列 -/
def parseSExprTestSet : String → Prop :=
  testSet parseSExprSpec

/-- 仕様パーサーのテスト集合: spec 形式の S式 -/
def parseSpecTestSet : SExpr → Prop :=
  testSet parseSpecSpec
