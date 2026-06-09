"""
governance_approval_models.py

Models governance approval decisions.
"""

from dataclasses import dataclass


@dataclass
class GovernanceApprovalDecision:
    claim_id: str
    decision: str
    approver: str
    rationale: str
