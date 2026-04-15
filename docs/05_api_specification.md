# 05. API 仕様

## 目次
- [1. 文書の目的](#1-文書の目的)
- [2. API 設計方針](#2-api-設計方針)
- [3. 公開 API 一覧](#3-公開-api-一覧)
- [4. 共通データモデル](#4-共通データモデル)
- [5. 各 API の詳細仕様](#5-各-api-の詳細仕様)
- [6. Python 使用例](#6-python-使用例)
- [7. エラーハンドリング](#7-エラーハンドリング)
- [8. バージョニング方針](#8-バージョニング方針)
- [9. 関連文書](#9-関連文書)

## 1. 文書の目的
本書は、概念圧縮システムが外部に公開する API の契約を定義する。  
内部設計は [03_architecture.md](./03_architecture.md)、詳細実装仕様は [04_implementation_spec.md](./04_implementation_spec.md) を参照する。

本 API は以下を提供する。

- 抽象化 API
- 展開 API
- 制約検証 API
- 複雑度評価 API
- MDL 評価 API
- ヘルスチェック API

## 2. API 設計方針
### 2.1 原則
- JSON ベースの同期 API を標準とする
- 外部公開名は安定させ、内部クラス構成とは分離する
- すべてのレスポンスに `trace_id` を含める
- 診断情報を返せる API では `diagnostics` を標準化する
- 検証不能と失敗を区別する
- バッチ化しやすい単純な入出力構造を優先する

### 2.2 ベース URL
```text
/api/v1
```

### 2.3 MIME Type
- Request: `application/json`
- Response: `application/json`

## 3. 公開 API 一覧
| API 名 | HTTP | パス | 目的 |
|---|---|---|---|
| Health Check | GET | `/health` | 稼働確認 |
| Abstract Text | POST | `/abstract` | 入力文・概念列を高位語へ圧縮 |
| Expand Term | POST | `/expand` | 高位語を低位概念へ展開 |
| Validate Expression | POST | `/validate` | 型・制約整合性の判定 |
| Estimate Complexity | POST | `/complexity/estimate` | 近似複雑度の算出 |
| Evaluate MDL | POST | `/mdl/evaluate` | 候補の MDL 評価 |
| Batch Abstract | POST | `/batch/abstract` | 複数入力の一括抽象化 |
| Batch Expand | POST | `/batch/expand` | 複数高位語の一括展開 |

```mermaid
flowchart LR
    A[Client] --> H[/health]
    A --> B[/abstract]
    A --> C[/expand]
    A --> D[/validate]
    A --> E[/complexity/estimate]
    A --> F[/mdl/evaluate]
    A --> G[/batch/abstract]
    A --> I[/batch/expand]
```

## 4. 共通データモデル
### 4.1 共通リクエストメタデータ
```json
{
  "trace_id": "optional-client-trace-id",
  "context": {
    "assumptions": ["..."],
    "forbidden_operations": ["..."],
    "rules": ["..."]
  }
}
```

### 4.2 共通レスポンスメタデータ
```json
{
  "trace_id": "server-trace-id",
  "status": "ok",
  "diagnostics": []
}
```

### 4.3 型表現
```json
{
  "name": "Group",
  "parameters": {
    "commutative": false
  },
  "predicates": [
    "associative",
    "has_identity",
    "has_inverse"
  ]
}
```

### 4.4 検証レポート表現
```json
{
  "is_valid": true,
  "contradictions": [],
  "entailments": ["group_operation_closed"],
  "warnings": [],
  "trace": ["predicate:associative -> satisfied"]
}
```

## 5. 各 API の詳細仕様
### 5.1 GET `/health`
#### 目的
API サービスの稼働状態を返す。

#### リクエスト
なし

#### レスポンス
```json
{
  "trace_id": "2f1c2e54",
  "status": "ok",
  "service": "concept-compression-api",
  "version": "1.0.0"
}
```

#### 例外
- なし。異常時は HTTP 503

---

### 5.2 POST `/abstract`
#### 目的
自然言語文または概念列を、高位語候補へ抽象化する。

#### リクエスト
```json
{
  "trace_id": "req-001",
  "text": "結合律、単位元、逆元を持つ代数構造",
  "top_k": 3,
  "context": {
    "assumptions": ["algebra_domain"],
    "forbidden_operations": [],
    "rules": ["group_axioms"]
  }
}
```

#### 引数
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `trace_id` | `string` | 任意 | クライアント側追跡 ID |
| `text` | `string` | 条件付き必須 | 入力文 |
| `concepts` | `array<object>` | 条件付き必須 | 既に概念化済み入力 |
| `top_k` | `integer` | 任意 | 上位候補数。既定値 5 |
| `context` | `object` | 任意 | 制約文脈 |

`text` または `concepts` のいずれか一方は必須。

#### レスポンス
```json
{
  "trace_id": "req-001",
  "status": "ok",
  "candidates": [
    {
      "surface": "群",
      "type": {
        "name": "Group",
        "parameters": {},
        "predicates": ["associative", "has_identity", "has_inverse"]
      },
      "confidence": 0.93,
      "complexity": {
        "symbol_length": 1.0,
        "structural_cost": 1.2,
        "dependency_cost": 0.4,
        "total_cost": 2.6
      },
      "mdl": {
        "model_cost": 1.1,
        "data_cost": 0.8,
        "penalty_cost": 0.0,
        "total_cost": 1.9,
        "decision": "accept"
      },
      "validation": {
        "is_valid": true,
        "contradictions": [],
        "entailments": ["group_axioms_satisfied"],
        "warnings": [],
        "trace": []
      }
    }
  ],
  "diagnostics": []
}
```

#### 戻り値
- `candidates`: 高位語候補配列
- `diagnostics`: 候補棄却理由や曖昧性情報

#### 例外
- `400 Bad Request`: 入力不足
- `422 Unprocessable Entity`: 構文解析不能
- `409 Conflict`: 制約文脈が自己矛盾
- `500 Internal Server Error`: 予期しない内部障害

---

### 5.3 POST `/expand`
#### 目的
高位語を低位概念列へ展開する。

#### リクエスト
```json
{
  "trace_id": "req-002",
  "term": "群",
  "granularity": "detailed",
  "context": {
    "assumptions": ["algebra_domain"],
    "forbidden_operations": [],
    "rules": ["group_axioms"]
  }
}
```

#### 引数
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `trace_id` | `string` | 任意 | トレース ID |
| `term` | `string` | 必須 | 展開対象高位語 |
| `granularity` | `string` | 任意 | `compact` / `standard` / `detailed` |
| `context` | `object` | 任意 | 制約文脈 |

#### レスポンス
```json
{
  "trace_id": "req-002",
  "status": "ok",
  "term": "群",
  "expansions": [
    {
      "concepts": [
        {"id": "c1", "label": "二項演算"},
        {"id": "c2", "label": "結合律"},
        {"id": "c3", "label": "単位元"},
        {"id": "c4", "label": "逆元"}
      ],
      "type": {
        "name": "Group",
        "parameters": {},
        "predicates": ["associative", "has_identity", "has_inverse"]
      },
      "validation": {
        "is_valid": true,
        "contradictions": [],
        "entailments": ["group_definition_expanded"],
        "warnings": [],
        "trace": []
      },
      "score": 0.95
    }
  ],
  "diagnostics": []
}
```

#### 例外
- `404 Not Found`: 語彙辞書に存在しない高位語
- `422 Unprocessable Entity`: 展開テンプレート不整合
- `409 Conflict`: 文脈と高位語型が矛盾

---

### 5.4 POST `/validate`
#### 目的
文、概念列、高位語のいずれかに対し、型および制約整合性を判定する。

#### リクエスト
```json
{
  "trace_id": "req-003",
  "expression": {
    "term": "可換群",
    "type": {
      "name": "Group",
      "parameters": {
        "commutative": true
      },
      "predicates": ["associative", "has_identity", "has_inverse"]
    }
  },
  "context": {
    "assumptions": ["algebra_domain"],
    "forbidden_operations": [],
    "rules": ["abelian_group_axioms"]
  }
}
```

#### 引数
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `trace_id` | `string` | 任意 | トレース ID |
| `expression` | `object` | 必須 | 検証対象 |
| `context` | `object` | 任意 | 制約文脈 |
| `expected_type` | `object` | 任意 | 想定型 |

#### レスポンス
```json
{
  "trace_id": "req-003",
  "status": "ok",
  "validation": {
    "is_valid": true,
    "contradictions": [],
    "entailments": ["commutative_operation"],
    "warnings": [],
    "trace": [
      "type_check: Group -> ok",
      "predicate_check: commutative -> satisfied"
    ]
  },
  "diagnostics": []
}
```

#### 例外
- `400 Bad Request`: `expression` 欠落
- `422 Unprocessable Entity`: 型推論不能
- `409 Conflict`: 制約矛盾

---

### 5.5 POST `/complexity/estimate`
#### 目的
入力表現の近似複雑度を算出する。

#### リクエスト
```json
{
  "trace_id": "req-004",
  "concepts": [
    {"id": "c1", "label": "結合律"},
    {"id": "c2", "label": "単位元"},
    {"id": "c3", "label": "逆元"}
  ],
  "context": {
    "assumptions": ["algebra_domain"],
    "forbidden_operations": [],
    "rules": ["group_axioms"]
  }
}
```

#### 戻り値
```json
{
  "trace_id": "req-004",
  "status": "ok",
  "complexity": {
    "symbol_length": 8.0,
    "structural_cost": 3.1,
    "dependency_cost": 1.5,
    "total_cost": 12.6,
    "evidence": {
      "concept_count": 3,
      "relation_count": 0
    }
  },
  "diagnostics": []
}
```

#### 例外
- `400 Bad Request`: 入力欠落
- `422 Unprocessable Entity`: 構造不正

---

### 5.6 POST `/mdl/evaluate`
#### 目的
候補高位語または候補集合の MDL スコアを算出する。

#### リクエスト
```json
{
  "trace_id": "req-005",
  "source_complexity": {
    "symbol_length": 8.0,
    "structural_cost": 3.1,
    "dependency_cost": 1.5,
    "total_cost": 12.6
  },
  "candidate": {
    "surface": "群",
    "type": {
      "name": "Group",
      "parameters": {},
      "predicates": ["associative", "has_identity", "has_inverse"]
    },
    "complexity": {
      "symbol_length": 1.0,
      "structural_cost": 1.2,
      "dependency_cost": 0.4,
      "total_cost": 2.6
    },
    "validation": {
      "is_valid": true,
      "contradictions": [],
      "entailments": [],
      "warnings": [],
      "trace": []
    }
  }
}
```

#### レスポンス
```json
{
  "trace_id": "req-005",
  "status": "ok",
  "mdl": {
    "model_cost": 1.1,
    "data_cost": 0.8,
    "penalty_cost": 0.0,
    "total_cost": 1.9,
    "decision": "accept"
  },
  "diagnostics": []
}
```

#### 例外
- `400 Bad Request`: 入力項不足
- `422 Unprocessable Entity`: 複雑度形式不正

---

### 5.7 POST `/batch/abstract`
#### 目的
複数テキストの一括抽象化を行う。

#### リクエスト
```json
{
  "trace_id": "req-006",
  "items": [
    {"text": "結合律、単位元、逆元を持つ代数構造"},
    {"text": "情報を短い高位表現に圧縮する操作"}
  ],
  "top_k": 2,
  "context": {
    "assumptions": [],
    "forbidden_operations": [],
    "rules": []
  }
}
```

#### レスポンス
各 item ごとに `/abstract` と同等の結果を返す。

#### 例外
- `400 Bad Request`: `items` 空配列
- `413 Payload Too Large`: 件数超過

---

### 5.8 POST `/batch/expand`
#### 目的
複数高位語の一括展開を行う。

#### リクエスト
```json
{
  "trace_id": "req-007",
  "items": [
    {"term": "群"},
    {"term": "ゼロトラスト"}
  ],
  "granularity": "standard",
  "context": {
    "assumptions": [],
    "forbidden_operations": [],
    "rules": []
  }
}
```

#### レスポンス
各 item ごとに `/expand` と同等の結果を返す。

#### 例外
- `400 Bad Request`: `items` 空配列
- `413 Payload Too Large`: 件数超過

## 6. Python 使用例
### 6.1 サービス API の想定インターフェース
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AbstractRequest:
    text: Optional[str]
    concepts: Optional[list]
    top_k: int = 5
    context: Optional[dict] = None

@dataclass
class ExpandRequest:
    term: str
    granularity: str = "standard"
    context: Optional[dict] = None

class ConceptCompressionService:
    def abstract_text(self, request: AbstractRequest) -> dict:
        ...

    def expand_term(self, request: ExpandRequest) -> dict:
        ...

    def validate_expression(self, expression: dict, context: Optional[dict] = None) -> dict:
        ...

    def estimate_complexity(self, payload: dict) -> dict:
        ...

    def evaluate_mdl(self, payload: dict) -> dict:
        ...
```

### 6.2 抽象化 API 使用例
```python
service = ConceptCompressionService()

result = service.abstract_text(
    AbstractRequest(
        text="結合律、単位元、逆元を持つ代数構造",
        top_k=3,
        context={"assumptions": ["algebra_domain"]}
    )
)

for candidate in result["candidates"]:
    print(candidate["surface"], candidate["mdl"]["total_cost"])
```

### 6.3 展開 API 使用例
```python
result = service.expand_term(
    ExpandRequest(
        term="群",
        granularity="detailed",
        context={"assumptions": ["algebra_domain"]}
    )
)

for expansion in result["expansions"]:
    labels = [c["label"] for c in expansion["concepts"]]
    print(labels)
```

### 6.4 検証 API 使用例
```python
validation = service.validate_expression(
    expression={
        "term": "可換群",
        "type": {
            "name": "Group",
            "parameters": {"commutative": True},
            "predicates": ["associative", "has_identity", "has_inverse"]
        }
    },
    context={"rules": ["abelian_group_axioms"]}
)

print(validation["validation"]["is_valid"])
```

## 7. エラーハンドリング
### 7.1 エラーレスポンス形式
```json
{
  "trace_id": "req-err-001",
  "status": "error",
  "error": {
    "code": "TYPE_MISMATCH",
    "message": "期待型 Group と実際型 Ring が一致しません",
    "details": {
      "expected": "Group",
      "actual": "Ring"
    }
  },
  "diagnostics": [
    "type_check: Group <- Ring failed"
  ]
}
```

### 7.2 エラーコード一覧
| コード | HTTP | 説明 |
|---|---|---|
| `INVALID_REQUEST` | 400 | 必須フィールド不足、形式不正 |
| `PARSE_ERROR` | 422 | 入力解析失敗 |
| `TYPE_MISMATCH` | 422 | 型不整合 |
| `CONSTRAINT_VIOLATION` | 409 | 制約違反 |
| `UNKNOWN_TERM` | 404 | 辞書未登録語 |
| `AMBIGUOUS_TERM` | 422 | 曖昧性が高すぎる |
| `KNOWLEDGE_LOOKUP_FAILED` | 503 | 外部知識または辞書参照失敗 |
| `INTERNAL_ERROR` | 500 | 予期しない障害 |

### 7.3 エラー設計原則
- エラーコードは機械可読
- メッセージは人間可読
- `details` には補助データを格納
- `diagnostics` には推論トレースを含める
- 重大制約違反と単なる警告を分離する

### 7.4 リトライ方針
- `500`, `503` はリトライ対象
- `400`, `404`, `409`, `422` は通常リトライ非推奨
- バッチ API では部分失敗を許容し、項目単位結果を返すことが望ましい

## 8. バージョニング方針
- URL にメジャーバージョンを含める: `/api/v1`
- 後方互換を壊す変更は `v2` 以降で提供
- フィールド追加は後方互換な変更として許容
- エラーコードの意味変更は禁止

## 9. 関連文書
- 理論的基盤: [01_theoretical_foundation.md](./01_theoretical_foundation.md)
- 要件定義: [02_requirements.md](./02_requirements.md)
- アーキテクチャ設計: [03_architecture.md](./03_architecture.md)
- 実装仕様: [04_implementation_spec.md](./04_implementation_spec.md)

```mermaid
flowchart TD
    A[01 理論的基盤] --> B[02 要件定義]
    B --> C[03 アーキテクチャ設計]
    C --> D[04 実装仕様]
    D --> E[05 API 仕様]