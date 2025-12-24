"""Araña — Normative decision engine.

Consumes Verdicts from Amanecer and produces final audit decisions.
"""

from .decision import Decision
from .stage import AranaStage

__all__ = ['Decision', 'AranaStage']
