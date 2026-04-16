import SpecSystem.Basic
import SpecSystem.Theory

/-!
# SpecSystem.DSL.Macros

Embedded DSL for writing TypeSpec and FuncSpec declarations
directly in Lean files using custom syntax.

## Usage

```lean
-- Define a type spec with invariant
specType UserId Nat fun x => x > 0

-- Define a type spec without invariant
specType Amount Nat

-- Define a function spec
specFunc transfer UserId_TypeSpec Amount_TypeSpec
  fun x => default
  fun x => x > 0
  fun x y => True
```
-/

-- ============================================================
-- specType: TypeSpec declaration macro
-- ============================================================

/-- `specType Name BaseType fun x => inv` — declare a TypeSpec with invariant. -/
macro "specType " name:ident base:ident inv:term : command =>
  let defName := Lean.mkIdent (name.getId ++ `TypeSpec)
  `(def $defName : TypeSpec where
      α := $base
      inv := $inv)

/-- `specType Name BaseType` — declare a TypeSpec with trivial invariant. -/
macro "specType " name:ident base:ident : command =>
  let defName := Lean.mkIdent (name.getId ++ `TypeSpec)
  `(def $defName : TypeSpec where
      α := $base
      inv := fun _ => True)

-- ============================================================
-- specFunc: FuncSpec declaration macro
-- ============================================================

/-- `specFunc Name InSpec OutSpec | impl | pre | post` — declare a FuncSpec.
    The `sound` proof is left as `sorry` (to be filled in or verified externally). -/
macro "specFunc " name:ident inSpec:ident outSpec:ident
    " | " impl:term " | " pre:term " | " post:term : command =>
  let defName := Lean.mkIdent (name.getId ++ `FuncSpec)
  `(def $defName : FuncSpec $inSpec $outSpec where
      f := $impl
      pre := $pre
      post := $post
      sound := by sorry)

-- ============================================================
-- specTheorem: 定理宣言マクロ (ACL2 式定理分離, #21)
-- ============================================================

/-- `specTheorem Name | statement | proof` — declare a theorem.
    Use `by sorry` for proof to defer. -/
macro "specTheorem " name:ident " | " stmt:term " | " prf:term : command =>
  `(theorem $name : $stmt := $prf)

/-- `specTheorem Name | statement` — declare with sorry proof. -/
macro "specTheorem " name:ident " | " stmt:term : command =>
  `(theorem $name : $stmt := by sorry)

-- ============================================================
-- specBound: 上界/下界宣言マクロ (#21)
-- ============================================================

/-- `specBound Name | bound_statement | proof` — declare a bound. -/
macro "specBound " name:ident " | " stmt:term " | " prf:term : command =>
  `(theorem $name : $stmt := $prf)

/-- `specBound Name | bound_statement` — declare with sorry proof. -/
macro "specBound " name:ident " | " stmt:term : command =>
  `(theorem $name : $stmt := by sorry)
