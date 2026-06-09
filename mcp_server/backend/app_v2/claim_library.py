"""
Claim Library

Loads claim templates and enriches them with Dynatrace capability metadata.
"""

from pathlib import Path

import yaml

from claim_models import Claim


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"


def load_yaml(file_path: Path) -> dict:
    """Load a YAML file and return its contents as a dictionary."""

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_claim_library() -> list[Claim]:
    """Load all claim templates from the claim library."""

    claim_data = load_yaml(CONFIG_DIR / "claim_library.yaml")
    capability_matrix = load_yaml(CONFIG_DIR / "capability_matrix.yaml")

    claims = []

    for item in claim_data["claims"]:
        capability = capability_matrix[item["claim_id"]]

        claims.append(
            Claim(
                claim_id=item["claim_id"],
                name=item["name"],
                category=item["category"],
                description=item["description"],
                evidence_required=capability["evidence"],
                entity_type=capability["entity_type"],
                verifiability=capability["verifiability"],
            )
        )

    return claims
