"""
Requirement Assurance Models

Requirement assurance rolls up multiple claim assurance results
into a business-level requirement status.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class RequirementAssuranceResult:
    """Represents assurance status for a requirement."""

    requirement_id: str
    title: str
    status: str
    verified_claims: int
    insufficient_claims: int
    failed_claims: int
    claim_results: list[Any]
    explanation: str
