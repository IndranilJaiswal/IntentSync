"""
Policy Models

Purpose:
Represent organizational policies and objectives that may
generate candidate assurance claims.

Responsibilities:
- Store policy metadata
- Store policy objectives
- Store suggested claims

Future Evolution:
Support standards, regulations, and framework mappings.
"""

from dataclasses import dataclass


@dataclass
class PolicyObjective:
    """
    Represents a single policy objective.

    Example:
    Business-critical services must remain healthy.
    """

    objective_id: str
    description: str
    suggested_claims: list[str]


@dataclass
class Policy:
    """
    Represents an organizational policy.

    A policy contains multiple objectives.
    """

    policy_id: str
    name: str
    description: str
    objectives: list[PolicyObjective]
