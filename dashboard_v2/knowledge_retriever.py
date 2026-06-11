"""
knowledge_retriever.py

Purpose:
---------
Retrieves governed knowledge from MongoDB.

Current Sources:
----------------
- claim_patterns
- policies
- standards

Future Sources:
---------------
- technical_documents
- remediation_patterns

This module provides retrieval context for:
- Gemini Claim Discovery Agent
- PML Claim Review Package Builder
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


class KnowledgeRetriever:
    """
    Retrieves knowledge documents from MongoDB.

    This class does not call Gemini.
    It only retrieves governed knowledge.
    """

    def __init__(self):
        """Initialize MongoDB connection."""

        mongodb_uri = os.getenv("MONGODB_URI")

        if not mongodb_uri:
            raise ValueError(
                "MONGODB_URI not configured"
            )

        self.client = MongoClient(mongodb_uri)

        self.db = self.client["ai_assurance"]

    def get_claim_patterns(self) -> list[dict]:
        """
        Retrieve claim patterns.

        Claim patterns are examples used by Gemini
        during claim discovery.
        """

        return list(
            self.db["claim_patterns"].find(
                {},
                {"_id": 0},
            )
        )

    def get_policies(self) -> list[dict]:
        """
        Retrieve governance policies.

        Policies provide business and organizational
        traceability for claim review packages.
        """

        return list(
            self.db["policies"].find(
                {},
                {"_id": 0},
            )
        )

    def get_standards(self) -> list[dict]:
        """
        Retrieve standards guidance.

        Standards provide external or internal technical
        assurance references for claim review packages.
        """

        return list(
            self.db["standards"].find(
                {},
                {"_id": 0},
            )
        )
