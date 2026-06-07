"""
Evidence Models

Evidence requests describe the facts required
to evaluate an approved claim.
"""

from dataclasses import dataclass


@dataclass
class EvidenceRequest:
    """Represents a request for observable evidence."""

    claim_id: str
    target_name: str
    evidence_type: str
    source: str
