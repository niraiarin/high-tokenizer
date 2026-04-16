# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a theoretical research paper proposing that **technical terminology is "logical compression of concepts"** — integrating statistical learning with logical verification. The central hypothesis: specialized terms compress multiple concepts, premises, and constraints into short symbol sequences while preserving logical structure.

There is **no implementation code yet**. The repository consists entirely of theory documents and design specifications. Class names, API names, and algorithms in the docs are proposed specifications derived from the theory.

## Repository Structure

- `docs/` — 10-chapter academic paper + design documents
  - Chapters 01-06: Theory foundations (completed, high quality)
  - Chapter 07: Theoretical analysis (partially complete — sections 7.3, 7.4, 7.6 done; 7.1, 7.2, 7.5 blocked on implementation)
  - Chapter 08: Experimental evaluation (blocked on implementation)
  - Chapters 09-10: Discussion and conclusion (need revision after experiments)
  - `02_requirements.md`, `03_architecture.md`, `04_implementation_spec.md`, `05_api_specification.md` — System design docs (separate from the paper chapters with same numbers)
  - `REVIEW_CHAPTER_*.md`, `REVIEW_SUMMARY.md` — Critical review reports for chapters 7-10
  - `PROGRESS_AND_NEXT_STEPS.md` — Current status and phased work plan
- `chatlog.md` — Original conversation log that spawned the research

## Key Theoretical Concepts

- **Probabilistic type system**: Integrates statistical compression with logical constraints (Ch. 5.1)
- **Dynamic compression theory**: Time evolution of compression rates during learning, explains Grokking (Ch. 5.2)
- **Three-layer constraint verification**: Type checking, constraint satisfaction, logical verification (Ch. 5.3)
- **Capacity-dependent compression theory**: Integrates with Scaling Laws, derives optimal model size (Ch. 5.6)
  - Optimal compression: `C_optimal(N) = C_∞(1 - e^(-βN))`
  - Optimal model size: `N* = Nc(αL₀/λ)^(1/(1+α))`

## Current Status

The project is at **Phase 1: awaiting implementation**. All subsequent phases (experiments, remaining theory sections, revisions) are blocked until a working implementation exists. See `docs/PROGRESS_AND_NEXT_STEPS.md` for the full phased plan.

## Terminology Conventions

All documents use these terms consistently:
- **Abstraction/compression** (抽象化): Compressing concepts
- **Decompression/expansion** (展開): Expanding compressed concepts
- **Constraint validation** (制約検証): Verifying logical constraints
- **High-order term** (高位語): Highly compressed concept representation
- **Low-order concepts** (低位概念): Expanded base concept sequences

## Language

Documents are written in Japanese. When editing or extending them, maintain Japanese unless instructed otherwise.
