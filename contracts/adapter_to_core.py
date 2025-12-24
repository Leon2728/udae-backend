"""Contract: adapters (ports) → core (business logic).

Defines protocol for how external adapters communicate with the core engine.
Adapters (HTTP, Word, Google Docs, etc.) must respect this contract.
Core never depends on adapters. Only the opposite.
"""

from typing import Protocol, Dict, Any
from dataclasses import dataclass


class AdapterInput(Protocol):
    """Input that adapters provide to the core.
    
    Adapters transform external formats (HTTP JSON, Word, PDF, etc.)
    into snapshots the core can process.
    """
    
    def get_snapshot(self) -> Any:
        """Return a Snapshot (from core.models).
        
        The adapter is responsible for:
        - Converting external document format to snapshot
        - Ensuring deterministic extraction
        - Providing document hash and timestamp
        """
        ...
    
    def get_rules(self) -> Any:
        """Return a Rule set (from core.models).
        
        The adapter loads normative rules from:
        - Configuration files
        - Policy files
        - Rule databases
        
        All rules must be immutable and versionable.
        """
        ...


class CoreOutput(Protocol):
    """Output that core produces for adapters.
    
    Adapters consume verdicts and reports from the core.
    """
    
    def get_verdicts(self) -> Any:
        """Return list of Verdicts (from core.models).
        
        Each verdict is immutable and fully traceable.
        """
        ...
    
    def get_report(self) -> str:
        """Return audit report as structured text.
        
        Adapters format this for users:
        - HTML reports
        - PDF exports
        - JSON APIs
        - Dashboards
        """
        ...


# ADAPTER PROTOCOL INVARIANTS
"""
1. Inversion of Dependency
   - Adapters depend on core
   - Core NEVER depends on adapters
   - No circular imports

2. Immutability Contract
   - Core delivers immutable snapshots and rules
   - Adapters NEVER mutate these
   - Adapters are stateless processors

3. Determinism Responsibility
   - Adapters must ensure extraction is deterministic
   - Same external input → same snapshot
   - Timestamps must be explicit and included

4. No Business Logic in Adapters
   - Adapters only transform formats
   - All decision logic belongs in core
   - Adapters are "dumb pipelines"

5. Bidirectional Coupling Forbidden
   - Adapters call core
   - Core never calls adapters back
   - No callbacks or hooks from core
"""
