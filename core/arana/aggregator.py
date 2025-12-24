"""Verdict aggregation logic."""

from typing import List, Tuple
from core.models.verdict import Verdict


def aggregate_verdicts(verdicts: List[Verdict]) -> Tuple[List[Verdict], List[Verdict], List[Verdict], List[Verdict]]:
    """Aggregate verdicts by result and blocking status.
    
    Args:
        verdicts: List of Verdict instances
        
    Returns:
        Tuple of (blocking_failures, non_blocking_failures, blocking_passes, non_blocking_passes)
    """
    blocking_failures: List[Verdict] = []
    non_blocking_failures: List[Verdict] = []
    blocking_passes: List[Verdict] = []
    non_blocking_passes: List[Verdict] = []
    
    for v in verdicts:
        is_blocking = v.severity == "error"
        is_failure = v.result == "FAIL"
        
        if is_failure and is_blocking:
            blocking_failures.append(v)
        elif is_failure and not is_blocking:
            non_blocking_failures.append(v)
        elif not is_failure and is_blocking:
            blocking_passes.append(v)
        else:
            non_blocking_passes.append(v)
    
    return blocking_failures, non_blocking_failures, blocking_passes, non_blocking_passes
