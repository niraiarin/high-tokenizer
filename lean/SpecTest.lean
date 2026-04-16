import LSpec
import SpecSystem

/-!
# SpecTest

LSpec による Lean 仕様の property テスト。
Python パーサーとの整合性は、両者が同じ AST 定義（SpecSystem.DSL.AST）を
共有していることで保証する。
-/

open LSpec

-- SExpr BEq tests
#lspec test "SExpr.atom equality" (SExpr.atom "hello" == SExpr.atom "hello")
#lspec test "SExpr.atom inequality" (SExpr.atom "hello" != SExpr.atom "world")
#lspec test "SExpr.list equality"
  (SExpr.list [SExpr.atom "a", SExpr.atom "b"] ==
   SExpr.list [SExpr.atom "a", SExpr.atom "b"])
#lspec test "SExpr.list nested"
  (SExpr.list [SExpr.atom "spec", SExpr.list [SExpr.atom "type"]] ==
   SExpr.list [SExpr.atom "spec", SExpr.list [SExpr.atom "type"]])

-- SpecAST construction
#lspec test "empty SpecAST" ((SpecAST.mk []).items.length == 0)

-- TypeExpr / FuncExpr construction
#lspec test "TypeExpr construction"
  ((TypeExpr.mk "UserId" "Int" ["(>= 0)"]).name == "UserId")
#lspec test "FuncExpr construction"
  ((FuncExpr.mk "transfer" [ParamExpr.mk "from" "UserId"] "Bool" ["(> from 0)"] ["(= result true)"]).name == "transfer")

-- SpecItem construction
#lspec test "TypeDecl via SpecItem"
  (match SpecItem.typeDecl (TypeExpr.mk "X" "Int" []) with
   | SpecItem.typeDecl t => t.name == "X"
   | _ => false)

#lspec test "FuncDecl via SpecItem"
  (match SpecItem.funcDecl (FuncExpr.mk "f" [ParamExpr.mk "x" "Int"] "Bool" [] []) with
   | SpecItem.funcDecl f => f.name == "f"
   | _ => false)
