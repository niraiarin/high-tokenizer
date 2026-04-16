import Lake
open Lake DSL

package «spec-system» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib «SpecSystem» where
  roots := #[`SpecSystem]
