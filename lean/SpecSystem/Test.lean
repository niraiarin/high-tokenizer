import SpecSystem.Basic
import SpecSystem.DSL.AST
import SpecSystem.DSL.Spec

/-!
# SpecSystem.Test

Lean 側の smoketest。`#check` / `#eval` で基本的な型整合性を確認する。
-/

-- TypeSpec / FuncSpec の型が正しく構成されていること
#check TypeSpec
#check FuncSpec
#check ConstraintSpec
#check refines
#check @refines_refl
#check @refines_trans

-- DSL AST 型の構成
#check SExpr.atom
#check SExpr.list
#check SpecItem.typeDecl
#check SpecItem.funcDecl
#check SpecAST.wellFormed

-- DSL パーサー仕様
#check parseSExprSpec
#check parseSpecSpec
#check parseSExprTestSet
#check parseSpecTestSet

-- 精緻化半順序の性質
#check @refines_refl
#check @refines_trans
#check @test_completeness

-- AST の具体例が構築可能であること
#eval repr (SExpr.atom "hello")
#eval repr (SExpr.list [SExpr.atom "spec", SExpr.atom "test"])
#eval repr (TypeExpr.mk "UserId" "Int" ["(>= 0)"])
#eval repr (SpecAST.mk [])
