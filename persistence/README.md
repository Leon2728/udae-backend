# Persistence

Data persistence layer.

## Responsibility
Store and retrieve audit trails, rules, and snapshots.

## Principles
- Append-only stores
- Immutable records
- Hash-based identity

## Submodules
- `audit_store/` - Immutable audit trail storage
- `rule_store/` - Version-controlled normative rules
- `snapshot_store/` - Document snapshot archive

## Status
Architecture defined. Implementation pending.