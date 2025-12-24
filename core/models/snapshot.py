"""Snapshot model — Immutable document state at evaluation time.

A snapshot is the complete state of a document as extracted by amanecer.
It cannot change. Its identity is its hash.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from .hashes import hash_json


@dataclass(frozen=True)
class Snapshot:
    """Immutable document snapshot.
    
    Attributes:
        snapshot_id: Canonical identifier (computed hash).
        document_name: Name or identifier of source document.
        document_hash: Hash of original document for integrity.
        extracted_fields: Dict of extracted document fields and values.
        extraction_timestamp: ISO 8601 timestamp of extraction.
        extraction_version: Version of extraction engine (amanecer).
    """
    document_name: str
    document_hash: str
    extracted_fields: Dict[str, Any]
    extraction_timestamp: str
    extraction_version: str
    snapshot_id: str = field(default="", init=False)
    
    def __post_init__(self) -> None:
        """Compute snapshot_id as hash of snapshot content."""
        snapshot_dict = {
            'document_name': self.document_name,
            'document_hash': self.document_hash,
            'extracted_fields': self.extracted_fields,
            'extraction_timestamp': self.extraction_timestamp,
            'extraction_version': self.extraction_version,
        }
        object.__setattr__(self, 'snapshot_id', hash_json(snapshot_dict))
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        return (f"Snapshot(document={self.document_name!r}, "
                f"snapshot_id={self.snapshot_id[:8]}...)")
    
    def __hash__(self) -> int:
        """Hash based on snapshot_id."""
        return hash(self.snapshot_id)
    
    def __eq__(self, other: object) -> bool:
        """Equality based on snapshot_id."""
        if not isinstance(other, Snapshot):
            return NotImplemented
        return self.snapshot_id == other.snapshot_id
