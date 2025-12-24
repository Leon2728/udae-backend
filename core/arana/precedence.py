"""Precedence rules for decision logic."""

from typing import List
from core.models.verdict import Verdict


def apply_precedence(blocking_failures: List[Verdict]) -> str:
    """Apply precedence rules to determine final decision.
    
    Hard rule: If any blocking failure exists → FAIL
    Otherwise → PASS
    
    Args:
        blocking_failures: List of blocking (error-level) failure verdicts
        
    Returns:
        "PASS" or "FAIL"
    """
    if len(blocking_failures) > 0:
        return "FAIL"
    return "PASS"
