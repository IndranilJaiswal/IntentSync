"""
Claim Review Models

Purpose:
Represent the review package shown to the Project Marketing Leader.

The PML should not approve opaque claim IDs.
They should approve explainable assurance intent.
"""

from dataclasses import dataclass


@dataclass
class ClaimReviewPackage:
    """Reviewable package for one suggested claim."""

    claim_id: str
    requirement: str
    category: str
    rationale: str
    business_impact: str
    relevant_policies: list[str]
    relevant_standards: list[str]
    coverage_status: str
    coverage_gap_reason: str | None = None
