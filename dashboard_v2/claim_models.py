"""
Claim Models

A requirement is human intent.
A claim is an approved, observable statement.
Only claims are evaluated by the Assurance Engine.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Claim:
    """Represents a reusable claim template."""

    claim_id: str
    name: str
    category: str
    description: str
    evidence_required: list[str]
    entity_type: str
    verifiability: str


@dataclass
class ApprovedClaim:
    """Represents a claim selected by a human for assurance."""

    claim: Claim
    target_name: str
    thresholds: dict[str, Any]
