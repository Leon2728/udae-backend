"""APA7 Layout Validator - Deterministic rule evaluation.

Applies hard-coded rules to extracted facts.
Produces Evidence and Verdicts.
NO scoring, NO heuristics, NO probability.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib
import json

from .extractor import LayoutFacts
from .rules import (
    APA7_LAYOUT_RULES,
    Rule,
    VALID_FONTS,
    REQUIRED_MARGIN,
    REQUIRED_LINE_SPACING,
    MARGIN_TOLERANCE
)


@dataclass
class Evidence:
    """Verifiable evidence for a rule evaluation."""
    rule_code: str
    fact_name: str
    expected_value: Any
    actual_value: Any
    match: bool


@dataclass
class Verdict:
    """Atomic verdict for a single rule."""
    rule_code: str
    description: str
    result: str  # "PASS" or "FAIL"
    severity: str
    blocking: bool
    evidence: List[Evidence]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "rule_code": self.rule_code,
            "description": self.description,
            "result": self.result,
            "severity": self.severity,
            "blocking": self.blocking,
            "evidence": [
                {
                    "rule_code": e.rule_code,
                    "fact_name": e.fact_name,
                    "expected_value": e.expected_value,
                    "actual_value": e.actual_value,
                    "match": e.match
                }
                for e in self.evidence
            ]
        }


def _check_margin(value: float, required: float, tolerance: float) -> bool:
    """Check if margin is within tolerance."""
    if value is None:
        return False
    return abs(value - required) <= tolerance


def _evaluate_margin_rule(
    rule: Rule,
    facts: LayoutFacts,
    margin_name: str
) -> Verdict:
    """Evaluate a single margin rule."""
    actual_value = getattr(facts, margin_name)
    match = _check_margin(actual_value, REQUIRED_MARGIN, MARGIN_TOLERANCE)
    
    evidence = Evidence(
        rule_code=rule.rule_code,
        fact_name=margin_name,
        expected_value=REQUIRED_MARGIN,
        actual_value=actual_value,
        match=match
    )
    
    return Verdict(
        rule_code=rule.rule_code,
        description=rule.description,
        result="PASS" if match else "FAIL",
        severity=rule.severity,
        blocking=rule.blocking,
        evidence=[evidence]
    )


def _evaluate_font_rules(rules: List[Rule], facts: LayoutFacts) -> List[Verdict]:
    """Evaluate all font-related rules."""
    verdicts = []
    
    # Check if font is valid
    font_valid_rule = next(r for r in rules if r.rule_code == "APA7-FONT-VALID")
    font_name = facts.font_name
    font_is_valid = font_name in VALID_FONTS
    
    evidence_font = Evidence(
        rule_code="APA7-FONT-VALID",
        fact_name="font_name",
        expected_value=list(VALID_FONTS.keys()),
        actual_value=font_name,
        match=font_is_valid
    )
    
    verdicts.append(Verdict(
        rule_code="APA7-FONT-VALID",
        description=font_valid_rule.description,
        result="PASS" if font_is_valid else "FAIL",
        severity=font_valid_rule.severity,
        blocking=font_valid_rule.blocking,
        evidence=[evidence_font]
    ))
    
    # If font is valid, check size
    if font_is_valid and font_name:
        required_size = VALID_FONTS[font_name]
        actual_size = facts.font_size
        size_match = actual_size == required_size if actual_size is not None else False
        
        # Find the appropriate size rule
        rule_code_map = {
            "Times New Roman": "APA7-FONT-SIZE-TNR",
            "Calibri": "APA7-FONT-SIZE-CALIBRI",
            "Arial": "APA7-FONT-SIZE-ARIAL",
            "Georgia": "APA7-FONT-SIZE-GEORGIA"
        }
        
        rule_code = rule_code_map.get(font_name)
        if rule_code:
            size_rule = next(r for r in rules if r.rule_code == rule_code)
            
            evidence_size = Evidence(
                rule_code=rule_code,
                fact_name="font_size",
                expected_value=required_size,
                actual_value=actual_size,
                match=size_match
            )
            
            verdicts.append(Verdict(
                rule_code=rule_code,
                description=size_rule.description,
                result="PASS" if size_match else "FAIL",
                severity=size_rule.severity,
                blocking=size_rule.blocking,
                evidence=[evidence_size]
            ))
    
    return verdicts


def _evaluate_line_spacing_rule(rule: Rule, facts: LayoutFacts) -> Verdict:
    """Evaluate line spacing rule."""
    actual_value = facts.line_spacing
    match = actual_value == REQUIRED_LINE_SPACING if actual_value is not None else False
    
    evidence = Evidence(
        rule_code=rule.rule_code,
        fact_name="line_spacing",
        expected_value=REQUIRED_LINE_SPACING,
        actual_value=actual_value,
        match=match
    )
    
    return Verdict(
        rule_code=rule.rule_code,
        description=rule.description,
        result="PASS" if match else "FAIL",
        severity=rule.severity,
        blocking=rule.blocking,
        evidence=[evidence]
    )


def _evaluate_page_numbering_rule(rule: Rule, facts: LayoutFacts) -> Verdict:
    """Evaluate page numbering rule."""
    actual_value = facts.page_numbering
    match = actual_value is True
    
    evidence = Evidence(
        rule_code=rule.rule_code,
        fact_name="page_numbering",
        expected_value=True,
        actual_value=actual_value,
        match=match
    )
    
    return Verdict(
        rule_code=rule.rule_code,
        description=rule.description,
        result="PASS" if match else "FAIL",
        severity=rule.severity,
        blocking=rule.blocking,
        evidence=[evidence]
    )


def validate_apa7_layout(facts: LayoutFacts) -> List[Verdict]:
    """Validate layout facts against APA7 rules.
    
    Pure deterministic evaluation:
    - Same input -> Same output
    - No probability
    - No scoring
    - Only PASS/FAIL
    
    Args:
        facts: Extracted layout facts
        
    Returns:
        List of atomic Verdicts
    """
    verdicts = []
    
    # Evaluate margin rules
    margin_rules = [
        ("APA7-MARGIN-TOP", "margin_top"),
        ("APA7-MARGIN-BOTTOM", "margin_bottom"),
        ("APA7-MARGIN-LEFT", "margin_left"),
        ("APA7-MARGIN-RIGHT", "margin_right")
    ]
    
    for rule_code, margin_name in margin_rules:
        rule = next(r for r in APA7_LAYOUT_RULES if r.rule_code == rule_code)
        verdict = _evaluate_margin_rule(rule, facts, margin_name)
        verdicts.append(verdict)
    
    # Evaluate font rules
    font_verdicts = _evaluate_font_rules(APA7_LAYOUT_RULES, facts)
    verdicts.extend(font_verdicts)
    
    # Evaluate line spacing
    line_spacing_rule = next(
        r for r in APA7_LAYOUT_RULES if r.rule_code == "APA7-LINE-SPACING"
    )
    verdicts.append(_evaluate_line_spacing_rule(line_spacing_rule, facts))
    
    # Evaluate page numbering
    page_numbering_rule = next(
        r for r in APA7_LAYOUT_RULES if r.rule_code == "APA7-PAGE-NUMBERING"
    )
    verdicts.append(_evaluate_page_numbering_rule(page_numbering_rule, facts))
    
    return verdicts


def compute_verdict_hash(verdicts: List[Verdict]) -> str:
    """Compute deterministic hash of verdicts for verification.
    
    Same verdicts -> Same hash (proves determinism)
    """
    verdict_data = [v.to_dict() for v in verdicts]
    verdict_json = json.dumps(verdict_data, sort_keys=True)
    return hashlib.sha256(verdict_json.encode()).hexdigest()
