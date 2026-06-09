"""
Assurance Explanation Engine

Purpose:
Convert deterministic assurance results into human-readable explanations.

Important:
This engine does not change assurance outcomes.
It only explains outcomes already produced by the Assurance Engine.

Current:
Deterministic explanation generation.

Future:
Gemini-assisted explanation generation using the same input/output contract.
"""

from assurance_explanation_models import AssuranceExplanation


class AssuranceExplanationEngine:
    """Generates explanations from requirement assurance results."""

    def explain(self, requirement_result) -> AssuranceExplanation:
        """Generate an explanation for a requirement assurance result."""

        if requirement_result.status == "VERIFIED":
            return self._explain_verified(requirement_result)

        if requirement_result.status == "PARTIALLY_ASSURED":
            return self._explain_partially_assured(requirement_result)

        if requirement_result.status == "FAILED":
            return self._explain_failed(requirement_result)

        return AssuranceExplanation(
            title="Requirement Assurance Unknown",
            summary="The requirement assurance status could not be explained.",
            details=[
                "The explanation engine does not recognize the assurance status."
            ],
            recommendations=[
                "Review the assurance result and supported status values."
            ],
        )

    def _explain_verified(self, requirement_result) -> AssuranceExplanation:
        """Explain a verified requirement."""

        return AssuranceExplanation(
            title="Requirement Verified",
            summary=(
                "The requirement is verified because all supporting claims "
                "were supported by observed evidence."
            ),
            details=[
                f"Verified claims: {requirement_result.verified_claims}",
                "No failed claims were detected.",
                "No evidence gaps were detected.",
            ],
            recommendations=[
                "Continue monitoring for evidence drift."
            ],
        )

    def _explain_partially_assured(
        self,
        requirement_result,
    ) -> AssuranceExplanation:
        """Explain a partially assured requirement."""

        evidence_gaps = []

        for claim_result in requirement_result.claim_results:
            for gap in claim_result.evidence_gaps:
                evidence_gaps.append(
                    f"{claim_result.claim_id}: {gap}"
                )

        details = [
            f"Verified claims: {requirement_result.verified_claims}",
            (
                "Claims with insufficient evidence: "
                f"{requirement_result.insufficient_claims}"
            ),
            f"Failed claims: {requirement_result.failed_claims}",
        ]

        if evidence_gaps:
            details.append(
                "Evidence gaps were detected in the supporting claims."
            )

        recommendations = []

        for gap in evidence_gaps:
            recommendations.append(
                f"Collect missing evidence for {gap}."
            )

        if not recommendations:
            recommendations.append(
                "Review supporting claims with insufficient evidence."
            )

        return AssuranceExplanation(
            title="Requirement Partially Assured",
            summary=(
                "The requirement is partially assured. Some supporting claims "
                "were verified, but others could not be justified because "
                "required evidence is missing."
            ),
            details=details + evidence_gaps,
            recommendations=recommendations,
        )

    def _explain_failed(self, requirement_result) -> AssuranceExplanation:
        """Explain a failed requirement."""

        failed_claims = [
            claim_result.claim_id
            for claim_result in requirement_result.claim_results
            if claim_result.status == "FAILED"
        ]

        return AssuranceExplanation(
            title="Requirement Failed",
            summary=(
                "The requirement failed because one or more supporting claims "
                "were contradicted by evidence."
            ),
            details=[
                f"Failed claims: {', '.join(failed_claims)}",
                f"Verified claims: {requirement_result.verified_claims}",
                (
                    "Claims with insufficient evidence: "
                    f"{requirement_result.insufficient_claims}"
                ),
            ],
            recommendations=[
                "Investigate failed claims and review operational reality.",
                "Confirm whether the requirement still reflects intended policy.",
            ],
        )
