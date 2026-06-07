"""
claim_discovery_agent.py

Purpose:
Convert requirements into ClaimSuggestion objects using Gemini reasoning.

Workflow:
Requirement
↓
Knowledge Retrieval
↓
Gemini
↓
ClaimSuggestion with rationale, business impact, and governance need

Author:
Indranil Jaiswal
AI Assurance Platform
"""

import json

from gemini_client import GeminiClient
from knowledge_retriever import KnowledgeRetriever
from claim_suggestion_models import ClaimSuggestion


class ClaimDiscoveryAgent:
    """
    Gemini-backed claim discovery agent.

    This agent reasons over:
    - the requirement text
    - known claim patterns from the knowledge base

    It returns ClaimSuggestion objects enriched with:
    - rationale
    - business impact
    - governance need
    """

    def __init__(self):
        self.gemini = GeminiClient()
        self.retriever = KnowledgeRetriever()

    def discover(self, requirement: str):
        claim_patterns = self.retriever.get_claim_patterns()

        known_claims = [
            pattern["claim_name"]
            for pattern in claim_patterns
        ]

        prompt = f"""
You are an assurance architect.

Requirement:
{requirement}

Known Claims:
{", ".join(known_claims)}

Task:
Suggest claims needed to assure the requirement.

Rules:
- Return valid JSON only.
- Return a JSON array.
- Each item must include:
  - claim_id
  - rationale
  - business_impact
  - governance_need
- Use uppercase claim naming.
- Do not include markdown.
- Do not wrap the JSON in code fences.

Example:
[
  {{
    "claim_id": "SERVICE_REDUNDANT",
    "rationale": "Redundancy is required to reduce single points of failure.",
    "business_impact": "Without redundancy, service interruption may affect business continuity.",
    "governance_need": "PML should confirm whether redundancy is required for this requirement."
  }}
]
"""

        response = self.gemini.generate(prompt)

        try:
            parsed_claims = json.loads(response)

        except json.JSONDecodeError:
            parsed_claims = [
                {
                    "claim_id": line.strip(),
                    "rationale": "AI-discovered claim requiring review.",
                    "business_impact": (
                        "If this claim is not assured, the requirement may "
                        "not be fully supported by observable evidence."
                    ),
                    "governance_need": (
                        "PML must determine whether this claim should become "
                        "part of the governed assurance scope."
                    ),
                }
                for line in response.splitlines()
                if line.strip()
            ]

        suggestions = []

        for item in parsed_claims:

            claim_id = item.get("claim_id", "").strip()

            if not claim_id:
                continue

            rationale = item.get(
                "rationale",
                "AI-discovered claim requiring review.",
            )

            business_impact = item.get(
                "business_impact",
                "If this claim is not assured, the requirement may not be "
                "fully supported.",
            )

            governance_need = item.get(
                "governance_need",
                "PML must classify this claim before execution.",
            )

            suggestion = ClaimSuggestion(
                claim_id=claim_id,
                policy_id="AI_DISCOVERY",
                policy_name="Gemini Discovery Agent",
                objective_id="REQ_DISCOVERY",
                objective_description=rationale,
                requirement=requirement,
            )

            suggestion.rationale = rationale
            suggestion.business_impact = business_impact
            suggestion.governance_need = governance_need

            suggestions.append(suggestion)

        return suggestions
