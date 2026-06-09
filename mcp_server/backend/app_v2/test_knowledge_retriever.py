"""
test_knowledge_retriever.py

Purpose:
---------
Validate MongoDB retrieval of
claim pattern knowledge.

Usage:
------
python3 backend/app_v2/test_knowledge_retriever.py
"""

from knowledge_retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()

patterns = retriever.get_claim_patterns()

print("\n==============================")
print("CLAIM PATTERNS")
print("==============================")

for pattern in patterns:
    print(pattern)
