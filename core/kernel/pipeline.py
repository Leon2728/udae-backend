"""Deterministic pipeline orchestrator.

This module implements the core pipeline that orchestrates stage execution.
The pipeline does NOT evaluate, does NOT interpret, does NOT transform content.
It ONLY orchestrates stages and stops on blocking failures.
"""

from typing import List

from .context import PipelineContext
from .errors import BlockingStageError
from .stages import StageDefinition, StageResult


class Pipeline:
    """Deterministic pipeline orchestrator.
    
    The pipeline executes stages in order and stops immediately
    when a blocking stage fails. No business logic is performed.
    
    Attributes:
        stages: Ordered list of stage definitions to execute
    """
    
    def __init__(self, stages: List[StageDefinition]):
        """Initialize pipeline with ordered stages.
        
        Args:
            stages: List of StageDefinition objects in execution order
        """
        self.stages = stages
        self._results: List[StageResult] = []
    
    def execute(self, context: PipelineContext) -> List[StageResult]:
        """Execute pipeline stages in order.
        
        Executes each stage sequentially. If a stage returns ok=False
        and blocking=True, execution stops immediately.
        
        Args:
            context: Immutable pipeline context
            
        Returns:
            List of StageResult objects for executed stages
            
        Raises:
            BlockingStageError: When a blocking stage fails
        """
        self._results = []
        
        for stage_def in self.stages:
            # Execute stage function with context
            result = stage_def.fn(context)
            
            # Register result
            self._results.append(result)
            
            # Check for blocking failure
            if not result.ok and result.blocking:
                raise BlockingStageError(
                    stage_name=stage_def.name.value,
                    reason="Stage failed with blocking=True",
                    details={
                        "error": result.error,
                        "output": result.output
                    }
                )
        
        return self._results
    
    @property
    def results(self) -> List[StageResult]:
        """Get results from last execution.
        
        Returns:
            List of StageResult objects
        """
        return self._results.copy()
