"""Integration tests for deterministic pipeline.

These tests verify pipeline orchestration without business logic.
All stages are pure dummy functions with no side effects.
"""

import pytest

from core.kernel import (
    BlockingStageError,
    Pipeline,
    PipelineContext,
    StageDefinition,
    StageName,
    StageResult,
)


# Dummy stage functions - pure, deterministic, no side effects
def stage_a_success(context: PipelineContext) -> StageResult:
    """Dummy stage A that always succeeds."""
    return StageResult(
        ok=True,
        blocking=False,
        output={"stage": "a", "processed": True}
    )


def stage_b_success(context: PipelineContext) -> StageResult:
    """Dummy stage B that always succeeds."""
    return StageResult(
        ok=True,
        blocking=True,
        output={"stage": "b", "processed": True}
    )


def stage_c_success(context: PipelineContext) -> StageResult:
    """Dummy stage C that always succeeds."""
    return StageResult(
        ok=True,
        blocking=False,
        output={"stage": "c", "processed": True}
    )


def stage_blocking_failure(context: PipelineContext) -> StageResult:
    """Dummy stage that fails with blocking=True."""
    return StageResult(
        ok=False,
        blocking=True,
        error=Exception("Intentional blocking failure")
    )


def stage_nonblocking_failure(context: PipelineContext) -> StageResult:
    """Dummy stage that fails with blocking=False."""
    return StageResult(
        ok=False,
        blocking=False,
        error=Exception("Intentional non-blocking failure")
    )


@pytest.fixture
def dummy_context():
    """Create a deterministic dummy context."""
    return PipelineContext(
        document_ref="doc-12345",
        normative_context="test-norm-v1",
        facts_snapshot=None,
        run_id="test-run-001",
        meta={"test": True, "env": "integration"}
    )


def test_pipeline_executes_stages_in_order(dummy_context):
    """Test that pipeline executes stages in the defined order."""
    # Arrange
    stages = [
        StageDefinition(
            name=StageName.STAGE_A,
            blocking=False,
            fn=stage_a_success
        ),
        StageDefinition(
            name=StageName.STAGE_B,
            blocking=False,
            fn=stage_b_success
        ),
        StageDefinition(
            name=StageName.STAGE_C,
            blocking=False,
            fn=stage_c_success
        ),
    ]
    pipeline = Pipeline(stages=stages)
    
    # Act
    results = pipeline.execute(dummy_context)
    
    # Assert
    assert len(results) == 3
    assert results[0].output["stage"] == "a"
    assert results[1].output["stage"] == "b"
    assert results[2].output["stage"] == "c"
    assert all(r.ok for r in results)


def test_blocking_failure_stops_execution(dummy_context):
    """Test that blocking failure stops pipeline execution immediately."""
    # Arrange
    stages = [
        StageDefinition(
            name=StageName.STAGE_A,
            blocking=False,
            fn=stage_a_success
        ),
        StageDefinition(
            name=StageName.STAGE_B,
            blocking=True,
            fn=stage_blocking_failure
        ),
        StageDefinition(
            name=StageName.STAGE_C,
            blocking=False,
            fn=stage_c_success
        ),
    ]
    pipeline = Pipeline(stages=stages)
    
    # Act & Assert
    with pytest.raises(BlockingStageError) as exc_info:
        pipeline.execute(dummy_context)
    
    # Verify error details
    assert exc_info.value.stage_name == StageName.STAGE_B.value
    assert "blocking=True" in str(exc_info.value)
    
    # Verify only first two stages executed
    results = pipeline.results
    assert len(results) == 2
    assert results[0].ok is True  # Stage A succeeded
    assert results[1].ok is False  # Stage B failed


def test_pipeline_context_is_immutable(dummy_context):
    """Test that PipelineContext cannot be modified."""
    # Arrange & Act & Assert
    with pytest.raises(Exception):  # dataclass frozen raises FrozenInstanceError
        dummy_context.document_ref = "modified-doc"
    
    with pytest.raises(Exception):
        dummy_context.run_id = "modified-run"


def test_result_is_deterministic(dummy_context):
    """Test that pipeline produces deterministic results."""
    # Arrange
    stages = [
        StageDefinition(
            name=StageName.STAGE_A,
            blocking=False,
            fn=stage_a_success
        ),
        StageDefinition(
            name=StageName.STAGE_B,
            blocking=False,
            fn=stage_b_success
        ),
    ]
    pipeline = Pipeline(stages=stages)
    
    # Act - Execute multiple times
    results_1 = pipeline.execute(dummy_context)
    results_2 = pipeline.execute(dummy_context)
    results_3 = pipeline.execute(dummy_context)
    
    # Assert - All executions produce identical results
    assert len(results_1) == len(results_2) == len(results_3) == 2
    
    for r1, r2, r3 in zip(results_1, results_2, results_3):
        assert r1.ok == r2.ok == r3.ok
        assert r1.blocking == r2.blocking == r3.blocking
        assert r1.output == r2.output == r3.output


def test_nonblocking_failure_continues_execution(dummy_context):
    """Test that non-blocking failures allow pipeline to continue."""
    # Arrange
    stages = [
        StageDefinition(
            name=StageName.STAGE_A,
            blocking=False,
            fn=stage_a_success
        ),
        StageDefinition(
            name=StageName.STAGE_B,
            blocking=False,
            fn=stage_nonblocking_failure
        ),
        StageDefinition(
            name=StageName.STAGE_C,
            blocking=False,
            fn=stage_c_success
        ),
    ]
    pipeline = Pipeline(stages=stages)
    
    # Act
    results = pipeline.execute(dummy_context)
    
    # Assert - All stages executed despite Stage B failure
    assert len(results) == 3
    assert results[0].ok is True   # Stage A succeeded
    assert results[1].ok is False  # Stage B failed (non-blocking)
    assert results[2].ok is True   # Stage C executed and succeeded
