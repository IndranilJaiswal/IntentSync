"""
Claim Assurance Engine

Evaluates whether collected evidence supports an approved claim.

The Assurance Engine does not collect evidence.
It evaluates whether available evidence is sufficient and supportive.
"""

from assurance_models import AssuranceResult


class ClaimAssuranceEngine:
    """Evaluates evidence records against approved claims."""

    def evaluate(self, approved_claim, evidence_records) -> AssuranceResult:
        """
        Evaluate an approved claim using collected evidence records.

        Gate 1:
        Check whether required evidence types exist and were observed.

        Gate 2:
        Apply claim-specific assurance logic.
        """

        evidence_gaps = self._find_evidence_gaps(
            approved_claim,
            evidence_records,
        )

        if evidence_gaps:
            return AssuranceResult(
                claim_id=approved_claim.claim.claim_id,
                target_name=approved_claim.target_name,
                status="INSUFFICIENT_EVIDENCE",
                confidence=0.0,
                evidence_gaps=evidence_gaps,
                explanation=(
                    "Required evidence is missing or has not been observed."
                ),
            )

        if approved_claim.claim.claim_id == "SERVICE_EXISTS":
            return self._evaluate_service_exists(
                approved_claim,
                evidence_records,
            )

        if approved_claim.claim.claim_id == "SERVICE_HEALTHY":
            return self._evaluate_service_healthy(
                approved_claim,
                evidence_records,
            )

        return AssuranceResult(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            status="INSUFFICIENT_EVIDENCE",
            confidence=0.0,
            evidence_gaps=[],
            explanation="No assurance rule is implemented for this claim.",
        )

    def _find_evidence_gaps(self, approved_claim, evidence_records) -> list[str]:
        """
        Identify required evidence that is missing or not observed.

        Compatibility note:
        Some claim definitions may require service_exists, while the
        Dynatrace adapter may provide service_entity. For assurance purposes,
        service_entity can satisfy service_exists because it proves the service
        was observed as a runtime entity.
        """

        evidence_by_type = {
            evidence.evidence_type: evidence
            for evidence in evidence_records
        }

        gaps = []

        for required_type in approved_claim.claim.evidence_required:

            evidence = evidence_by_type.get(required_type)

            if evidence is None and required_type == "service_exists":
                evidence = evidence_by_type.get("service_entity")

            if evidence is None:
                gaps.append(required_type)
                continue

            if evidence.observed is not True:
                gaps.append(required_type)

        return gaps

    def _evaluate_service_exists(self, approved_claim, evidence_records):
        """
        Evaluate SERVICE_EXISTS.

        Supports:
        - service_exists
        - service_entity
        """

        service_exists_record = next(
            (
                evidence
                for evidence in evidence_records
                if evidence.evidence_type in ["service_exists", "service_entity"]
            ),
            None,
        )

        if service_exists_record is None:
            return AssuranceResult(
                claim_id=approved_claim.claim.claim_id,
                target_name=approved_claim.target_name,
                status="INSUFFICIENT_EVIDENCE",
                confidence=0.0,
                evidence_gaps=["service_exists"],
                explanation=(
                    "No service existence or service entity evidence was collected."
                ),
            )

        if service_exists_record.observed is True:
            return AssuranceResult(
                claim_id=approved_claim.claim.claim_id,
                target_name=approved_claim.target_name,
                status="VERIFIED",
                confidence=1.0,
                evidence_gaps=[],
                explanation="Service was observed in Dynatrace runtime reality.",
            )

        return AssuranceResult(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            status="FAILED",
            confidence=1.0,
            evidence_gaps=[],
            explanation="Service was not observed in Dynatrace runtime reality.",
        )

    def _evaluate_service_healthy(self, approved_claim, evidence_records):
        """
        Evaluate SERVICE_HEALTHY.

        At this stage, SERVICE_HEALTHY is considered VERIFIED only when all
        required health evidence has been observed.

        Real response time and failure rate threshold logic will be added after
        live metric collection is implemented.
        """

        return AssuranceResult(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            status="VERIFIED",
            confidence=1.0,
            evidence_gaps=[],
            explanation=(
                "Service health evidence is complete. "
                "Metric threshold evaluation will be added next."
            ),
        )
