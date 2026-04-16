# Lean 4 DSL + 仕様形式化 ベストプラクティス

調査日: 2026-04-16

## 1. Lean 4 DSL パ��ーン

### 基本アーキテクチャ（3 層）

1. **Syntax Category** (`declare_syntax_cat`): 独立した文法空間を作成
2. **Syntax Rules** (`syntax`): パターンをコンビネータで定義
3. **Elaborators** (`@[term_elab]`): `Syntax` → `Expr` 変換

```lean
declare_syntax_cat myDSL
syntax "keyword" term ":" myDSL
syntax "[MyDSL|" myDSL "]" : term
@[term_elab myDSL] def elaborateMyDSL : TermElab := ...
```

### 単純なケース: notation で十分

```lean
infixl:60 " ⊕ " => semantic_function
```

複雑な DSL でなければ elaborator は不要��

### 参考プロジェクト

- **zkLean** (GaloisInc): Hoare triple 記法 `⦃ precond ⦄ operation ⦃ postcond ⦄` で ZK 回路を記述
- **Lean 4 Metaprogramming Book**: DSL, Syntax, Elaboration の 3 章が教科書

## 2. プロジェクト構成

### モジュール命名規則

- **型/構造体**: PascalCase (`FuncSpec`, `TypeExpr`)
- **定理/性質**: snake_case (`refines_trans`, `test_completeness`)
- **関数**: camelCase (`parseExpr`, `wellFormed`)
- **ファイル**: PascalCase、ドット記法でモジュール化 (`SpecSystem/DSL/Spec.lean` → `SpecSystem.DSL.Spec`)

### sorry の戦略的使用

- Stage 0（ブートストラップ）では仕様の「形」を定義し、sorry で証明を仮置き
- Python 実装のテスト通過で代替検証
- B4（セルフホスティング）で再訪し解消判断
- **ドキュメント必須**: なぜ sorry にしたか、いつ解消するかを doc comment に記載

### structure vs class vs inductive の判断

| 使い分け | 用途 | 本プロジェクトの例 |
|----------|------|-------------------|
| `structure` | 単一バリアントのデータ束 | `TypeSpec`, `FuncSpec`, `SpecAST` |
| `inductive` | 複数バリアント | `SExpr`, `SpecItem` |
| `class` | 多相的インターフェース | （現時点では未使用） |

## 3. Python-Lean 連携

### JSON 交換パターン（推奨）

```
Python: S式パース → JSON シリアライズ → Lean REPL に送信
Lean:   JSON パース → FuncSpec に対して検証 → 結果を返す
Python: テスト実行、事後条件と比較
```

### 関連ツール

- **LeanInteract**: Python から Lean 4 REPL を呼び出すライブラリ。環境を保持したまま対話可能
- **lean4-json-schema**: Lean 4 で JSON バリデーションを証明付きで実行
- **LSpec**: Lean 4 テストフレームワーク
- **SlimCheck**: Lean 4 の QuickCheck 相当。property-based testing

### テスト生成ワークフロー

1. Python で仕様（S式）からテストケースを生成
2. JSON 経由で Lean に���信し FuncSpec に対して検証
3. **SlimCheck** で property-based testing（事後条件の自動テスト）
4. 反例を抽出して仕様を精緻化

## 4. 本プロジェクトへの適用方針

### 現在の設計との整合

- `TypeSpec`/`FuncSpec` パターンは Lean 4 のベストプラクティスに合致
- `inductive` を AST ノードに、`structure` を仕様に使う判断は正しい
- 精緻化半順序 `≤ₛ` の notation 定義は Lean のイディオム通り

### 今後の拡張方針

1. **B1 (DSL パーサー)**: S式パースは Python で実装。Lean には JSON 経由で AST を渡す
2. **B2 (コード生成)**: Lean の `syntax`/`macro` ではなく Python でコード生成し、生成結果を Lean コンパイラで検証
3. **B3 (LLM 統合)**: LeanInteract で Python → Lean REPL 対話ループを実装
4. **将来**: 十分に安定したら、Lean 4 native の `declare_syntax_cat` で eDSL 化を検討

## 参考資料

- [Lean 4 Metaprogramming Book: DSLs](https://leanprover-community.github.io/lean4-metaprogramming-book/main/08_dsls.html)
- [Lean 4 Metaprogramming Book: Syntax](https://leanprover-community.github.io/lean4-metaprogramming-book/main/05_syntax.html)
- [zkLean (GaloisInc)](https://github.com/GaloisInc/zkLean)
- [LeanInteract](https://github.com/augustepoiroux/LeanInteract)
- [lean4-json-schema](https://predictablemachines.com/blog/announcing-lean4-json-schema/)
- [LSpec](https://github.com/lurk-lab/LSpec)
- [Mathlib Naming Conventions](https://leanprover-community.github.io/contribute/naming.html)
