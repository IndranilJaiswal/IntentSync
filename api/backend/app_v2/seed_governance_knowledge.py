"""
seed_governance_knowledge.py

Purpose:
---------
Seed governance knowledge collections.

Collections:
------------
policies
standards

Author:
--------
Indranil Jaiswal
AI Assurance Platform
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI")
)

db = client["ai_assurance"]

policies = db["policies"]
standards = db["standards"]

# ----------------------------------------
# Development reset
# ----------------------------------------

policies.delete_many({})
standards.delete_many({})

# ----------------------------------------
# Policies
# ----------------------------------------

policies.insert_many(
    [
        {
            "policy_id": "POL-001",
            "title": "Service Availability Policy",
            "tags": [
                "availability",
                "service",
                "uptime"
            ],
            "content": (
                "Customer-facing services "
                "shall maintain availability "
                "and resiliency."
            ),
        },
        {
            "policy_id": "POL-002",
            "title": "Business Continuity Policy",
            "tags": [
                "recovery",
                "continuity",
                "resilience"
            ],
            "content": (
                "Critical services shall "
                "support recovery objectives."
            ),
        },
    ]
)

# ----------------------------------------
# Standards
# ----------------------------------------

standards.insert_many(
    [
        {
            "standard_id": "IEC62443-SR7-1",
            "title": "Resource Availability",
            "tags": [
                "availability",
                "capacity",
                "resilience"
            ],
            "content": (
                "Resources shall remain "
                "available under expected load."
            ),
        },
        {
            "standard_id": "IEC62443-SR7-2",
            "title": "Denial Of Service Protection",
            "tags": [
                "availability",
                "dos",
                "resilience"
            ],
            "content": (
                "Systems shall resist "
                "availability degradation."
            ),
        },
    ]
)

print(
    "Governance knowledge seeded successfully."
)
