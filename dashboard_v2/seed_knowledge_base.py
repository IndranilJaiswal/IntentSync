"""
Seed Knowledge Base

Purpose:
Seed MongoDB Atlas with starter assurance knowledge documents.

Collections:
- organization_policies
- standards
- technical_documentation
- claim_library
- remediation_library

This creates the first knowledge base used by the future Gemini Assurance Agent.
"""

from datetime import datetime, timezone

from mongodb_client import MongoDBClient


def utc_now():
    """Return current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def seed_collection(collection, documents):
    """
    Replace seed documents in a collection.

    We delete only documents marked as seed_data=True so future manually added
    documents are not accidentally removed.
    """

    collection.delete_many({"seed_data": True})

    if documents:
        collection.insert_many(documents)


def main():
    """Seed MongoDB assurance knowledge base."""

    mongo = MongoDBClient()

    print("MongoDB ping:", mongo.ping())

    now = utc_now()

    organization_policies = [
        {
            "document_id": "POL-001",
            "source_type": "organization_policy",
            "title": "Service Availability Policy",
            "content": (
                "Business-critical customer-facing services must remain "
                "available, observable, and monitored. Critical services must "
                "exist in operational reality and must have sufficient telemetry "
                "to determine service health."
            ),
            "tags": [
                "availability",
                "service",
                "monitoring",
                "telemetry",
            ],
            "owner": "Operations Governance",
            "version": "1.0",
            "seed_data": True,
            "created_at": now,
        },
        {
            "document_id": "POL-002",
            "source_type": "organization_policy",
            "title": "Operational Monitoring Policy",
            "content": (
                "Critical applications must expose response time, error rate, "
                "failure rate, availability, and active problem indicators. "
                "Monitoring gaps must be documented and remediated."
            ),
            "tags": [
                "monitoring",
                "response_time",
                "failure_rate",
                "error_rate",
            ],
            "owner": "Platform Operations",
            "version": "1.0",
            "seed_data": True,
            "created_at": now,
        },
    ]

    standards = [
        {
            "document_id": "STD-001",
            "source_type": "standard",
            "title": "Critical Service Monitoring Guidance",
            "content": (
                "Critical systems should support monitoring, event collection, "
                "failure detection, and operational visibility. Assurance should "
                "be based on observable evidence rather than assumptions."
            ),
            "tags": [
                "monitoring",
                "event_collection",
                "evidence",
                "critical_systems",
            ],
            "standard_family": "Internal Standard Based on Industry Guidance",
            "version": "1.0",
            "seed_data": True,
            "created_at": now,
        }
    ]

    technical_documentation = [
        {
            "document_id": "ARCH-001",
            "source_type": "technical_documentation",
            "title": "Booking Service Architecture",
            "content": (
                "The customer booking service is represented by "
                "easyTravel-Business. The service depends on supporting runtime "
                "components and should be observable through Dynatrace. Service "
                "health should be assessed using response time and failure rate."
            ),
            "tags": [
                "booking",
                "easyTravel-Business",
                "dynatrace",
                "service_health",
            ],
            "owner": "Application Architecture",
            "version": "1.0",
            "seed_data": True,
            "created_at": now,
        }
    ]

    claim_library = [
        {
            "claim_id": "SERVICE_EXISTS",
            "name": "Service Exists",
            "description": "Required service is observed in runtime reality.",
            "required_evidence": [
                "service_exists",
            ],
            "tags": [
                "availability",
                "service",
            ],
            "seed_data": True,
            "created_at": now,
        },
        {
            "claim_id": "SERVICE_HEALTHY",
            "name": "Service Healthy",
            "description": (
                "Service exists and has sufficient health telemetry."
            ),
            "required_evidence": [
                "service_exists",
                "response_time",
                "failure_rate",
            ],
            "tags": [
                "availability",
                "service_health",
                "monitoring",
            ],
            "seed_data": True,
            "created_at": now,
        },
        {
            "claim_id": "NO_ACTIVE_PROBLEMS",
            "name": "No Active Problems",
            "description": (
                "No active operational problems are associated with the service."
            ),
            "required_evidence": [
                "active_problems",
            ],
            "tags": [
                "operations",
                "problem_detection",
            ],
            "seed_data": True,
            "created_at": now,
        },
    ]

    remediation_library = [
        {
            "remediation_id": "REM-001",
            "gap_type": "response_time",
            "title": "Enable Response Time Monitoring",
            "description": (
                "Configure or validate response time monitoring for the target "
                "service in Dynatrace."
            ),
            "checklist": [
                "Identify target service entity.",
                "Confirm response time metric availability.",
                "Enable or configure response time collection.",
                "Validate metric visibility in Dynatrace.",
                "Re-run assurance after telemetry is available.",
            ],
            "suggested_owner": "Application Operations",
            "priority": "HIGH",
            "seed_data": True,
            "created_at": now,
        },
        {
            "remediation_id": "REM-002",
            "gap_type": "failure_rate",
            "title": "Enable Failure Rate Monitoring",
            "description": (
                "Configure or validate failure rate monitoring for the target "
                "service in Dynatrace."
            ),
            "checklist": [
                "Identify target service entity.",
                "Confirm failure rate metric availability.",
                "Enable or configure failure rate collection.",
                "Validate metric visibility in Dynatrace.",
                "Re-run assurance after telemetry is available.",
            ],
            "suggested_owner": "Application Operations",
            "priority": "HIGH",
            "seed_data": True,
            "created_at": now,
        },
    ]

    seed_collection(
        mongo.get_collection("organization_policies"),
        organization_policies,
    )

    seed_collection(
        mongo.get_collection("standards"),
        standards,
    )

    seed_collection(
        mongo.get_collection("technical_documentation"),
        technical_documentation,
    )

    seed_collection(
        mongo.get_collection("claim_library"),
        claim_library,
    )

    seed_collection(
        mongo.get_collection("remediation_library"),
        remediation_library,
    )

    print("Knowledge base seeded successfully.")


if __name__ == "__main__":
    main()
