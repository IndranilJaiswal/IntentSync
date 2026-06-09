from governance_approval_models import GovernanceApprovalDecision


def approve_claims(
    claim_ids: list[str],
    approver: str = "PML",
) -> dict:
    decisions = []

    for claim_id in claim_ids:
        decisions.append(
            GovernanceApprovalDecision(
                claim_id=claim_id,
                decision="APPROVED",
                approver=approver,
                rationale="Approved for governed assurance scope.",
            )
        )

    return {
        "approved_claims": [
            {
                "claim_id": decision.claim_id,
                "decision": decision.decision,
                "approver": decision.approver,
                "rationale": decision.rationale,
            }
            for decision in decisions
        ]
    }
