"""
assurance_service.py

Shared IntentSync assurance execution service.

Used by:
- Streamlit dashboard
- FastAPI service for Agent Builder
"""

from claim_assurance_engine import ClaimAssuranceEngine
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_mcp_evidence_provider import DynatraceMCPEvidenceProvider
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


def get_claim_by_id(claims, claim_id):
    return next(claim for claim in claims if claim.claim_id == claim_id)


def get_requirement_by_id(requirements, requirement_id):
    return next(
        requirement
        for requirement in requirements
        if requirement.requirement_id == requirement_id
    )


def run_assurance_for_requirement(
    requirement_id: str,
    approved_governed_claim_ids: list[str] | None = None,
    target_name: str = "easyTravel-Business",
) -> dict:
    """
    Run assurance for one requirement.

    If approved_governed_claim_ids is not provided, the service uses the
    requirement's configured claim IDs as the approved assurance scope.
    """

    claims = load_claim_library()
    requirements = load_requirements()

    requirement = get_requirement_by_id(
        requirements,
        requirement_id,
    )

    if approved_governed_claim_ids is None:
        approved_governed_claim_ids = requirement.claim_ids

    evidence_provider = DynatraceMCPEvidenceProvider()

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    claim_results = []
    evidence_by_claim = {}

    for governed_claim_id in approved_governed_claim_ids:
        claim = get_claim_by_id(claims, governed_claim_id)

        approved_claim = ApprovedClaim(
            claim=claim,
            target_name=target_name,
            thresholds={},
        )

        evidence_records = evidence_provider.collect_evidence(
            approved_claim
        )

        claim_result = claim_assurance_engine.evaluate(
            approved_claim,
            evidence_records,
        )

        claim_results.append(claim_result)
        evidence_by_claim[governed_claim_id] = evidence_records

    requirement_result = requirement_assurance_engine.evaluate(
        requirement,
        claim_results,
    )

    return {
        "requirement": requirement,
        "requirement_result": requirement_result,
        "evidence_by_claim": evidence_by_claim,
    }


def serialize_assurance_result(result: dict) -> dict:
    """
    Convert assurance result objects into JSON-safe API response.
    """

    requirement = result["requirement"]
    requirement_result = result["requirement_result"]
    evidence_by_claim = result["evidence_by_claim"]

    serialized_claims = []

    for claim_result in requirement_result.claim_results:
        evidence_records = evidence_by_claim.get(
            claim_result.claim_id,
            [],
        )

        serialized_claims.append(
            {
                "claim_id": claim_result.claim_id,
                "target_name": claim_result.target_name,
                "status": claim_result.status,
                "confidence": claim_result.confidence,
                "explanation": claim_result.explanation,
                "evidence_gaps": claim_result.evidence_gaps,
                "evidence_records": [
                    {
                        "claim_id": evidence.claim_id,
                        "target_name": evidence.target_name,
                        "evidence_type": evidence.evidence_type,
                        "source": evidence.source,
                        "observed": evidence.observed,
                        "value": evidence.value,
                        "details": evidence.details,
                    }
                    for evidence in evidence_records
                ],
            }
        )

    return {
        "requirement": {
            "requirement_id": requirement.requirement_id,
            "title": requirement.title,
            "description": requirement.description,
        },
        "assurance": {
            "status": requirement_result.status,
            "explanation": requirement_result.explanation,
            "verified_claims": requirement_result.verified_claims,
            "insufficient_claims": requirement_result.insufficient_claims,
            "failed_claims": requirement_result.failed_claims,
            "claim_results": serialized_claims,
        },
    }
