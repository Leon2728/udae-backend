"""Verdict model — Immutable decision result of rule evaluation.

A verdict is the outcome of evaluating a rule against evidence and snapshot.
It cannot be changed. Its identity is its hash.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .hashes import hash_json


@dataclass(frozen=True)
class Verdict:
    """Immutable rule evaluation decision.
    
    Attributes:
        verdict_id: Canonical identifier (computed hash).
        rule_id: ID of the rule that was evaluated.
        snapshot_id: ID of the document snapshot evaluated.
        result: "PASS" or "FAIL" (binary decision).
        evidence_ids: List of evidence IDs that determined this verdict.
        reasoning: Human-readable explanation of the decision.
        severity: Inherited from rule ("error", "warning", "info").
    """
    rule_id: str
    snapshot_id: str
    result: str  # "PASS" or "FAIL"
    evidence_ids: List[str]
    reasoning: str
    severity: str
    verdict_id: str = field(default="", init=False)
    
    def __post_init__(self) -> None:
        """Compute verdict_id as hash of verdict content."""
        verdict_dict = {
            'rule_id': self.rule_id,
            'snapshot_id': self.snapshot_id,
            'result': self.result,
            'evidence_ids': sorted(self.evidence_ids),
            'reasoning': self.reasoning,
            'severity': self.severity,
        }
        object.__setattr__(self, 'verdict_id', hash_json(verdict_dict))
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        return (f"Verdict(result={self.result!r}, "
                f"verdict_id={self.verdict_id[:8]}...)")
    
    def __hash__(self) -> int:
        """Hash based on verdict_id."""
        return hash(self.verdict_id)
    
    def __eq__(self, other: object) -> bool:
        """Equality based on verdict_id."""
        if not isinstance(other, Verdict):
            return NotImplemented
        return self.verdict_id == other.verdict_id
