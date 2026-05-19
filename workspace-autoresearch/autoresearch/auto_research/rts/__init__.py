"""Research Task Specification protocol helpers."""

from __future__ import annotations

from auto_research.rts.io import load_rts, rts_from_dict, rts_to_dict, save_rts
from auto_research.rts.schema import ResearchTaskSpecification
from auto_research.rts.validation import RTSValidator

__all__ = [
    "ResearchTaskSpecification",
    "RTSValidator",
    "load_rts",
    "rts_from_dict",
    "rts_to_dict",
    "save_rts",
]
