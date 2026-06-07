# Knowledge Layer

## Purpose

The Knowledge Layer provides contextual information used by the
Gemini Assurance Agent to discover assurance claims.

## Knowledge Sources

### Organization Policies

Internal governance requirements.

Examples:

- Service Availability Policy
- Monitoring Policy

### Standards

External guidance.

Examples:

- IEC 62443
- NIST

### Technical Documentation

System-specific implementation knowledge.

Examples:

- Service architecture
- Dependency documentation
- Runbooks

## Storage Technology

MongoDB Atlas

## Collections

organization_policies

standards

technical_documentation

claim_library

remediation_library

## Current State

Seeded through:

seed_knowledge_base.py

## Future State

Document Upload
→ Ingestion Pipeline
→ Chunking
→ Embeddings
→ Atlas Vector Search
→ Gemini Retrieval
