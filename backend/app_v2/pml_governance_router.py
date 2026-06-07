"""
PML Governance Router

Routes claim review packages into the correct governance lane.

This prevents unsupported AI-discovered claims from flowing directly
into SDL execution.
"""


def route_claim_review_package(package) -> str:
    """
    Route a claim review package based on its coverage status.

    Supported claims:
        Existing executable claims. These require PML approval before
        SDL execution.

    Coverage gaps:
        New or unsupported claims. These require PML classification
        before becoming part of the governed claim library.
    """

    coverage_status = getattr(package, "coverage_status", None)

    if coverage_status == "SUPPORTED":
        return "PML_APPROVAL_REQUIRED"

    if coverage_status == "COVERAGE_GAP":
        return "PML_GOVERNANCE_CLASSIFICATION_REQUIRED"

    return "MANUAL_REVIEW_REQUIRED"
