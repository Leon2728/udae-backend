"""Rule model — Immutable normative decision rule.

A rule is the smallest unit of normative decision logic in UDAE.
It cannot be changed once created. Its identity is its hash.
"""

from dataclasses import dataclass, field
from typing import Optional
from .hashes import hash_json


@dataclass(frozen=True)
class Rule:
    """Immutable rule for normative decision.
    
    Attributes:
        rule_id: Canonical identifier (set by __post_init__).
        code: Unique rule code (e.g., "APA7_TITLE_FORMAT").
        version: Semantic version of the rule.
        description: Human-readable rule description.
        logic_type: Type of logic ("binary", "sequential", "conditional").
        condition: Optional conditional logic in structured format.
        consequent: Expected outcome if rule passes.
        evidence_field: Document field this rule evaluates.
        severity: "error", "warning", "info".
    """
    code: str
    version: str
    description: str
    logic_type: str
    consequent: str
    evidence_field: str
    severity: str
    condition: Optional[str] = None
    rule_id: str = field(default="", init=False)
    
    def __post_init__(self) -> None:
        """Compute rule_id as hash of rule content."""
        rule_dict = {
            'code': self.code,
            'version': self.version,
            'description': self.description,
            'logic_type': self.logic_type,
            'condition': self.condition,
            'consequent': self.consequent,
            'evidence_field': self.evidence_field,
            'severity': self.severity,
        }
        object.__setattr__(self, 'rule_id', hash_json(rule_dict))
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        return (f"Rule(code={self.code!r}, version={self.version!r}, "
                f"rule_id={self.rule_id[:8]}...)")
    
    def __hash__(self) -> int:
        """Hash based on rule_id for use in sets and dicts."""
        return hash(self.rule_id)
    
    def __eq__(self, other: object) -> bool:
        """Equality based on rule_id."""
        if not isinstance(other, Rule):
            return NotImplemented
        return self.rule_id == other.rule_id
