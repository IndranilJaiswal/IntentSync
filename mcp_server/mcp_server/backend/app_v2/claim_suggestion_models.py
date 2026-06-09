"""
Claim Suggestion Models

Purpose:
Represent claims suggested by policy or standards agents before
they are approved for assurance.

Important:
A suggested claim is not part of assurance scope until a human approves it.
"""

from dataclasses import dataclass


@dataclass
class ClaimSuggestion:
    """
    Represents a claim suggested by a policy or standards agent.

    The suggestion includes traceability back to the policy or standard
    that caused the claim to be recommended.
    """

    claim_id: str
    policy_id: str
    policy_name: str
    objective_id: str
    objective_description: str
    requirement: str
    approved: bool = False
