"""
pml_claim_mapping_agent.py

Purpose:
Recommend mappings between AI-discovered claims and existing governed claims.

The agent supports PML review by identifying whether a newly discovered claim
is semantically equivalent to an existing governed claim.

Important:
The agent does not approve mappings.
The agent does not update the claim library.
The agent only recommends mappings for PML decision.
"""

import json

from gemini_client import GeminiClient


class PMLClaimMappingAgent:
    """
    Gemini-backed mapping agent for PML claim governance.

    Example:
    LATENCY_WITHIN_THRESHOLD
    may map to
    LATENCY_WITHIN_LIMITS
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def recommend_mapping(
        self,
        discovered_claim: str,
        governed_claims: list[str],
    ) -> dict:
        """
        Recommend the closest governed claim for a discovered claim.

        Returns:
            dict with:
            - mapped_claim
            - confidence
            - rationale
        """

        prompt = f"""
You are a governance architect.

Discovered Claim:
{discovered_claim}

Governed Claims:
{", ".join(governed_claims)}

Task:
Determine whether the discovered claim can be mapped to an existing governed claim.

Rules:
- Return JSON only.
- Do not include markdown.
- Do not use code fences.
- If no good mapping exists, return mapped_claim as null.
- confidence must be between 0 and 1.

Example:
{{
  "mapped_claim": "LATENCY_WITHIN_LIMITS",
  "confidence": 0.92,
  "rationale": "Both claims describe acceptable latency boundaries."
}}
"""

        response = self.gemini.generate(prompt)

        try:
            parsed = json.loads(response)

            return {
                "mapped_claim": parsed.get("mapped_claim"),
                "confidence": float(parsed.get("confidence", 0.0)),
                "rationale": parsed.get(
                    "rationale",
                    "Mapping rationale not provided.",
                ),
            }

        except Exception:
            return {
                "mapped_claim": None,
                "confidence": 0.0,
                "rationale": "Mapping recommendation unavailable.",
            }
