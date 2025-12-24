"""Integration tests for APA7 Layout Stage.

Tests deterministic behavior:
- Incorrect margins -> FAIL + BLOCKING
- Correct APA7 -> PASS
- Minimal change -> FAIL deterministic
- Same input -> Same hash
"""

import pytest
from core.amanecer.apa7_layout.stage import apa7_layout_stage
from core.amanecer.apa7_layout.validator import compute_verdict_hash


def create_test_context(layout_config: dict) -> dict:
    """Create test pipeline context with layout configuration."""
    return {
        "document_id": "test-doc",
        "metadata": {
            "layout": layout_config
        }
    }


def test_incorrect_margins_fail_blocking():
    """Test: Document with incorrect margins -> FAIL + BLOCKING"""
    context = create_test_context({
        "margin_top": 0.75,  # Incorrect: should be 1.0
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False, "Should fail with incorrect margins"
    assert result["blocking"] is True, "Layout validation must be blocking"
    assert result["error"] is None, "Should not have technical errors"
    
    # Verify specific failure
    verdicts = result["output"]
    margin_top_verdict = next(
        v for v in verdicts if v["rule_code"] == "APA7-MARGIN-TOP"
    )
    assert margin_top_verdict["result"] == "FAIL"
    assert margin_top_verdict["blocking"] is True


def test_correct_apa7_pass():
    """Test: Document with correct APA7 layout -> PASS"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is True, "Should pass with correct APA7 layout"
    assert result["blocking"] is True
    assert result["error"] is None
    
    # Verify all rules passed
    verdicts = result["output"]
    for verdict in verdicts:
        assert verdict["result"] == "PASS", f"Rule {verdict['rule_code']} should pass"
    
    # Verify metadata
    metadata = result["metadata"]
    assert metadata["failed_rules"] == 0
    assert metadata["passed_rules"] == metadata["total_rules"]


def test_incorrect_font_size_fail():
    """Test: Minimal change (11pt instead of 12pt) -> FAIL deterministic"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 11.0,  # Incorrect: should be 12.0 for Times New Roman
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False, "Should fail with incorrect font size"
    assert result["error"] is None
    
    # Verify specific failure
    verdicts = result["output"]
    font_size_verdict = next(
        v for v in verdicts if v["rule_code"] == "APA7-FONT-SIZE-TNR"
    )
    assert font_size_verdict["result"] == "FAIL"
    
    # Verify evidence
    evidence = font_size_verdict["evidence"][0]
    assert evidence["expected_value"] == 12.0
    assert evidence["actual_value"] == 11.0
    assert evidence["match"] is False


def test_same_input_same_hash_determinism():
    """Test: Same input -> Same verdicts (hash identical) - proves determinism"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    # Run validation multiple times
    result1 = apa7_layout_stage(context)
    result2 = apa7_layout_stage(context)
    result3 = apa7_layout_stage(context)
    
    hash1 = result1["metadata"]["verdict_hash"]
    hash2 = result2["metadata"]["verdict_hash"]
    hash3 = result3["metadata"]["verdict_hash"]
    
    # Hashes must be identical
    assert hash1 == hash2 == hash3, "Same input must produce identical verdict hashes"
    
    # All results must be identical
    assert result1["ok"] == result2["ok"] == result3["ok"]
    assert len(result1["output"]) == len(result2["output"]) == len(result3["output"])


def test_invalid_font_fail():
    """Test: Invalid font name -> FAIL"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Comic Sans",  # Not in APA7 valid fonts
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False
    
    verdicts = result["output"]
    font_valid_verdict = next(
        v for v in verdicts if v["rule_code"] == "APA7-FONT-VALID"
    )
    assert font_valid_verdict["result"] == "FAIL"


def test_incorrect_line_spacing_fail():
    """Test: Incorrect line spacing -> FAIL"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 1.5,  # Incorrect: should be 2.0
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False
    
    verdicts = result["output"]
    line_spacing_verdict = next(
        v for v in verdicts if v["rule_code"] == "APA7-LINE-SPACING"
    )
    assert line_spacing_verdict["result"] == "FAIL"


def test_no_page_numbering_fail():
    """Test: Missing page numbering -> FAIL"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": False
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False
    
    verdicts = result["output"]
    page_numbering_verdict = next(
        v for v in verdicts if v["rule_code"] == "APA7-PAGE-NUMBERING"
    )
    assert page_numbering_verdict["result"] == "FAIL"


def test_calibri_11pt_pass():
    """Test: Calibri 11pt is valid APA7 -> PASS"""
    context = create_test_context({
        "margin_top": 1.0,
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Calibri",
        "font_size": 11.0,  # Correct for Calibri
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is True


def test_margin_tolerance_pass():
    """Test: Margins within tolerance (±0.01 inches) -> PASS"""
    context = create_test_context({
        "margin_top": 1.005,  # Within tolerance
        "margin_bottom": 0.995,  # Within tolerance
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is True, "Should pass with margins within tolerance"


def test_margin_outside_tolerance_fail():
    """Test: Margins outside tolerance (>0.01 inches) -> FAIL"""
    context = create_test_context({
        "margin_top": 1.02,  # Outside tolerance
        "margin_bottom": 1.0,
        "margin_left": 1.0,
        "margin_right": 1.0,
        "font_name": "Times New Roman",
        "font_size": 12.0,
        "line_spacing": 2.0,
        "page_numbering": True
    })
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False, "Should fail with margins outside tolerance"


def test_missing_layout_data_fail():
    """Test: Missing layout data -> FAIL gracefully"""
    context = create_test_context({})  # Empty layout
    
    result = apa7_layout_stage(context)
    
    assert result["ok"] is False
    assert result["error"] is None  # Should not be technical error
    
    # All verdicts should fail due to missing data
    verdicts = result["output"]
    assert all(v["result"] == "FAIL" for v in verdicts)
