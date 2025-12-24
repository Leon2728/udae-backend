"""Structural fact extraction from document context.

Extracts measurable, deterministic layout properties.
NO interpretation, NO heuristics, NO ML.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LayoutFacts:
    """Structural facts extracted from document."""
    margin_top: Optional[float] = None  # inches
    margin_bottom: Optional[float] = None  # inches
    margin_left: Optional[float] = None  # inches
    margin_right: Optional[float] = None  # inches
    font_name: Optional[str] = None
    font_size: Optional[float] = None  # points
    line_spacing: Optional[float] = None  # multiplier (1.0, 2.0, etc)
    page_numbering: Optional[bool] = None


def extract_layout_facts(context: Dict[str, Any]) -> LayoutFacts:
    """Extract structural layout facts from pipeline context.
    
    Args:
        context: PipelineContext as dict
        
    Returns:
        LayoutFacts with measurable properties
    """
    # Extract from document metadata if available
    metadata = context.get("metadata", {})
    layout = metadata.get("layout", {})
    
    # Direct extraction - NO interpretation
    return LayoutFacts(
        margin_top=layout.get("margin_top"),
        margin_bottom=layout.get("margin_bottom"),
        margin_left=layout.get("margin_left"),
        margin_right=layout.get("margin_right"),
        font_name=layout.get("font_name"),
        font_size=layout.get("font_size"),
        line_spacing=layout.get("line_spacing"),
        page_numbering=layout.get("page_numbering")
    )
