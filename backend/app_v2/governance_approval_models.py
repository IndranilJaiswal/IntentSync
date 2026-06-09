from dataclasses import dataclass


@dataclass
class GovernanceApprovalDecision:
    claim_id: str
    decision: str
    approver: str
    rationale: str
