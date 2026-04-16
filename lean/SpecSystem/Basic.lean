/-!
# SpecSystem.Basic

spec_system.md §2 の Lean 形式化。
Spec = (T, F, ≤, Φ, I) の基本構造体を定義する。

## 参照
- docs/ref/spec_system.md §2: Lean による形式化
- docs/ref/spec_system.md §4: 半順序（精緻化）
- docs/ref/spec_system.md §5: テスト生成
-/

/-- 型仕様: 型 α と不変条件 inv を持つ。
    spec_system.md §2 の TypeSpec に対応。 -/
structure TypeSpec where
  α : Type
  inv : α → Prop

/-- 関数仕様: 事前条件・事後条件・健全性証明を持つ。
    spec_system.md §2 の FuncSpec に対応。 -/
structure FuncSpec (A B : TypeSpec) where
  f : A.α → B.α
  pre : A.α → Prop
  post : A.α → B.α → Prop
  sound : ∀ (x : A.α), pre x → post x (f x)

/-- 制約仕様: 型に対する追加制約。
    Spec 5-タプルの Φ に対応。 -/
structure ConstraintSpec (T : TypeSpec) where
  constraints : List (T.α → Prop)

/-- 精緻化半順序: f ≤ g ⟺ pre_g ⇒ pre_f ∧ post_f ⇒ post_g
    spec_system.md §4 に対応。

    直感: g がより強い事前条件を要求する場合、f は g を精緻化する
    （f はより広い入力を受け付け、より強い保証を提供する） -/
def refines {A B : TypeSpec} (f g : FuncSpec A B) : Prop :=
  (∀ (x : A.α), g.pre x → f.pre x) ∧
  (∀ (x : A.α) (y : B.α), f.post x y → g.post x y)

notation:50 f " ≤ₛ " g => refines f g

/-- 精緻化は反射的 -/
theorem refines_refl {A B : TypeSpec} (f : FuncSpec A B) : f ≤ₛ f :=
  ⟨fun _ h => h, fun _ _ h => h⟩

/-- 精緻化は推移的 -/
theorem refines_trans {A B : TypeSpec} (f g h : FuncSpec A B)
    (hfg : f ≤ₛ g) (hgh : g ≤ₛ h) : f ≤ₛ h :=
  ⟨fun x hx => hfg.1 x (hgh.1 x hx),
   fun x y hy => hgh.2 x y (hfg.2 x y hy)⟩

/-- テスト集合: 事前条件を満たす入力の集合。
    spec_system.md §5: Test = { x | pre(x) } に対応。 -/
def testSet {A B : TypeSpec} (spec : FuncSpec A B) : A.α → Prop :=
  fun x => spec.pre x

/-- テスト完全性: 事前条件を満たす全入力がテスト集合に含まれる。
    spec_system.md §5: ∀x, pre(x) ⇒ ∃t ∈ T -/
theorem test_completeness {A B : TypeSpec} (spec : FuncSpec A B)
    (x : A.α) (h : spec.pre x) : testSet spec x :=
  h
