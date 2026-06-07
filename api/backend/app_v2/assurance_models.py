"""
Assurance Models

Assurance results explain whether evidence justifies a claim.
"""

from dataclasses import dataclass


@dataclass
class AssuranceResult:
    """Represents the result of evaluating a claim."""

    claim_id: str
    target_name: str
    status: str
    confidence: float
    evidence_gaps: list[str]
    explanation: str
