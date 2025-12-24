"""APA7 Layout Rules - Hard-coded, explicit, deterministic.

Each rule defines exact APA 7th edition layout requirements.
NO scoring, NO probability, NO flexibility.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Rule:
    """Single deterministic rule."""
    rule_code: str
    description: str
    severity: str  # "critical", "error", "warning"
    blocking: bool


# APA7 Layout Rules - HARD-CODED
APA7_LAYOUT_RULES: List[Rule] = [
    Rule(
        rule_code="APA7-MARGIN-TOP",
        description="Top margin must be exactly 1 inch",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-MARGIN-BOTTOM",
        description="Bottom margin must be exactly 1 inch",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-MARGIN-LEFT",
        description="Left margin must be exactly 1 inch",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-MARGIN-RIGHT",
        description="Right margin must be exactly 1 inch",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-FONT-VALID",
        description="Font must be Times New Roman, Calibri, Arial, or Georgia",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-FONT-SIZE-TNR",
        description="Times New Roman must be 12pt",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-FONT-SIZE-CALIBRI",
        description="Calibri must be 11pt",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-FONT-SIZE-ARIAL",
        description="Arial must be 11pt",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-FONT-SIZE-GEORGIA",
        description="Georgia must be 11pt",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-LINE-SPACING",
        description="Line spacing must be double (2.0)",
        severity="critical",
        blocking=True
    ),
    Rule(
        rule_code="APA7-PAGE-NUMBERING",
        description="Page numbering must be present",
        severity="error",
        blocking=True
    )
]


# Valid font configurations (name -> required size)
VALID_FONTS = {
    "Times New Roman": 12.0,
    "Calibri": 11.0,
    "Arial": 11.0,
    "Georgia": 11.0
}

# Exact margin requirement (inches)
REQUIRED_MARGIN = 1.0

# Exact line spacing requirement
REQUIRED_LINE_SPACING = 2.0

# Tolerance for floating point comparison (0.01 inches = ~0.25mm)
MARGIN_TOLERANCE = 0.01
