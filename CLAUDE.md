# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a theoretical research paper proposing that **technical terminology is "logical compression of concepts"** — integrating statistical learning with logical verification. The central hypothesis: specialized terms compress multiple concepts, premises, and constraints into short symbol sequences while preserving logical structure.

The project uses a **spec-driven + test-driven** development methodology based on `docs/ref/spec_system.md`. Formal specifications are written in a custom S-expression DSL, processed through a pipeline (DSL → AST → Lean → SMT → Test → Python), and verified by the Lean compiler and Z3 SMT solver.

## Repository Structure

- `pipeline/` — Spec-driven development pipeline (Python)
  - `dsl/` — S-expression DSL parser (`parser.py`, `ast.py`)
  - `codegen/` — Code generation (Lean: `lean_gen.py`, SMT: `smt_gen.py`, Python: `python_gen.py`)
  - `testgen/` — Automatic test generation from FuncSpec pre-conditions (`pytest_gen.py`)
  - `llm/` — LLM refinement loop: `S_{n+1} = Fix(LLM(S_n), Verify)` (`refine_loop.py`)
  - `verify/` — Refinement partial order verification
- `lean/` — Lean 4 formal specifications (v4.29.0)
  - `SpecSystem/Basic.lean` — TypeSpec, FuncSpec, refinement partial order (proved, no sorry)
  - `SpecSystem/DSL/` — AST types and DSL parser FuncSpecs
  - `SpecTest.lean` — LSpec compile-time property tests
- `specs/` — DSL specification files
  - `high_tokenizer/` — Formal specs for all 6 high-tokenizer components
  - `spec_system_core.spec`, `dsl_spec.spec`, `dsl_parser.spec` — Pipeline self-hosting specs
- `high_tokenizer/` — Main package (implementation via TDD in Phase A-3)
- `tests/` — pytest test suites (97 tests)
- `docs/` — Research paper (10-chapter academic paper + design documents, Japanese)
  - `ref/` — Technical references (`spec_system.md`, `dsl_grammar.md`, `lean_dsl_best_practices.md`)

## Development

```bash
uv sync --group dev          # Install dev dependencies
uv run pytest                # Run tests (97 passed, 1 skipped)
uv run ruff check .          # Lint
uv run ruff format --check . # Format check
uv run pyright               # Type check
cd lean && lake build         # Build Lean specs
```

## Current Status

- **Phase A-1** (pipeline construction): Complete. 5-stage bootstrap (B0-B4) with self-hosting.
- **Phase A-2** (Lean formal specs): Complete. 6 component specs through full pipeline.
- **Phase A-3** (Python TDD implementation): Not started. Next phase — TDD against auto-generated tests.
- **Phases A-3 → Gap 3 → Gap 2 → Gap 4**: Blocked on A-3 completion.

See GitHub Issues #1 (project overview), #2 (Gap 1 phases), #7 (A-1 bootstrap) for full plan.

## Key Theoretical Concepts

- **Probabilistic type system**: Integrates statistical compression with logical constraints (Ch. 5.1)
- **Dynamic compression theory**: Time evolution of compression rates during learning, explains Grokking (Ch. 5.2)
- **Three-layer constraint verification**: Type checking, constraint satisfaction, logical verification (Ch. 5.3)
- **Capacity-dependent compression theory**: Integrates with Scaling Laws, derives optimal model size (Ch. 5.6)

## Terminology Conventions

All documents use these terms consistently:
- **Abstraction/compression** (抽象化): Compressing concepts
- **Decompression/expansion** (展開): Expanding compressed concepts
- **Constraint validation** (制約検証): Verifying logical constraints
- **High-order term** (高位語): Highly compressed concept representation
- **Low-order concepts** (低位概念): Expanded base concept sequences

## Language

Paper documents (`docs/01-10`) are written in Japanese. Technical references (`docs/ref/`) and code are in English. When editing paper chapters, maintain Japanese unless instructed otherwise.
