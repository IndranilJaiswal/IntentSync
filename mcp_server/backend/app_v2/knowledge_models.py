"""
Knowledge Models

Purpose:
Represent retrieved knowledge used by the future Gemini Assurance Agent.

These models are retrieval-only.

They do not perform:
- AI reasoning
- Assurance evaluation
- MongoDB access
"""

from dataclasses import dataclass


@dataclass
class KnowledgeDocument:
    """
    Single retrieved knowledge document.
    """

    document_id: str
    source_type: str
    title: str
    content: str
    tags: list[str]
    score: float


@dataclass
class RetrievedContext:
    """
    Collection of retrieved knowledge documents.
    """

    requirement: str
    documents: list[KnowledgeDocument]
