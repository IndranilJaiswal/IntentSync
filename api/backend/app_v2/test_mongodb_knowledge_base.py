"""
Test MongoDB Knowledge Base

Purpose:
Verify seeded MongoDB knowledge base collections and document counts.
"""

from mongodb_client import MongoDBClient


def main():
    """Print seeded collection counts."""

    mongo = MongoDBClient()

    collections = [
        "organization_policies",
        "standards",
        "technical_documentation",
        "claim_library",
        "remediation_library",
    ]

    for collection_name in collections:

        collection = mongo.get_collection(collection_name)

        print(
            collection_name,
            collection.count_documents({}),
        )


if __name__ == "__main__":
    main()
