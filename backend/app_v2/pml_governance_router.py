"""
pml_governance_router.py

Routes claim review packages into the correct governance lane.

This prevents unsupported AI-discovered claims from flowing directly
into assurance execution.
"""


def route_claim_review_package(package) -> str:
    """
    Route a claim review package based on its coverage / executability status.
    """

    coverage_status = getattr(package, "coverage_status", None)

    if coverage_status == "EXECUTABLE":
        return "PML_APPROVAL_REQUIRED"

    if coverage_status == "PARTIALLY_EXECUTABLE":
        return "PML_APPROVAL_REQUIRED_WITH_CAPABILITY_GAPS"

    if coverage_status == "CLAIM_DEFINED":
        return "PML_IMPLEMENTATION_REVIEW_REQUIRED"

    if coverage_status == "SUPPORTED":
        return "PML_APPROVAL_REQUIRED"

    if coverage_status == "COVERAGE_GAP":
        return "PML_GOVERNANCE_CLASSIFICATION_REQUIRED"

    return "MANUAL_REVIEW_REQUIRED"
