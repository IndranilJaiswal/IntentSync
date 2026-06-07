"""
Evidence Records

Evidence records are collected facts from reality sources.

They do not make assurance decisions.
They only record what was observed.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class EvidenceRecord:
    """Represents collected evidence for an evidence request."""

    claim_id: str
    target_name: str
    evidence_type: str
    source: str
    observed: bool
    value: Any
    details: dict
