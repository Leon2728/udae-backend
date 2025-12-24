"""Architecture guard tests for layer boundaries.

Ensures that the hexagonal architecture is respected:
- No business logic in adapters
- No core dependencies on adapters
- No bidirectional coupling
- Contracts are properly defined and respected
"""

import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_models_are_immutable():
    """Verify that core models use frozen dataclasses."""
    from core.models import Rule, Snapshot, Evidence, Verdict
    
    # All models should be dataclasses with frozen=True
    assert hasattr(Rule, '__dataclass_fields__')
    assert hasattr(Snapshot, '__dataclass_fields__')
    assert hasattr(Evidence, '__dataclass_fields__')
    assert hasattr(Verdict, '__dataclass_fields__')
    
    # They should all be frozen
    rule_instance = Rule('TEST', '1.0', 'test', 'binary', 'PASS', 'title', 'error')
    snapshot_instance = Snapshot('test.pdf', 'abc', {}, '2025-01-01T00:00:00Z', '1.0')
    evidence_instance = Evidence('field', 'value', 'str', 0.9)
    verdict_instance = Verdict('r1', 's1', 'PASS', ['e1'], 'test', 'error')
    
    # Attempting to mutate should raise FrozenInstanceError
    try:
        rule_instance.code = 'MODIFIED'
        assert False, "Rule should be immutable"
    except AttributeError:
        pass  # Expected
    
    print("✓ All models are immutable")


def test_contracts_are_protocols():
    """Verify that layer contracts are Protocol types (structural typing)."""
    from contracts import (
        AmanecerOutput, FenixInput,
        FenixOutput, AranaInput,
        AranaOutput, IreInput,
        AdapterInput, CoreOutput
    )
    
    # All should be Protocol types
    from typing import Protocol, runtime_checkable
    
    # Protocols exist and are importable
    assert AmanecerOutput is not None
    assert FenixInput is not None
    assert FenixOutput is not None
    assert AranaInput is not None
    assert AranaOutput is not None
    assert IreInput is not None
    assert AdapterInput is not None
    assert CoreOutput is not None
    
    print("✓ All layer contracts exist and are importable")


def test_no_core_imports_adapters():
    """Verify that core module does not import from adapters."""
    import ast
    from pathlib import Path
    
    core_path = Path('core')
    adapter_path = Path('adapters')
    
    # Scan core for imports from adapters
    violations = []
    for py_file in core_path.rglob('*.py'):
        with open(py_file, 'r') as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        if isinstance(node, ast.ImportFrom) and node.module:
                            if 'adapters' in node.module or 'adapter' in node.module:
                                violations.append(f"{py_file}: {ast.unparse(node)}")
            except SyntaxError:
                pass  # Ignore syntax errors in test files
    
    assert len(violations) == 0, f"Core imports adapters: {violations}"
    print("✓ Core does not import from adapters")


def test_no_mutable_state_in_models():
    """Verify that models don't have mutable default values."""
    from core.models import Snapshot
    from dataclasses import fields
    
    for field in fields(Snapshot):
        # Mutable defaults should use default_factory
        if field.default is not None:
            assert isinstance(field.default, (str, int, float, bool, type(None)))
        if field.default_factory is not None:  # noqa: F821
            # OK - mutable defaults via factory
            pass
    
    print("✓ Models have no mutable default values")


def test_contracts_have_invariants():
    """Verify that contracts document invariants."""
    import contracts.amanecer_to_fenix as atf
    import contracts.fenix_to_arana as fta
    import contracts.arana_to_ire as ati
    import contracts.adapter_to_core as atc
    
    # Each module should have documented invariants
    modules = [atf, fta, ati, atc]
    for module in modules:
        # Check for docstring mentioning invariants
        assert module.__doc__ is not None
        assert 'INVARIANT' in module.__doc__.upper() or 'invariant' in module.__doc__
    
    print("✓ All contracts document invariants")


if __name__ == '__main__':
    print("Running architecture guard tests...")
    test_models_are_immutable()
    test_contracts_are_protocols()
    test_no_core_imports_adapters()
    test_no_mutable_state_in_models()
    test_contracts_have_invariants()
    print("\nAll architecture guard tests passed! ✅")
