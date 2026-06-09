"""
IntentSync MCP Server

Exposes IntentSync assurance capabilities as MCP tools for Google Agent Builder.

Tool exposed:
- run_assurance

Architecture:
Agent Builder
    ↓
IntentSync MCP Server
    ↓
IntentSync Assurance Service
    ↓
Dynatrace Partner MCP
    ↓
Runtime Evidence
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "backend" / "app_v2"

sys.path.insert(0, str(APP_DIR))

from typing import List, Optional

from mcp.server.fastmcp import FastMCP
from claim_discovery_agent import ClaimDiscoveryAgent  # noqa: E402

ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "backend" / "app_v2"
sys.path.append(str(APP_DIR))


from assurance_service import (  # noqa: E402
    run_assurance_for_requirement,
    serialize_assurance_result,
)


mcp = FastMCP(
    name="IntentSync MCP",
    instructions=(
        "IntentSync synchronizes intent with reality through continuous "
        "assurance. Use run_assurance to verify whether a requirement is "
        "supported by governed claims and runtime evidence."
    ),
    host="0.0.0.0",
    port=8080,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def run_assurance(
    requirement_id: str,
    approved_governed_claim_ids: Optional[List[str]] = None,
    target_name: str = "easyTravel-Business",
) -> dict:
    """
    Run assurance for a system requirement.

    Args:
        requirement_id: Requirement identifier, for example REQ-001.
        approved_governed_claim_ids: Optional governed claim IDs to evaluate.
        target_name: Runtime target service name.

    Returns:
        JSON-safe assurance result with requirement status, claim results,
        and Dynatrace Partner MCP evidence summary.
    """

    result = run_assurance_for_requirement(
        requirement_id=requirement_id,
        approved_governed_claim_ids=approved_governed_claim_ids,
        target_name=target_name,
    )

    return serialize_assurance_result(result)

@mcp.tool()
def discover_claims(requirement_text: str) -> dict:
    """
    Discover assurance claims required to assure a requirement.

    Args:
        requirement_text: Natural language requirement text.

    Returns:
        Candidate assurance claims with rationale, business impact,
        and governance need.
    """

    agent = ClaimDiscoveryAgent()
    suggestions = agent.discover(requirement_text)

    return {
        "requirement_text": requirement_text,
        "claim_suggestions": [
            {
                "claim_id": suggestion.claim_id,
                "policy_id": suggestion.policy_id,
                "policy_name": suggestion.policy_name,
                "objective_id": suggestion.objective_id,
                "objective_description": (
                    suggestion.objective_description
                ),
                "rationale": getattr(
                    suggestion,
                    "rationale",
                    suggestion.objective_description,
                ),
                "business_impact": getattr(
                    suggestion,
                    "business_impact",
                    None,
                ),
                "governance_need": getattr(
                    suggestion,
                    "governance_need",
                    None,
                ),
            }
            for suggestion in suggestions
        ],
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
