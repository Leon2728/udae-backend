"""APA7 Layout Stage - Pipeline integration.

StageDefinition that validates APA7 layout compliance.
Returns StageResult with atomic Verdicts.
"""

from typing import Dict, Any, List

from .extractor import extract_layout_facts
from .validator import validate_apa7_layout, compute_verdict_hash


def apa7_layout_stage(context: Dict[str, Any]) -> Dict[str, Any]:
    """Validate document layout against APA7 requirements.
    
    This is a StageDefinition compatible function.
    
    Args:
        context: PipelineContext as dict
        
    Returns:
        StageResult as dict:
        {
            "ok": bool,  # True only if ALL rules pass
            "blocking": bool,  # Always True for layout validation
            "output": List[Verdict],  # Atomic verdicts
            "error": Optional[str],  # None unless technical error
            "metadata": dict  # Hash for determinism verification
        }
    """
    try:
        # Extract structural facts
        facts = extract_layout_facts(context)
        
        # Validate against APA7 rules
        verdicts = validate_apa7_layout(facts)
        
        # Check if all rules passed
        all_passed = all(v.result == "PASS" for v in verdicts)
        
        # Compute hash for determinism verification
        verdict_hash = compute_verdict_hash(verdicts)
        
        # Convert verdicts to dicts for output
        verdict_dicts = [v.to_dict() for v in verdicts]
        
        return {
            "ok": all_passed,
            "blocking": True,  # Layout validation is always blocking
            "output": verdict_dicts,
            "error": None,
            "metadata": {
                "verdict_hash": verdict_hash,
                "total_rules": len(verdicts),
                "passed_rules": sum(1 for v in verdicts if v.result == "PASS"),
                "failed_rules": sum(1 for v in verdicts if v.result == "FAIL")
            }
        }
        
    except Exception as e:
        # Technical error (not validation failure)
        return {
            "ok": False,
            "blocking": True,
            "output": [],
            "error": f"Technical error in APA7 layout validation: {str(e)}",
            "metadata": {}
        }
