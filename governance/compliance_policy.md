# Compliance Policy

## Auditability Requirements
Every decision made by UDAE Backend must be:
1. **Explainable**: traceable to explicit normative rule
2. **Reproducible**: same input + same rules = same output
3. **Verifiable**: evidence chain must be complete
4. **Immutable**: audit trail cannot be altered post-execution

## Prohibited Practices
- ❌ Heuristic scoring without explicit rule basis
- ❌ ML/LLM decisions in core evaluation pipeline
- ❌ Mutable rule application
- ❌ Hidden state or side effects
- ❌ Non-deterministic evaluation order

## Audit Trail Requirements
- Every evaluation must produce:
  - Input snapshot hash
  - Ruleset version identifier
  - Complete evidence list
  - Execution timestamp
  - Deterministic result

## Compliance Verification
- Architecture guards must enforce layer boundaries
- Determinism tests must verify reproducibility
- Auditability tests must validate evidence completeness

## Status
Policy active from repository initialization.