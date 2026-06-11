"""
MongoDB Client

Purpose:
Provide a simple MongoDB Atlas connection for the assurance knowledge base.

Responsibilities:
- Load MongoDB configuration from .env
- Connect to MongoDB Atlas
- Return configured collections

Important:
This module does not contain retrieval or AI logic.
It only manages MongoDB access.
"""

import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


class MongoDBClient:
    """MongoDB Atlas client for the assurance knowledge base."""

    def __init__(self):
        """Initialize MongoDB client and database handle."""

        uri = os.getenv("MONGODB_URI")
        database_name = os.getenv("MONGODB_DATABASE")

        if not uri:
            raise ValueError("MONGODB_URI is not set in .env")

        if not database_name:
            raise ValueError("MONGODB_DATABASE is not set in .env")

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where(),
        )

        self.database = self.client[database_name]

    def ping(self) -> dict:
        """Verify MongoDB connectivity."""

        return self.client.admin.command("ping")

    def get_collection(self, collection_name: str):
        """Return a MongoDB collection."""

        return self.database[collection_name]
