"""
claim_review_package_builder.py

Builds reviewable PML claim packages from AI-discovered claims.

Purpose:
Convert Gemini claim suggestions into explainable governance packages
before they can enter assurance execution.
"""

from capability_metrics import calculate_assurance_readiness
from capability_registry import get_claim_capability
from claim_library import load_claim_library
from claim_review_models import ClaimReviewPackage
from knowledge_retriever import KnowledgeRetriever
from pml_governance_router import route_claim_review_package


def _claim_exists_in_library(claim_id: str) -> bool:
    """Check whether a claim already exists in the governed claim library."""

    claims = load_claim_library()

    return any(
        claim.claim_id == claim_id
        for claim in claims
    )


def _match_policy_names(
    claim_id: str,
    policies: list[dict],
) -> list[str]:
    """Find relevant policies for the claim."""

    matched = []

    claim_tokens = claim_id.replace("_", " ").lower().split()

    for policy in policies:
        policy_name = (
            policy.get("policy_name")
            or policy.get("name")
            or policy.get("title")
        )

        policy_text = " ".join(
            str(value)
            for value in policy.values()
            if value is not None
        ).lower()

        if any(token in policy_text for token in claim_tokens):
            if policy_name:
                matched.append(policy_name)

    return matched or ["PML Review Required"]


def _match_standard_names(
    claim_id: str,
    standards: list[dict],
) -> list[str]:
    """Find relevant standards for the claim."""

    matched = []

    claim_tokens = claim_id.replace("_", " ").lower().split()

    for standard in standards:
        standard_name = (
            standard.get("standard_name")
            or standard.get("name")
            or standard.get("title")
        )

        standard_text = " ".join(
            str(value)
            for value in standard.values()
            if value is not None
        ).lower()

        if any(token in standard_text for token in claim_tokens):
            if standard_name:
                matched.append(standard_name)

    return matched


def _infer_category(claim_id: str) -> str:
    """Infer a review category from the claim name."""

    claim_id = claim_id.upper()

    if (
        "LOG" in claim_id
        or "MONITOR" in claim_id
        or "OBSERV" in claim_id
        or "TRACE" in claim_id
    ):
        return "Observability"

    if (
        "RECOVER" in claim_id
        or "REDUNDANT" in claim_id
        or "FAILOVER" in claim_id
        or "RESILIENT" in claim_id
    ):
        return "Resilience"

    if (
        "SECURE" in claim_id
        or "AUTH" in claim_id
        or "ENCRYPT" in claim_id
        or "ACCESS" in claim_id
    ):
        return "Security"

    if (
        "HEALTH" in claim_id
        or "AVAILABLE" in claim_id
        or "EXISTS" in claim_id
        or "SCALABLE" in claim_id
    ):
        return "Availability"

    return "Assurance"


def build_claim_review_package(
    requirement_text: str,
    suggestion,
) -> dict:
    """
    Build one governance-ready claim review package.
    """

    retriever = KnowledgeRetriever()

    policies = retriever.get_policies()
    standards = retriever.get_standards()

    claim_id = suggestion.claim_id

    is_supported = _claim_exists_in_library(claim_id)

    capability = get_claim_capability(claim_id)

    coverage_status = capability["executability"]

    coverage_gap_reason = None

    if coverage_status == "COVERAGE_GAP":
        coverage_gap_reason = (
            "No executable claim definition exists in the governed "
            "claim library or assurance capability matrix."
        )

    elif coverage_status == "PARTIALLY_EXECUTABLE":
        coverage_gap_reason = (
            "Claim is defined but some required evidence capabilities "
            "are currently unavailable."
        )

    elif coverage_status == "CLAIM_DEFINED":
        coverage_gap_reason = (
            "Claim exists but executable assurance logic has not yet "
            "been implemented."
        )

    package = ClaimReviewPackage(
        claim_id=claim_id,
        requirement=requirement_text,
        category=_infer_category(claim_id),
        rationale=getattr(
            suggestion,
            "rationale",
            getattr(
                suggestion,
                "objective_description",
                "AI-discovered claim requiring review.",
            ),
        ),
        business_impact=getattr(
            suggestion,
            "business_impact",
            (
                "If this claim is not assured, the requirement may not "
                "be fully supported by observable evidence."
            ),
        ),
        relevant_policies=_match_policy_names(
            claim_id,
            policies,
        ),
        relevant_standards=_match_standard_names(
            claim_id,
            standards,
        ),
        coverage_status=coverage_status,
        coverage_gap_reason=coverage_gap_reason,
    )

    governance_route = route_claim_review_package(package)

    return {
        "claim_id": package.claim_id,
        "requirement": package.requirement,
        "category": package.category,
        "rationale": package.rationale,
        "business_impact": package.business_impact,
        "relevant_policies": package.relevant_policies,
        "relevant_standards": package.relevant_standards,
        "coverage_status": package.coverage_status,
        "coverage_gap_reason": package.coverage_gap_reason,
        "governance_route": governance_route,

        # Capability Matrix Fields
        "verifiability": capability["verifiability"],
        "executability": capability["executability"],
        "entity_type": capability["entity_type"],
        "assurance_logic": capability["assurance_logic"],
        "evidence_provider": capability["evidence_provider"],
        "required_evidence": capability["evidence"],
        "mcp_capabilities": capability["mcp_capabilities"],
        "missing_capabilities": capability["missing_capabilities"],

        # Legacy compatibility
        "claim_supported": is_supported,
    }


def build_claim_review_packages(
    requirement_text: str,
    suggestions: list,
) -> dict:
    """
    Build governance-ready claim review packages for all suggestions.
    """

    packages = [
        build_claim_review_package(
            requirement_text=requirement_text,
            suggestion=suggestion,
        )
        for suggestion in suggestions
    ]

    metrics = calculate_assurance_readiness(packages)

    return {
        "requirement_text": requirement_text,
        "review_packages": packages,
        "summary": metrics,
    }
