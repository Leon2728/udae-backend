"""Contract: fenix (rule loading) → arana (evaluation).

Defines the protocol between the rule loading layer and the evaluation layer.

Fenix produces Rules. Arana consumes them and evaluates against Snapshots.
No implementation. Only types and documentation.
"""

from typing import Protocol, List, Dict, Any


class FenixOutput(Protocol):
    """Output produced by fenix (rule loading).
    
    Fenix loads normative rules from authoritative sources.
    Rules define what must be evaluated against documents.
    """
    
    def get_rule_id(self) -> str:
        """Return canonical rule identifier (SHA-256 hash)."""
        ...
    
    def get_rule_code(self) -> str:
        """Return unique rule code (e.g., 'APA7_TITLE_FORMAT')."""
        ...
    
    def get_rule_version(self) -> str:
        """Return semantic version of rule."""
        ...
    
    def get_severity(self) -> str:
        """Return severity level: 'error', 'warning', or 'info'."""
        ...


class AranaInput(Protocol):
    """Input expected by arana (evaluation).
    
    Arana receives rules and evaluates them against snapshots.
    Must implement Rule interface from core.models.
    """
    
    @property
    def rule_id(self) -> str:
        """Canonical rule identifier (SHA-256)."""
        ...
    
    @property
    def code(self) -> str:
        """Unique rule code."""
        ...
    
    @property
    def version(self) -> str:
        """Semantic version."""
        ...
    
    @property
    def severity(self) -> str:
        """Error | Warning | Info."""
        ...
    
    @property
    def logic_type(self) -> str:
        """Type of logic: 'binary', 'sequential', 'conditional'."""
        ...
    
    @property
    def condition(self) -> str:
        """Optional conditional logic."""
        ...
    
    @property
    def consequent(self) -> str:
        """Expected outcome if rule passes."""
        ...


# PROTOCOL INVARIANTS
"""
1. Rule Immutability
   - Rules cannot change after loading
   - rule_id must be reproducible

2. Deterministic Evaluation
   - Same rule + same snapshot → same result
   - No external state access
   - No randomness

3. Completeness
   - All information needed for evaluation must be in the rule
   - No lazy evaluation
   - No deferred loading

4. Clarity
   - Rules must be explicit, not heuristic
   - Condition must be inspectable
   - Consequent must be binary (PASS/FAIL)

5. Traceability
   - Each rule must be traceable to authoritative source
   - Version must be locked
   - No override capability in arana
"""
