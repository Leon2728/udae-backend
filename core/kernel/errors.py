"""Pipeline control flow errors.

This module defines exceptions for pipeline execution control.
These are NOT business logic errors, only flow control.
"""

from typing import Any


class BlockingStageError(Exception):
    """Raised when a blocking stage fails.
    
    This error stops pipeline execution immediately.
    
    Attributes:
        stage_name: Name of the failed stage
        reason: Human-readable failure reason
        details: Optional additional context
    """
    
    def __init__(self, stage_name: str, reason: str, details: Any | None = None):
        self.stage_name = stage_name
        self.reason = reason
        self.details = details
        super().__init__(f"Blocking stage '{stage_name}' failed: {reason}")


class NonBlockingStageError(Exception):
    """Raised when a non-blocking stage fails.
    
    Pipeline execution continues despite this error.
    
    Attributes:
        stage_name: Name of the failed stage
        reason: Human-readable failure reason
        details: Optional additional context
    """
    
    def __init__(self, stage_name: str, reason: str, details: Any | None = None):
        self.stage_name = stage_name
        self.reason = reason
        self.details = details
        super().__init__(f"Non-blocking stage '{stage_name}' failed: {reason}")
