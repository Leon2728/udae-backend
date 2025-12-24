"""Evidence model — Immutable fact extracted from document.

Evidence is a single verifiable fact extracted from a document.
It cannot be changed. Its identity is its hash.
"""

from dataclasses import dataclass, field
from typing import Optional
from .hashes import hash_json


@dataclass(frozen=True)
class Evidence:
    """Immutable fact from document.
    
    Attributes:
        evidence_id: Canonical identifier (computed hash).
        field_path: Path to field in document (e.g., "title", "authors[0].name").
        extracted_value: The actual value extracted from document.
        value_type: Type of value ("string", "number", "list", etc.).
        confidence: Extraction confidence (0.0-1.0).
        source_context: Optional context snippet from document.
    """
    field_path: str
    extracted_value: str
    value_type: str
    confidence: float
    source_context: Optional[str] = None
    evidence_id: str = field(default="", init=False)
    
    def __post_init__(self) -> None:
        """Compute evidence_id as hash of evidence content."""
        evidence_dict = {
            'field_path': self.field_path,
            'extracted_value': self.extracted_value,
            'value_type': self.value_type,
            'confidence': self.confidence,
            'source_context': self.source_context,
        }
        object.__setattr__(self, 'evidence_id', hash_json(evidence_dict))
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        return (f"Evidence(field={self.field_path!r}, "
                f"evidence_id={self.evidence_id[:8]}...)")
    
    def __hash__(self) -> int:
        """Hash based on evidence_id."""
        return hash(self.evidence_id)
    
    def __eq__(self, other: object) -> bool:
        """Equality based on evidence_id."""
        if not isinstance(other, Evidence):
            return NotImplemented
        return self.evidence_id == other.evidence_id
