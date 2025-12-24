"""Final decision structure."""

from dataclasses import dataclass, field
from typing import List
from core.models.verdict import Verdict
from core.models.hashes import hash_json


@dataclass(frozen=True)
class Decision:
    """Immutable final decision from Araña.
    
    Attributes:
        status: "PASS" or "FAIL" final decision
        blocking_failures: Verdicts that caused failure (error + FAIL)
        non_blocking_failures: Warnings/info that failed but don't block
        all_verdicts: Complete list of all verdicts evaluated
        decision_hash: Deterministic hash of decision content
    """
    status: str
    blocking_failures: List[Verdict]
    non_blocking_failures: List[Verdict]
    all_verdicts: List[Verdict]
    decision_hash: str = field(default="", init=False)
    
    def __post_init__(self) -> None:
        """Compute decision_hash deterministically."""
        # Sort verdicts by verdict_id for determinism
        sorted_blocking = sorted([v.verdict_id for v in self.blocking_failures])
        sorted_non_blocking = sorted([v.verdict_id for v in self.non_blocking_failures])
        sorted_all = sorted([v.verdict_id for v in self.all_verdicts])
        
        decision_dict = {
            'status': self.status,
            'blocking_failures': sorted_blocking,
            'non_blocking_failures': sorted_non_blocking,
            'all_verdicts': sorted_all,
        }
        object.__setattr__(self, 'decision_hash', hash_json(decision_dict))
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        return (f"Decision(status={self.status!r}, "
                f"blocking_failures={len(self.blocking_failures)}, "
                f"hash={self.decision_hash[:8]}...)")
