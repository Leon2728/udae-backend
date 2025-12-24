"""Araña stage for pipeline integration."""

from dataclasses import dataclass
from typing import List, Any
from core.models.verdict import Verdict
from .aggregator import aggregate_verdicts
from .precedence import apply_precedence
from .decision import Decision


@dataclass(frozen=True)
class StageResult:
    """Pipeline stage result."""
    blocking: bool
    ok: bool
    output: Any


class AranaStage:
    """Pipeline stage for Araña decision engine."""
    
    def execute(self, verdicts: List[Verdict]) -> StageResult:
        """Execute decision logic on verdicts.
        
        Args:
            verdicts: List of Verdict instances from Amanecer
            
        Returns:
            StageResult with blocking=True, ok based on decision, output=Decision
        """
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
