"""
governance_approval_service.py

Governance approval and claim promotion service.

Important:
Governance approval does not mean executable assurance.

Lifecycle:
DISCOVERED
↓
GOVERNANCE_APPROVED
↓
CAPABILITY_CHECKED
↓
GOVERNED_EXECUTABLE / GOVERNED_PARTIALLY_EXECUTABLE / GOVERNED_CLAIM_DEFINED
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from capability_registry import get_claim_capability


load_dotenv()


def _get_database():
    mongodb_uri = os.getenv("MONGODB_URI")
    mongodb_database = os.getenv("MONGODB_DATABASE", "assurance_knowledge")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI not configured")

    client = MongoClient(mongodb_uri)

    return client[mongodb_database]


def _promotion_status_from_capability(capability: dict) -> dict:
    executability = capability.get("executability", "COVERAGE_GAP")

    if executability == "EXECUTABLE":
        return {
            "promotion_status": "GOVERNED_EXECUTABLE",
            "execution_status": "EXECUTABLE",
            "implementation_required": False,
        }

    if executability == "PARTIALLY_EXECUTABLE":
        return {
            "promotion_status": "GOVERNED_PARTIALLY_EXECUTABLE",
            "execution_status": "PARTIALLY_EXECUTABLE",
            "implementation_required": True,
        }

    if executability == "CLAIM_DEFINED":
        return {
            "promotion_status": "GOVERNED_CLAIM_DEFINED",
            "execution_status": "CLAIM_DEFINED",
            "implementation_required": True,
        }

    return {
        "promotion_status": "GOVERNED_CLAIM_DEFINED",
        "execution_status": "NOT_EXECUTABLE",
        "implementation_required": True,
    }


def approve_claims(
    claim_ids: list[str],
    approver: str = "PML",
) -> dict:
    """
    Approve existing supported claims for assurance execution.

    This is used for claims already in the governed assurance path.
    """

    decisions = []

    for claim_id in claim_ids:
        capability = get_claim_capability(claim_id)
        promotion = _promotion_status_from_capability(capability)

        decisions.append(
            {
                "claim_id": claim_id,
                "decision": "APPROVED",
                "approver": approver,
                "rationale": "Approved for governed assurance scope.",
                "executability": capability.get("executability"),
                "promotion_status": promotion["promotion_status"],
                "execution_status": promotion["execution_status"],
                "implementation_required": promotion["implementation_required"],
            }
        )

    return {
        "approved_claims": decisions,
    }


def approve_and_promote_claim(
    claim_id: str,
    approved_by: str = "PML",
    rationale: str = "",
) -> dict:
    """
    Approve a discovered claim and promote it into governed knowledge.

    This function checks the capability matrix before deciding whether the
    promoted claim is executable, partially executable, or only claim-defined.
    """

    db = _get_database()

    capability = get_claim_capability(claim_id)
    promotion = _promotion_status_from_capability(capability)

    record = {
        "claim_id": claim_id,
        "governance_status": "APPROVED",
        "approved_by": approved_by,
        "rationale": rationale,
        "approved_at": datetime.utcnow().isoformat(),
        "capability": capability,
        "promotion_status": promotion["promotion_status"],
        "execution_status": promotion["execution_status"],
        "implementation_required": promotion["implementation_required"],
    }

    db["governed_claims"].update_one(
        {"claim_id": claim_id},
        {"$set": record},
        upsert=True,
    )

    if promotion["implementation_required"]:
        db["implementation_backlog"].update_one(
            {"claim_id": claim_id},
            {
                "$set": {
                    "claim_id": claim_id,
                    "status": "OPEN",
                    "reason": (
                        "Claim has governance approval but does not yet "
                        "have full executable assurance capability."
                    ),
                    "missing_capabilities": capability.get(
                        "missing_capabilities",
                        [],
                    ),
                    "evidence_provider": capability.get(
                        "evidence_provider",
                        "none",
                    ),
                    "created_at": datetime.utcnow().isoformat(),
                }
            },
            upsert=True,
        )

    return {
        "claim_id": claim_id,
        "governance_status": "APPROVED",
        "promotion_status": promotion["promotion_status"],
        "execution_status": promotion["execution_status"],
        "implementation_required": promotion["implementation_required"],
        "capability": capability,
    }
