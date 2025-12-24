"""Contract: amanecer (extraction) → fenix (rule loading).

Defines the protocol (interface) between the document extraction layer
and the rule loading layer.

Amanecer produces Snapshots. Fenix consumes them and produces Rule sets.
No implementation. Only types and documentation.
"""

from typing import Protocol, List, Dict, Any
from dataclasses import dataclass


class AmanecerOutput(Protocol):
    """Output produced by amanecer (document extraction).
    
    Amanecer extracts structure and content from a document.
    Output must be consumable by fenix without transformation.
    """
    
    def get_document_name(self) -> str:
        """Return canonical document identifier."""
        ...
    
    def get_document_hash(self) -> str:
        """Return SHA-256 hash of original document."""
        ...
    
    def get_extracted_fields(self) -> Dict[str, Any]:
        """Return extracted document fields.
        
        Structure must be JSON-serializable.
        No circular references.
        All values must be inspectable.
        """
        ...
    
    def get_extraction_timestamp(self) -> str:
        """Return ISO 8601 timestamp of extraction."""
        ...
    
    def get_extraction_version(self) -> str:
        """Return semantic version of extraction engine."""
        ...


class FenixInput(Protocol):
    """Input expected by fenix (rule loading).
    
    Fenix receives extracted document state and maps it to evaluable rules.
    Must implement Snapshot interface from core.models.
    """
    
    @property
    def document_name(self) -> str:
        """Canonical document identifier."""
        ...
    
    @property
    def document_hash(self) -> str:
        """SHA-256 hash of original document."""
        ...
    
    @property
    def extracted_fields(self) -> Dict[str, Any]:
        """Extracted document fields (JSON-serializable)."""
        ...
    
    @property
    def extraction_timestamp(self) -> str:
        """ISO 8601 timestamp."""
        ...
    
    @property
    def extraction_version(self) -> str:
        """Semantic version of extraction engine."""
        ...
    
    @property
    def snapshot_id(self) -> str:
        """Canonical identity hash (SHA-256)."""
        ...


# PROTOCOL INVARIANTS
# (These are not enforced at runtime, but document the contract)

"""
1. Determinism
   - Same document + same extractor version → same snapshot
   - snapshot_id must be reproducible

2. Immutability
   - Snapshot cannot change after creation
   - All fields are read-only

3. Completeness
   - Snapshot must contain all document fields needed by rules
   - No lazy loading
   - No external state access during evaluation

4. Auditability
   - snapshot_id must be computable by any auditor
   - extraction_version must be fixed and traceable

5. No Coupling
   - Fenix does not care HOW amanecer extracted fields
   - Only cares that fields are present and valid
   - Fenix must not modify the snapshot
"""
