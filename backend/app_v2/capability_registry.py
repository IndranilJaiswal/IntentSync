from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).parent / "config"
CAPABILITY_MATRIX = CONFIG_DIR / "capability_matrix.yaml"


def load_capability_matrix() -> dict:
    with open(CAPABILITY_MATRIX, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_claim_capability(claim_id: str) -> dict:
    matrix = load_capability_matrix()

    capability = matrix.get(claim_id)

    if not capability:
        return {
            "evidence": [],
            "entity_type": None,
            "verifiability": "NOT_DEFINED",
            "assurance_logic": False,
            "evidence_provider": "none",
            "mcp_capabilities": [],
            "missing_capabilities": [],
            "executability": "COVERAGE_GAP",
        }

    return {
        "evidence": capability.get("evidence", []),
        "entity_type": capability.get("entity_type"),
        "verifiability": capability.get("verifiability", "UNKNOWN"),
        "assurance_logic": capability.get("assurance_logic", True),
        "evidence_provider": capability.get("evidence_provider", "dynatrace_mcp"),
        "mcp_capabilities": capability.get("mcp_capabilities", capability.get("evidence", [])),
        "missing_capabilities": capability.get("missing_capabilities", []),
        "executability": capability.get("executability", capability.get("verifiability", "UNKNOWN")),
    }
