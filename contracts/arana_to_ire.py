"""Contract: arana (evaluation) → ire (reporting).

Defines protocol between evaluation and reporting layers.
Arana produces Verdicts. Ire consumes them and produces reports.
"""

from typing import Protocol, List


class AranaOutput(Protocol):
    """Output from arana (rule evaluation)."""
    
    def get_verdict_id(self) -> str:
        """Canonical verdict identifier (SHA-256)."""
        ...
    
    def get_result(self) -> str:
        """PASS or FAIL."""
        ...
    
    def get_severity(self) -> str:
        """Inherited from rule: error | warning | info."""
        ...


class IreInput(Protocol):
    """Input expected by ire (reporting).
    
    Ire receives verdicts and formats them as audit reports.
    Must implement Verdict interface from core.models.
    """
    
    @property
    def verdict_id(self) -> str:
        """Canonical verdict identifier (SHA-256)."""
        ...
    
    @property
    def result(self) -> str:
        """PASS or FAIL."""
        ...
    
    @property
    def severity(self) -> str:
        """Error | Warning | Info."""
        ...
    
    @property
    def reasoning(self) -> str:
        """Human-readable explanation."""
        ...


# PROTOCOL INVARIANTS
"""
1. Auditability
   - All verdicts must be traceable to rules and evidence
   - Reports must include chains of custody

2. Immutability
   - Verdicts cannot be modified by ire
   - Reports are derived, not mutated

3. Completeness
   - All verdicts must appear in reports
   - No filtering by ire

4. Clarity
   - Reasoning must be human-inspectable
   - No summarization that loses detail
"""
