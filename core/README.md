# Core

This is the **heart of UDAE**: the deterministic normative decision engine.

## Principles
- **Zero dependencies on adapters**
- **Pure business logic**
- **Immutable data structures**
- **Deterministic evaluation**
- **Explicit rule-based decisions**

## Submodules
- `kernel/` - Pipeline orchestration and normative engine core
- `amanecer/` - Document parsing and structural extraction
- `fenix/` - Normative rule loading and interpretation
- `arana/` - Rule evaluation and compliance checking
- `ire/` - Report generation and evidence assembly
- `models/` - Immutable domain models

## What NOT to put here
- No web frameworks
- No database drivers
- No file I/O logic
- No UI concerns
- No ML/LLM inference