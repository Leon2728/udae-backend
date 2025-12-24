"""Integration tests for Araña decision stage."""

import pytest
from core.models.verdict import Verdict
from core.kernel.stages import StageResult
from core.kernel.context import PipelineContext
from core.arana.stage import AranaStage
from core.arana.decision import Decision


def test_fail_due_to_blocking_failure():
    """Test that blocking failure causes FAIL decision."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id="rule_001",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=["ev_001"],
            reasoning="Missing required field",
            severity="error"
        )
    ]
    
    context = PipelineContext(meta={"verdicts": verdicts})
    result = stage.execute(context)
    
    assert isinstance(result, StageResult)
    assert result.blocking is True
    assert result.ok is False
    assert isinstance(result.output, Decision)
    assert result.output.status == "FAIL"
    assert len(result.output.blocking_failures) == 1
    assert result.output.blocking_failures[0].verdict_id == verdicts[0].verdict_id


def test_pass_without_blocking_failures():
    """Test that PASS occurs when no blocking failures exist."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id="rule_001",
            snapshot_id="snap_001",
            result="PASS",
            evidence_ids=["ev_001"],
            reasoning="Field present",
            severity="error"
        ),
        Verdict(
            rule_id="rule_002",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=["ev_002"],
            reasoning="Recommendation not followed",
            severity="warning"
        )
    ]
    
    context = PipelineContext(meta={"verdicts": verdicts})
    result = stage.execute(context)
    
    assert result.ok is True
    assert result.output.status == "PASS"
    assert len(result.output.blocking_failures) == 0
    assert len(result.output.non_blocking_failures) == 1


def test_mixed_verdicts_with_blocking_fail():
    """Test mixed verdicts where blocking failure determines outcome."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id="rule_001",
            snapshot_id="snap_001",
            result="PASS",
            evidence_ids=["ev_001"],
            reasoning="Valid",
            severity="error"
        ),
        Verdict(
            rule_id="rule_002",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=["ev_002"],
            reasoning="Critical failure",
            severity="error"
        ),
        Verdict(
            rule_id="rule_003",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=["ev_003"],
            reasoning="Warning only",
            severity="warning"
        )
    ]
    
    context = PipelineContext(meta={"verdicts": verdicts})
    result = stage.execute(context)
    
    assert result.ok is False
    assert result.output.status == "FAIL"
    assert len(result.output.blocking_failures) == 1
    assert len(result.output.non_blocking_failures) == 1
    assert len(result.output.all_verdicts) == 3


def test_decision_hash_determinism():
    """Test that decision hash is stable and deterministic."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id="rule_001",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=["ev_001"],
            reasoning="Error",
            severity="error"
        )
    ]
    
    context1 = PipelineContext(meta={"verdicts": verdicts})
    context2 = PipelineContext(meta={"verdicts": verdicts})
    
    result1 = stage.execute(context1)
    result2 = stage.execute(context2)
    
    assert result1.output.decision_hash == result2.output.decision_hash
    assert result1.output.decision_hash != ""


def test_different_order_same_decision():
    """Test that verdict order doesn't affect decision hash."""
    stage = AranaStage()
    
    v1 = Verdict(
        rule_id="rule_001",
        snapshot_id="snap_001",
        result="FAIL",
        evidence_ids=["ev_001"],
        reasoning="Error A",
        severity="error"
    )
    
    v2 = Verdict(
        rule_id="rule_002",
        snapshot_id="snap_001",
        result="FAIL",
        evidence_ids=["ev_002"],
        reasoning="Error B",
        severity="error"
    )
    
    context1 = PipelineContext(meta={"verdicts": [v1, v2]})
    context2 = PipelineContext(meta={"verdicts": [v2, v1]})
    
    result1 = stage.execute(context1)
    result2 = stage.execute(context2)
    
    assert result1.output.decision_hash == result2.output.decision_hash
    assert result1.output.status == result2.output.status


def test_all_pass_verdicts():
    """Test decision with all passing verdicts."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id=f"rule_{i:03d}",
            snapshot_id="snap_001",
            result="PASS",
            evidence_ids=[f"ev_{i:03d}"],
            reasoning=f"Valid {i}",
            severity="error"
        )
        for i in range(5)
    ]
    
    context = PipelineContext(meta={"verdicts": verdicts})
    result = stage.execute(context)
    
    assert result.ok is True
    assert result.output.status == "PASS"
    assert len(result.output.blocking_failures) == 0
    assert len(result.output.all_verdicts) == 5


def test_multiple_blocking_failures():
    """Test decision with multiple blocking failures."""
    stage = AranaStage()
    
    verdicts = [
        Verdict(
            rule_id=f"rule_{i:03d}",
            snapshot_id="snap_001",
            result="FAIL",
            evidence_ids=[f"ev_{i:03d}"],
            reasoning=f"Critical error {i}",
            severity="error"
        )
        for i in range(3)
    ]
    
    context = PipelineContext(meta={"verdicts": verdicts})
    result = stage.execute(context)
    
    assert result.ok is False
    assert result.output.status == "FAIL"
    assert len(result.output.blocking_failures) == 3


def test_empty_verdicts_list():
    """Test decision with empty verdict list."""
    stage = AranaStage()
    
    context = PipelineContext(meta={"verdicts": []})
    result = stage.execute(context)
    
    assert result.ok is True
    assert result.output.status == "PASS"
    assert len(result.output.blocking_failures) == 0
    assert len(result.output.all_verdicts) == 0
    assert result.output.decision_hash != ""


def test_missing_verdicts_in_context():
    """Test stage handles missing verdicts key gracefully."""
    stage = AranaStage()
    
    # Context without verdicts key
    context = PipelineContext(meta={})
    result = stage.execute(context)
    
    assert result.ok is True
    assert result.output.status == "PASS"
    assert len(result.output.all_verdicts) == 0
    assert result.output.decision_hash != ""
