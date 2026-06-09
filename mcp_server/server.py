"""
IntentSync MCP Server

Exposes IntentSync assurance capabilities as MCP tools for
Google Agent Builder.

Tools:
- run_assurance
- discover_claims
- generate_claim_review_package
"""

import sys
from pathlib import Path
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------
# Backend Import Path
# ---------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "backend" / "app_v2"

sys.path.insert(0, str(APP_DIR))

# ---------------------------------------------------------
# IntentSync Imports
# ---------------------------------------------------------

from assurance_service import (  # noqa: E402
    run_assurance_for_requirement,
    serialize_assurance_result,
)

from claim_discovery_agent import (  # noqa: E402
    ClaimDiscoveryAgent,
)

from claim_review_package_builder import (  # noqa: E402
    build_claim_review_packages,
)

from governance_approval_service import approve_claims
from requirement_resolver import resolve_requirement as resolve_requirement_service  # noqa: E402
from governance_approval_service import approve_claims
from governance_approval_service import ( # noqa: E402
approve_claims,
approve_and_promote_claim,
)

# ---------------------------------------------------------
# MCP Server
# ---------------------------------------------------------

mcp = FastMCP(
    name="IntentSync MCP",
    instructions=(
        "IntentSync synchronizes intent with reality through "
        "continuous assurance. "
        "Use run_assurance to verify requirements using runtime "
        "evidence. "
        "Use discover_claims to identify assurance claims. "
        "Use generate_claim_review_package to create governance "
        "review packages."
    ),
    host="0.0.0.0",
    port=8080,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


# ---------------------------------------------------------
# Tool 1
# ---------------------------------------------------------

@mcp.tool()
def run_assurance(
    requirement_id: str,
    approved_governed_claim_ids: Optional[List[str]] = None,
    target_name: str = "easyTravel-Business",
) -> dict:
    """
    Run assurance for a requirement.

    Returns:
        Requirement assurance result with evidence.
    """

    result = run_assurance_for_requirement(
        requirement_id=requirement_id,
        approved_governed_claim_ids=approved_governed_claim_ids,
        target_name=target_name,
    )

    return serialize_assurance_result(result)


# ---------------------------------------------------------
# Tool 2
# ---------------------------------------------------------

@mcp.tool()
def discover_claims(
    requirement_text: str,
) -> dict:
    """
    Discover assurance claims required to assure a requirement.

    Returns:
        Candidate claims with rationale,
        business impact,
        governance need.
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


# ---------------------------------------------------------
# Tool 3
# ---------------------------------------------------------

@mcp.tool()
def generate_claim_review_package(
    requirement_text: str,
) -> dict:
    """
    Generate governance-ready claim review packages.

    Workflow:
        Requirement
            ↓
        Claim Discovery
            ↓
        Review Package Generation
            ↓
        Governance Routing
    """

    agent = ClaimDiscoveryAgent()

    suggestions = agent.discover(requirement_text)

    return build_claim_review_packages(
        requirement_text=requirement_text,
        suggestions=suggestions,
    )

@mcp.tool()
def approve_claims_for_assurance(
    claim_ids: list[str],
    approver: str = "PML",
) -> dict:
    """
    Approve claims for governed assurance execution.
    """

    return approve_claims(
        claim_ids=claim_ids,
        approver=approver,
    )

@mcp.tool()
def resolve_requirement(requirement_text: str) -> dict:
    """
    Resolve natural language requirement text to a known requirement ID.
    """

    return resolve_requirement_service(
        requirement_text=requirement_text,
    )

@mcp.tool()
def approve_and_promote_claim(
    claim_id: str,
    approved_by: str,
    rationale: str,
):
    """
    Approve a coverage-gap claim and promote it into
    the governed claim library.
    """

    return approve_claims(
        claim_id=claim_id,
        approved_by=approved_by,
        rationale=rationale,
    )

@mcp.tool()
def approve_and_promote_claim_for_governance(
    claim_id: str,
    approved_by: str = "PML",
    rationale: str = "",
) -> dict:
    """
    Approve a discovered claim and promote it into governed knowledge.

    This does not automatically make the claim executable.
    The capability matrix determines whether the claim is executable,
    partially executable, or only claim-defined.
    """

    return approve_and_promote_claim(
        claim_id=claim_id,
        approved_by=approved_by,
        rationale=rationale,
    )
# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
    )
