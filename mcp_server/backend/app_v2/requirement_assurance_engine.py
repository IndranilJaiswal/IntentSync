"""
Requirement Assurance Engine

Rolls up claim assurance results into requirement-level assurance.

Rules:
- Any FAILED claim means the requirement is FAILED.
- Any INSUFFICIENT_EVIDENCE claim means the requirement is PARTIALLY_ASSURED.
- All VERIFIED claims means the requirement is VERIFIED.
"""

from requirement_assurance_models import RequirementAssuranceResult


class RequirementAssuranceEngine:
    """Evaluates requirement-level assurance from claim results."""

    def evaluate(self, requirement, claim_results) -> RequirementAssuranceResult:
        """Roll up claim assurance results into requirement assurance."""

        verified_claims = sum(
            1
            for result in claim_results
            if result.status == "VERIFIED"
        )

        insufficient_claims = sum(
            1
            for result in claim_results
            if result.status == "INSUFFICIENT_EVIDENCE"
        )

        failed_claims = sum(
            1
            for result in claim_results
            if result.status == "FAILED"
        )

        if failed_claims > 0:
            status = "FAILED"
            explanation = "One or more supporting claims failed."

        elif insufficient_claims > 0:
            status = "PARTIALLY_ASSURED"
            explanation = "One or more supporting claims have insufficient evidence."

        else:
            status = "VERIFIED"
            explanation = "All supporting claims are verified."

        return RequirementAssuranceResult(
            requirement_id=requirement.requirement_id,
            title=requirement.title,
            status=status,
            verified_claims=verified_claims,
            insufficient_claims=insufficient_claims,
            failed_claims=failed_claims,
            claim_results=claim_results,
            explanation=explanation,
        )
