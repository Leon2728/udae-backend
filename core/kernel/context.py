"""Immutable pipeline execution context.

This module defines the frozen context passed through pipeline stages.
Context is read-only and carries no business logic.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PipelineContext:
    """Immutable context for pipeline execution.
    
    This context is passed to each stage and cannot be modified.
    All fields are frozen at creation time.
    
    Attributes:
        document_ref: Reference identifier for the document being processed
        normative_context: Normative framework identifier or reference
        facts_snapshot: Optional snapshot of document facts
        run_id: Unique identifier for this pipeline execution
        meta: Immutable metadata mapping
    """
    
    document_ref: str
    normative_context: str
    facts_snapshot: Any | None
    run_id: str
    meta: Mapping[str, Any]
    
    def __post_init__(self):
        """Validate immutability of meta field."""
        if not isinstance(self.meta, Mapping):
            raise TypeError("meta must be a Mapping")
