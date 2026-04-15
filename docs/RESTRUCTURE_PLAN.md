# 論文構成の再構築計画

## 現在の構成から新構成へのマッピング

### 旧構成（01_theoretical_foundation.md）→ 新構成

| 新章 | ファイル名 | 旧セクション | 内容 |
|-----|-----------|------------|------|
| 1 | 01_introduction.md | セクション1, 2 | 文書の目的、中心仮説、知能の再定義 |
| 2 | 02_related_work.md | セクション3 | 先行研究との位置づけ（IB Theory, LTH, Grokking等） |
| 3 | 03_preliminaries.md | セクション4, 5, 6, 7 | 概念圧縮、Kolmogorov複雑度、MDL原理、情報理論的定式化 |
| 4 | 04_problem_formulation.md | **新規作成** | 形式的な問題定義、仮定、評価基準 |
| 5 | 05_theoretical_framework.md | セクション8, 9, 10, 11 | 双方向変換、型理論、制約検証、動的圧縮理論 |
| 6 | 06_methodology.md | セクション10, 13.2 | 制約検証機構の実装方法、型システムの導入 |
| 7 | 07_theoretical_analysis.md | **TBD** | 複雑度解析、収束性の証明、最適性の議論 |
| 8 | 08_experimental_evaluation.md | セクション13.1（一部）+ **TBD** | 実験設定、評価指標、結果（現在は提案のみ） |
| 9 | 09_discussion.md | セクション12 + **新規** | 批判的検証、限界、結果の解釈 |
| 10 | 10_conclusion.md | セクション13.4, 14 | 学術的貢献、今後の課題、設計要請 |

## 新構成の詳細

### 1. Introduction（序論）
**ファイル**: `01_introduction.md`
**内容**:
- 1.1 研究の背景と動機
- 1.2 問題設定
- 1.3 中心仮説
  - 専門用語 = 概念の論理的圧縮
  - 統計的圧縮と論理的圧縮の統合
- 1.4 知能の再定義
  - 抽象化能力
  - 展開能力
  - 制約検証能力
- 1.5 本研究の貢献
- 1.6 論文の構成

### 2. Related Work（関連研究）
**ファイル**: `02_related_work.md`
**内容**:
- 2.1 Information Bottleneck Theory
- 2.2 Lottery Ticket Hypothesis
- 2.3 Grokking
- 2.4 Scaling Laws
- 2.5 Emergent Abilities
- 2.6 Neuro-Symbolic AI
- 2.7 Representation Learning
- 2.8 比較表とまとめ

### 3. Preliminaries（予備知識）
**ファイル**: `03_preliminaries.md`
**内容**:
- 3.1 概念圧縮としての専門用語
- 3.2 Kolmogorov Complexity
- 3.3 MDL原理
- 3.4 情報理論的定式化
  - 圧縮利得
  - 制約コスト
  - 相互情報量

### 4. Problem Formulation（問題定式化）
**ファイル**: `04_problem_formulation.md`
**内容**: **新規作成**
- 4.1 形式的な問題定義
  - 入力空間と出力空間
  - 圧縮関数と展開関数の定義
- 4.2 仮定と制約
  - 型制約の定義
  - 論理的整合性の要件
- 4.3 最適化目標
  - MDL原理に基づく目的関数
  - 制約付き最適化問題
- 4.4 評価基準
  - 圧縮率
  - 復元精度
  - 制約充足度

### 5. Theoretical Framework（理論的枠組み）
**ファイル**: `05_theoretical_framework.md`
**内容**:
- 5.1 双方向変換モデル
  - 静的圧縮
  - 動的圧縮
- 5.2 確率的型システム
  - 型の定義
  - 確率的型判定
  - ソフト/ハード制約
- 5.3 制約検証機構
  - 三層構造
  - 型チェック層
  - 制約充足層
  - 論理検証層
- 5.4 動的圧縮理論
  - 相転移モデル
  - Grokkingの説明
  - エネルギー地形

### 6. Methodology（方法論）
**ファイル**: `06_methodology.md`
**内容**:
- 6.1 制約検証機構の実装
  - アーキテクチャ設計
  - 各層の実装詳細
- 6.2 型システムの導入
  - 型定義
  - 型推論機構
- 6.3 修正機構
  - Beam Search
  - Backtracking
  - Constraint Propagation
- 6.4 段階的制約強化
  - 学習スケジュール
  - αパラメータの調整

### 7. Theoretical Analysis（理論的解析）
**ファイル**: `07_theoretical_analysis.md`
**内容**: **TBD（今後実装）**
- 7.1 複雑度解析
  - 時間計算量
  - 空間計算量
- 7.2 収束性の証明
  - 学習の収束条件
  - 収束速度
- 7.3 最適性の議論
  - MDL最適性
  - 近似保証
- 7.4 理論的性質
  - 定理と証明
  - 補題

### 8. Experimental Evaluation（実験的評価）
**ファイル**: `08_experimental_evaluation.md`
**内容**: **TBD（今後実装）**
- 8.1 実験設定
  - データセット
  - ベースライン手法
  - ハイパーパラメータ
- 8.2 評価指標
  - 圧縮率
  - ハルシネーション率
  - 論理的整合性スコア
- 8.3 実験結果
  - Attentionパターンと概念圧縮の対応
  - 層別の圧縮率分析
  - 制約検証機構の効果
- 8.4 結果の分析
  - 統計的有意性
  - アブレーション研究

### 9. Discussion（考察）
**ファイル**: `09_discussion.md`
**内容**:
- 9.1 理論の強み
  - 統一的視点
  - Information Bottleneck Theoryとの整合性
  - 認知科学的妥当性
- 9.2 理論の限界
  - 残存する課題
  - 説明できない現象
- 9.3 理論と実験の整合性
  - 予測と結果の比較
  - 乖離の分析
- 9.4 実用的な含意
  - 設計指針
  - 実装上の考慮事項
- 9.5 将来の方向性
  - 理論の拡張可能性
  - 応用分野

### 10. Conclusion（結論）
**ファイル**: `10_conclusion.md`
**内容**:
- 10.1 主要な貢献のまとめ
  - 理論的貢献
  - 方法論的貢献
- 10.2 学術的意義
  - 既存研究への貢献
  - 独自性
- 10.3 今後の課題
  - 短期的課題（1-2年）
  - 中期的課題（3-5年）
  - 長期的展望（5年以上）
- 10.4 設計要請
  - 要件・設計への含意

## 実装計画

### Phase 1: 既存内容の分割（優先度：高）
1. 01_introduction.md
2. 02_related_work.md
3. 03_preliminaries.md
4. 05_theoretical_framework.md
5. 09_discussion.md
6. 10_conclusion.md

### Phase 2: 新規作成（優先度：中）
1. 04_problem_formulation.md（新規作成）
2. 06_methodology.md（一部新規、一部移動）

### Phase 3: TBDセクション（優先度：低、将来実装）
1. 07_theoretical_analysis.md（TBD）
2. 08_experimental_evaluation.md（TBD）

### Phase 4: 統合作業
1. README.md の更新
2. 各ファイル間の相互参照の整備
3. 01_theoretical_foundation.md のアーカイブ化

## ファイル命名規則

- 番号付き: `01_introduction.md`, `02_related_work.md`, ...
- 小文字とアンダースコア使用
- 英語の標準的な論文セクション名を使用

## 相互参照の形式

```markdown
詳細は [Problem Formulation](04_problem_formulation.md) を参照。
[Theoretical Framework](05_theoretical_framework.md#52-確率的型システム) のセクション5.2を参照。
```

## TBDセクションのテンプレート

```markdown
# [章タイトル]

> **Status**: TBD（To Be Determined）
> 
> この章は、実装と実験の完了後に執筆予定です。

## [セクションタイトル]

**予定内容**:
- [項目1]
- [項目2]
- ...

**必要な前提条件**:
- [条件1]
- [条件2]
- ...

**期待される成果**:
- [成果1]
- [成果2]
- ...
```

## 次のステップ

1. この計画をレビュー
2. Phase 1の実装開始
3. 各ファイルの作成と内容の移動
4. 相互参照の整備
5. README.mdの更新