"""
Requirement Library

Loads requirements from configuration.
"""

from pathlib import Path

import yaml

from requirement_models import Requirement


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"


def load_requirements() -> list[Requirement]:
    """Load requirements from YAML configuration."""

    with open(CONFIG_DIR / "requirements.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return [
        Requirement(
            requirement_id=item["requirement_id"],
            title=item["title"],
            description=item["description"],
            claim_ids=item["claim_ids"],
        )
        for item in data["requirements"]
    ]
