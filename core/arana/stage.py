"""Araña stage for pipeline integration."""

from typing import List
from core.kernel.stages import StageResult
from core.kernel.context import PipelineContext
from core.models.verdict import Verdict
from .aggregator import aggregate_verdicts
from .precedence import apply_precedence
from .decision import Decision


class AranaStage:
    """Pipeline stage for Araña decision engine."""
    
    def execute(self, context: PipelineContext) -> StageResult:
        """Execute decision logic on verdicts from context.
        
        Args:
            context: PipelineContext containing verdicts in meta["verdicts"]
            
        Returns:
            StageResult with blocking=True, ok based on decision, output=Decision
        """
        # Extract verdicts from context deterministically
        verdicts: List[Verdict] = list(context.meta.get("verdicts", []))
        
        # Aggregate verdicts
        blocking_failures, non_blocking_failures, _, _ = aggregate_verdicts(verdicts)
        
        # Apply precedence
        status = apply_precedence(blocking_failures)
        
        # Create decision
        decision = Decision(
            status=status,
            blocking_failures=blocking_failures,
            non_blocking_failures=non_blocking_failures,
            all_verdicts=verdicts
        )
        
        # Return stage result
        return StageResult(
            blocking=True,
            ok=(status == "PASS"),
            output=decision
        )
