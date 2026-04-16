# 機械判読可能な半順序保存・集合論的設計書の体系

## 1. 問題設定

Spec = (T, F, ≤, Φ, I)

-   T: 型
-   F: 関数
-   ≤: 精緻化半順序
-   Φ: 制約
-   I: 不変条件

## 2. Leanによる形式化

``` lean
structure TypeSpec :=
  (α : Type)
  (inv : α → Prop)

structure FuncSpec (A B : TypeSpec) :=
  (f : A.α → B.α)
  (pre  : A.α → Prop)
  (post : A.α → B.α → Prop)
  (sound : ∀ x, pre x → post x (f x))
```

## 3. DSL

``` lisp
(spec
  (type UserId Int (>= 0))
  (func transfer
    (input (from UserId))
    (output Bool)
    (pre (> from 0))
    (post (= result true))))
```

## 4. 半順序

f ≤ g ⇔ - pre_g ⇒ pre_f - post_f ⇒ post_g

## 5. テスト生成

Test = { x \| pre(x) }

完全性: ∀x, pre(x) ⇒ ∃t ∈ T

## 6. LLM統合

S\_{n+1} = Fix(LLM(S_n), Verify)

## 7. パイプライン

DSL → AST → SMT → Test → LLM → Code → Lean証明

## 8. 数理構造

-   圏論
-   Galois接続
-   固定点理論

