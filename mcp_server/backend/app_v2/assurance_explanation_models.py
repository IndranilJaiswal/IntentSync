"""
Assurance Explanation Models

Purpose:
Represent human-readable explanations generated from assurance results.

Important:
Explanations do not determine assurance status.
They only explain assurance status.

Future:
This model can support Gemini-generated explanations while preserving
a structured output contract.
"""

from dataclasses import dataclass


@dataclass
class AssuranceExplanation:
    """Structured explanation of an assurance result."""

    title: str
    summary: str
    details: list[str]
    recommendations: list[str]
