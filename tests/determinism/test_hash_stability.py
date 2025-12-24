"""Tests for hash stability and determinism of domain models.

Ensures that:
1. Identical objects always produce identical hashes
2. Minor changes in content produce different hashes
3. Hash function is deterministic and reproducible
"""

import sys
from pathlib import Path

# Add core to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'core'))

from models import (
    hash_json, hash_string, hash_bytes,
    Rule, Snapshot, Evidence, Verdict
)


def test_hash_function_determinism():
    """Test that hash_json produces identical hashes for identical inputs."""
    data = {'name': 'test', 'version': '1.0', 'order': ['z', 'a', 'b']}
    hash1 = hash_json(data)
    hash2 = hash_json(data)
    assert hash1 == hash2, "Hash should be deterministic"
    assert len(hash1) == 64, "SHA-256 hex should be 64 characters"


def test_hash_sensitivity_to_changes():
    """Test that hash changes when data changes."""
    data1 = {'field': 'value'}
    data2 = {'field': 'VALUE'}  # Different case
    hash1 = hash_json(data1)
    hash2 = hash_json(data2)
    assert hash1 != hash2, "Hash should change with content"


def test_rule_identity_stability():
    """Test that identical Rule objects produce identical hashes."""
    rule1 = Rule(
        code='TEST_RULE_001',
        version='1.0.0',
        description='Test rule',
        logic_type='binary',
        consequent='PASS',
        evidence_field='title',
        severity='error'
    )
    rule2 = Rule(
        code='TEST_RULE_001',
        version='1.0.0',
        description='Test rule',
        logic_type='binary',
        consequent='PASS',
        evidence_field='title',
        severity='error'
    )
    assert rule1.rule_id == rule2.rule_id, "Identical rules should have identical IDs"


def test_snapshot_identity_stability():
    """Test that identical Snapshot objects produce identical hashes."""
    snapshot1 = Snapshot(
        document_name='test.pdf',
        document_hash='abc123',
        extracted_fields={'title': 'Test Document'},
        extraction_timestamp='2025-01-01T00:00:00Z',
        extraction_version='1.0.0'
    )
    snapshot2 = Snapshot(
        document_name='test.pdf',
        document_hash='abc123',
        extracted_fields={'title': 'Test Document'},
        extraction_timestamp='2025-01-01T00:00:00Z',
        extraction_version='1.0.0'
    )
    assert snapshot1.snapshot_id == snapshot2.snapshot_id, "Identical snapshots should have identical IDs"


def test_evidence_identity_stability():
    """Test that identical Evidence objects produce identical hashes."""
    evidence1 = Evidence(
        field_path='title',
        extracted_value='My Title',
        value_type='string',
        confidence=0.95
    )
    evidence2 = Evidence(
        field_path='title',
        extracted_value='My Title',
        value_type='string',
        confidence=0.95
    )
    assert evidence1.evidence_id == evidence2.evidence_id, "Identical evidence should have identical IDs"


def test_verdict_identity_stability():
    """Test that identical Verdict objects produce identical hashes."""
    verdict1 = Verdict(
        rule_id='rule_123',
        snapshot_id='snap_123',
        result='PASS',
        evidence_ids=['ev1', 'ev2'],
        reasoning='Test passed',
        severity='error'
    )
    verdict2 = Verdict(
        rule_id='rule_123',
        snapshot_id='snap_123',
        result='PASS',
        evidence_ids=['ev2', 'ev1'],  # Different order
        reasoning='Test passed',
        severity='error'
    )
    # Verdicts should have identical IDs even if evidence order differs
    # (due to sorted() in __post_init__)
    assert verdict1.verdict_id == verdict2.verdict_id, "Verdicts with same evidence (any order) should have identical IDs"


if __name__ == '__main__':
    print("Running hash stability tests...")
    test_hash_function_determinism()
    print("✓ Hash function determinism")
    test_hash_sensitivity_to_changes()
    print("✓ Hash sensitivity to changes")
    test_rule_identity_stability()
    print("✓ Rule identity stability")
    test_snapshot_identity_stability()
    print("✓ Snapshot identity stability")
    test_evidence_identity_stability()
    print("✓ Evidence identity stability")
    test_verdict_identity_stability()
    print("✓ Verdict identity stability")
    print("\nAll tests passed! ✅")
