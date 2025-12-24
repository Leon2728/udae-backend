"""Stage definitions for the deterministic pipeline.

This module defines the core abstractions for pipeline stages.
Stages are pure orchestration units with no business logic.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class StageName(str, Enum):
    """Enumeration of available pipeline stages."""
    
    STAGE_A = "stage_a"
    STAGE_B = "stage_b"
    STAGE_C = "stage_c"


@dataclass(frozen=True)
class StageResult:
    """Immutable result of a stage execution.
    
    Attributes:
        ok: Whether the stage completed successfully
        blocking: Whether failure should stop pipeline execution
        output: Optional data produced by the stage
        error: Optional exception if stage failed
    """
    
    ok: bool
    blocking: bool
    output: Any | None = None
    error: Exception | None = None


@dataclass(frozen=True)
class StageDefinition:
    """Definition of a pipeline stage.
    
    Attributes:
        name: Unique identifier for the stage
        blocking: Whether this stage is blocking on failure
        fn: Callable that executes the stage logic
    """
    
    name: StageName
    blocking: bool
    fn: Callable[[Any], StageResult]
