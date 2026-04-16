import Lake
open Lake DSL

package «spec-system» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

require LSpec from git
  "https://github.com/lurk-lab/LSpec.git" @ "main"

@[default_target]
lean_lib «SpecSystem» where
  roots := #[`SpecSystem]

-- LSpec tests run at compile time via #lspec macro.
-- SpecTest is included in the SpecSystem library.
lean_lib «SpecTest» where
  roots := #[`SpecTest]
