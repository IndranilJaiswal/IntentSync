"""
Requirement Models

Requirements express human intent.

Claims make requirements observable.
"""

from dataclasses import dataclass


@dataclass
class Requirement:
    """Represents a business, architecture, security, or operational requirement."""

    requirement_id: str
    title: str
    description: str
    claim_ids: list[str]
