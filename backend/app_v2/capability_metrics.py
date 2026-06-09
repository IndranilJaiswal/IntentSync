"""
capability_metrics.py

Computes Assurance Capability Metrics from
claim review packages.
"""


def calculate_assurance_readiness(
    review_packages: list[dict],
) -> dict:

    total_claims = len(review_packages)

    executable = 0
    partially_executable = 0
    claim_defined = 0
    coverage_gaps = 0

    missing_capabilities = set()

    for package in review_packages:

        executability = package.get(
            "executability",
            "COVERAGE_GAP",
        )

        if executability == "EXECUTABLE":
            executable += 1

        elif executability == "PARTIALLY_EXECUTABLE":
            partially_executable += 1

        elif executability == "CLAIM_DEFINED":
            claim_defined += 1

        elif executability == "COVERAGE_GAP":
            coverage_gaps += 1

        for capability in package.get(
            "missing_capabilities",
            [],
        ):
            missing_capabilities.add(capability)

    readiness = 0.0

    if total_claims > 0:
        readiness = round(
            (
                executable
                + (partially_executable * 0.5)
            )
            / total_claims
            * 100,
            1,
        )

    return {
        "total_claims": total_claims,
        "executable_claims": executable,
        "partially_executable_claims":
            partially_executable,
        "claim_defined":
            claim_defined,
        "coverage_gaps":
            coverage_gaps,
        "assurance_readiness_percent":
            readiness,
        "top_missing_capabilities":
            sorted(list(missing_capabilities)),
    }
