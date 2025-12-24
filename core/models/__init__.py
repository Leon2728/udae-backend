"""Core domain models for UDAE.

All models are immutable by design (@dataclass(frozen=True)).
All models have deterministic hash identity (SHA-256).
No external dependencies. No IO. No database logic.

Canonical exports:
- Rule: Immutable normative rule
- Snapshot: Immutable document state
- Evidence: Immutable extracted fact
- Verdict: Immutable rule evaluation result
- Hash utilities: SHA-256 hashing functions
"""

from .hashes import hash_bytes, hash_json, hash_string
from .rule import Rule
from .snapshot import Snapshot
from .evidence import Evidence
from .verdict import Verdict

__all__ = [
    'hash_bytes',
    'hash_json',
    'hash_string',
    'Rule',
    'Snapshot',
    'Evidence',
    'Verdict',
]
