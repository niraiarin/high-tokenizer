import SpecSystem.DSL.Macros

/-!
# SpecSystem.DSL.Examples

Demonstrates the embedded DSL by specifying the spec_system.md
UserId/transfer example using custom Lean syntax.

Compare with:
- Hand-written: SpecSystem/DSL/Spec.lean
- External DSL: specs/dsl_parser.spec
-/

-- Type specs via eDSL
specType UserId Nat (fun (x : Nat) => 0 < x)
specType Amount Nat

-- Function spec via eDSL (pipe-separated: impl | pre | post)
specFunc transfer UserId.TypeSpec Amount.TypeSpec
  | (fun (_x : Nat) => (0 : Nat))
  | (fun (x : Nat) => 0 < x)
  | (fun (_x : Nat) (_y : Nat) => True)

-- Verify eDSL-generated definitions are well-typed
#check UserId.TypeSpec    -- : TypeSpec
#check Amount.TypeSpec    -- : TypeSpec
#check transfer.FuncSpec  -- : FuncSpec UserId.TypeSpec Amount.TypeSpec

-- Refinement works with eDSL-defined specs
example : transfer.FuncSpec ≤ₛ transfer.FuncSpec := refines_refl _
