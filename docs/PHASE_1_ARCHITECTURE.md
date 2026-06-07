# AI Decision Assurance Platform

## Phase 1 Architecture

### Objective

Determine whether approved observable claims are supported by operational reality.

The platform does not assure requirements directly.

The platform assures approved claims using collected evidence.

---

# Core Flow

Requirement
↓
Claim Selection
↓
Evidence Collection
↓
Assurance Evaluation
↓
Decision Assurance Report

---

# Component Overview

## claim_models.py

Defines the core domain objects.

Responsibilities:

* Claim definition
* Approved claim definition

Purpose:

Provides the foundational data structures used throughout the platform.

---

## claim_library.yaml

Contains reusable claim templates.

Examples:

* Service Exists
* Service Healthy
* Dependency Exists

Purpose:

Provides a catalog of approved observable claims.

---

## capability_matrix.yaml

Maps claims to evidence requirements.

Purpose:

Defines what evidence is required to verify a claim and whether Dynatrace can provide it.

Example:

SERVICE_HEALTHY
↓
service_exists
failure_rate
response_time

---

## claim_library.py

Loads claim definitions and enriches them using capability metadata.

Purpose:

Creates executable claim objects from YAML configuration.

---

## evidence_models.py

Defines evidence request objects.

Purpose:

Represents the facts required to evaluate a claim.

---

## evidence_request_builder.py

Converts approved claims into evidence requests.

Purpose:

Separates claim definition from evidence collection.

Example:

SERVICE_HEALTHY
↓
service_exists
failure_rate
response_time

---

## evidence_engine.py

Collects evidence from reality sources.

Phase 1 Source:

Dynatrace

Future Sources:

* AWS
* Azure
* Kubernetes
* ServiceNow

---

## assurance_engine.py

Evaluates collected evidence against claim rules.

Outputs:

* VERIFIED
* PARTIALLY VERIFIED
* FAILED
* INSUFFICIENT_EVIDENCE

---

## reality_engine.py

Interfaces with external systems to collect operational reality.

Phase 1:

Dynatrace

---

## main.py

Platform orchestration entry point.

Coordinates:

Claims
↓
Evidence
↓
Assurance

---

# Design Principles

1. Requirements are not directly evaluated.

2. Only approved observable claims can be assured.

3. Evidence collection is separated from claim definition.

4. AI assists interpretation but does not determine truth.

5. Every assurance decision must be traceable to evidence.

---

# Current Milestone

Phase 1A - Claim Assurance Core

Completed:

✓ Claim Library

✓ Capability Matrix

✓ Claim Models

In Progress:

□ Evidence Request Builder

□ Evidence Collection

□ Assurance Evaluation

Future:

□ Standards-Based Claims

□ Dynatrace Evidence Adapters

□ Decision Assurance Dashboard
## evidence_models.py

Defines evidence request objects.

Purpose:

Represents the observable facts required
to evaluate a claim.

---

## evidence_request_builder.py

Converts approved claims into evidence requests.

Purpose:

Creates the bridge between:

Claim
↓
Evidence

Example:

SERVICE_HEALTHY

↓

service_exists
failure_rate
response_time
## evidence_records.py

Defines evidence records collected from reality sources.

Purpose:

Represents observable facts collected from external systems.

Example:

Service Exists
↓
Observed = True

Evidence records do not make assurance decisions.

They only record reality.

---

## dynatrace_adapter.py

Collects evidence from Dynatrace.

Purpose:

Transforms evidence requests into evidence records.

Example:

Evidence Request:
service_exists

↓

Dynatrace Service Lookup

↓

Evidence Record

Observed = True

---

Current Evidence Sources

Phase 1:

- Dynatrace

Future:

- AWS
- Azure
- Kubernetes
- ServiceNow
## Legacy MVP Components

### reality_engine.py

Phase 0 MVP component.

Purpose:

Compare declared architecture against observed runtime topology.

Produces:

Truth Gap Report

This component will remain supported for backward compatibility.

Future versions will introduce dedicated reality providers.

---

### evidence_engine.py

Phase 0 MVP component.

Purpose:

Convert truth gaps into evidence records.

Future versions will introduce evidence collection directly from runtime sources.
## reality_provider.py

Provides normalized runtime reality.

Purpose:

Decouples evidence collection from external systems.

Phase 1 Source:

Dynatrace

Future Sources:

- AWS
- Azure
- Kubernetes
- ServiceNow
## Runtime Reality Layer

Purpose:

Provide a normalized representation of observed operational reality.

The platform should not depend directly on vendor APIs.

Instead, external systems are normalized into RuntimeReality.

Benefits:

- Decouples assurance logic from vendor implementations.
- Supports multiple evidence sources.
- Enables consistent evidence collection.

Examples:

- Dynatrace
- AWS
- Azure
- Kubernetes
- ServiceNow
## Runtime Reality Layer

Purpose:

Provide a normalized representation of observed operational reality.

The platform should not depend directly on vendor APIs.

Instead, external systems are normalized into RuntimeReality.

Benefits:

- Decouples assurance logic from vendor implementations.
- Supports multiple evidence sources.
- Enables consistent evidence collection.

Examples:

- Dynatrace
- AWS
- Azure
- Kubernetes
- ServiceNow

---

## reality_provider.py

Defines the RuntimeReality model and provider interface.

Purpose:

Create a standard representation of operational reality regardless of source.

---

## mock_dynatrace_provider.py

Temporary Dynatrace implementation.

Purpose:

Allow development and testing of the Claim → Evidence flow before live Dynatrace API integration.
## dynatrace_client.py

Low-level Dynatrace API client.

Purpose:

Handles authenticated calls to Dynatrace APIs.

Does not contain assurance logic.

---

## dynatrace_provider.py

Live Dynatrace runtime reality provider.

Purpose:

Converts Dynatrace entities into normalized RuntimeReality.

Current support:

- SERVICE entities
## test_dynatrace_adapter.py

Purpose:

Validate the complete Claim → Evidence flow using
live Dynatrace runtime reality.

Current Validation:

SERVICE_EXISTS

Future Validation:

- SERVICE_HEALTHY
- NO_ACTIVE_PROBLEMS
- DEPENDENCY_EXISTS
## Live Dynatrace Validation

Current Supported Validation:

SERVICE_EXISTS

Flow:

Approved Claim
↓
Evidence Request Builder
↓
Dynatrace Provider
↓
Runtime Reality
↓
Evidence Adapter
↓
Evidence Record

Current Runtime Reality Source:

Dynatrace SaaS Tenant

Current Validated Service:

easyTravel-Business

## evidence_collection_engine.py

Purpose:

Coordinates evidence collection for approved claims.

Responsibilities:

- Generate evidence requests
- Collect evidence
- Return evidence records

The engine does not perform assurance evaluation.
\

Approved Claim
↓
Evidence Requests
↓
Evidence Adapter
↓
Evidence Records

## Requirement Layer

Requirements express human intent.

Claims make requirements observable.

Architecture:

Requirement
↓
Approved Claims
↓
Evidence
↓
Assurance

---

## requirement_models.py

Defines requirement domain objects.

---

## requirement_library.py

Loads requirements from configuration.

---

## claim_assurance_engine.py

Evaluates evidence records against approved claims.

Phase 1C currently supports SERVICE_EXISTS.
## Requirement Assurance Rollup

Purpose:

Rolls multiple claim assurance results into a requirement-level assurance result.

Rules:

- Any FAILED claim results in FAILED.
- Any INSUFFICIENT_EVIDENCE claim results in PARTIALLY_ASSURED.
- All VERIFIED claims results in VERIFIED.

---

## requirement_assurance_models.py

Defines requirement-level assurance result objects.

---

## requirement_assurance_engine.py

Evaluates requirement status from supporting claim results.

## Dashboard v1

Purpose:

Displays the end-to-end assurance flow.

Shows:

- Requirements
- Requirement assurance status
- Supporting claims
- Claim assurance status
- Evidence records
- Missing evidence
- Explanation

Current dashboard:

dashboard_v2/app.py

## Dashboard v1

Purpose

Provides visibility into the full assurance workflow.

Flow

Requirement
↓
Claims
↓
Evidence Records
↓
Claim Assurance
↓
Requirement Assurance

Displayed Information

- Requirement status
- Supporting claims
- Evidence records
- Assurance explanations
- Missing evidence
- Claim confidence

Implementation

dashboard_v2/app.py

## Phase 1E – Service Health Assurance

Purpose

Introduce evidence coverage evaluation for service health claims.

Previously the platform only evaluated:

* SERVICE_EXISTS

The platform can now evaluate:

* SERVICE_HEALTHY

---

SERVICE_HEALTHY

Description

Determines whether sufficient evidence exists to justify the claim that a service is healthy.

Required Evidence

* service_exists
* response_time
* failure_rate

---

Evidence Coverage Rules

A claim cannot be evaluated unless all required evidence has been collected and observed.

If any required evidence is missing:

Status:

INSUFFICIENT_EVIDENCE

Explanation:

Required evidence is missing or has not been observed.

---

Current Implementation

Collected from Dynatrace:

* service_exists

Not yet collected:

* response_time
* failure_rate

Result:

SERVICE_HEALTHY currently produces:

INSUFFICIENT_EVIDENCE

until metric collection is implemented.

---

Architecture Impact

Requirement
↓
Claim
↓
Required Evidence
↓
Evidence Coverage Evaluation
↓
Claim Assurance
↓
Requirement Assurance

## Phase 2A – Policy Agent Claim Discovery

### Purpose

Introduce policy-driven claim discovery.

Requirements are no longer mapped directly to claims by a human.

Instead, approved organizational policies are used to suggest candidate claims.

### Architecture

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Human Approval
↓
Approved Claims
↓
Evidence Collection
↓
Assurance Engine
↓
Requirement Assurance

### Responsibilities

Policy Agent

* Load approved organizational policies
* Interpret policy objectives
* Suggest candidate claims
* Attach policy references

Human Reviewer

* Approve claims
* Reject claims
* Define assurance scope

Assurance Engine

* Collect evidence
* Evaluate claims
* Determine assurance status

### Important Principles

Policy Agents:

* Suggest claims
* Provide traceability
* Provide rationale

Policy Agents do not:

* Approve claims
* Collect evidence
* Perform assurance

### Future Evolution

Current:

Deterministic Policy Agent

Future:

LLM-Assisted Policy Agent

The output contract remains unchanged:

Requirement
↓
Suggested Claims
↓
Policy References

## Phase 2B – Human Approval Workflow

### Purpose

Introduce a governance checkpoint between claim discovery and assurance execution.

Policy and standards agents may suggest claims, but suggested claims do not automatically become assurance scope.

A human reviewer must approve claims before evidence collection begins.

### Architecture

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Human Approval
↓
Approved Claims
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance

### Responsibilities

Policy Agent

* Suggest candidate claims
* Provide policy traceability
* Provide rationale

Human Reviewer

* Approve claims
* Reject claims
* Define assurance scope

Evidence Collection

* Collect evidence only for approved claims

Assurance Engine

* Evaluate evidence
* Determine claim status
* Determine requirement status

### Governance Principle

AI suggests.

Humans approve.

Evidence determines assurance.

### Future Evolution

Current

Human approval occurs through explicit claim selection.

Future

Dashboard approval workflow with:

* Claim review
* Claim approval
* Claim rejection
* Approval audit history

## Phase 2C – Dashboard Approval Workflow

### Purpose

Make claim approval visible and interactive through the dashboard.

Prior phases introduced:

* Policy Agent Claim Discovery
* Human Approval Workflow

Phase 2C exposes these capabilities through the user interface.

### Architecture

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Dashboard Approval
↓
Approved Claims
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Dashboard

### Dashboard Responsibilities

Display Requirements

* Requirement ID
* Requirement Title
* Requirement Description

Display Suggested Claims

* Claim ID
* Policy Reference
* Objective Reference
* Rationale

Support Human Approval

* Approve claims
* Reject claims
* Define assurance scope

Display Approved Claims

* Current assurance scope
* Approved claim list

Display Assurance Results

* Requirement assurance
* Claim assurance
* Evidence records
* Evidence gaps
* Assurance explanations

### Governance Principle

Policy Agents suggest claims.

Humans approve claims.

Only approved claims enter assurance scope.

### Future Evolution

Dashboard approval decisions will be persisted and auditable.

Future capabilities:

* Approval history
* Reviewer identity
* Approval timestamps
* Multi-stage approval workflows

## Phase 3A – Assurance Explanation Engine

### Purpose

Convert deterministic assurance results into human-readable explanations.

The Assurance Engine determines assurance outcomes.

The Assurance Explanation Engine explains those outcomes.

### Architecture

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Dashboard Approval
↓
Approved Claims
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation Engine
↓
Dashboard

### Responsibilities

Assurance Engine

* Evaluate evidence
* Determine claim status
* Determine requirement status

Assurance Explanation Engine

* Explain assurance outcomes
* Explain evidence gaps
* Explain failed claims
* Generate recommendations

### Important Principle

Explanation does not determine assurance.

Assurance remains evidence-based and deterministic.

Explanation consumes assurance outcomes and converts them into understandable narratives.

### Example

Assurance Result

PARTIALLY_ASSURED

Evidence Gaps

* response_time
* failure_rate

Explanation

The requirement is partially assured.

The service exists and is observable in operational reality.

However, service health cannot currently be assured because response time and failure rate evidence are unavailable.

### Future Evolution

Current

Deterministic explanation generation.

Future

LLM-assisted explanation generation.

The explanation contract remains unchanged.

## Phase 3B – Dashboard Assurance Explanation Integration

### Purpose

Expose assurance explanations directly in the dashboard.

Phase 3A introduced the Assurance Explanation Engine.

Phase 3B makes explanations visible to users.

### Architecture

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Dashboard Approval
↓
Approved Claims
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation Engine
↓
Dashboard Explanation Panel

### Responsibilities

Dashboard

* Display assurance status
* Display claim assurance
* Display evidence records
* Display assurance explanations
* Display recommendations

Assurance Explanation Engine

* Explain assurance outcomes
* Explain evidence gaps
* Explain failed claims
* Recommend next actions

### User Experience

Users can now see:

* Requirement status
* Claim status
* Evidence details
* Explanation summary
* Supporting details
* Recommended actions

### Governance Principle

Assurance remains deterministic.

Explanations provide interpretation only.

Explanations do not modify assurance outcomes.

## Knowledge Layer (Phase 4A)

Purpose:

Provide a centralized knowledge repository used by the future Gemini
Assurance Agent.

The knowledge layer stores:

- Organization Policies
- Standards
- Technical Documentation
- Claim Library
- Remediation Library

Technology:

- MongoDB Atlas

Current State:

- Seeded through seed_knowledge_base.py

Future State:

- Documents uploaded through Knowledge Management UI
- Automatic document ingestion
- Chunking
- Vector embeddings
- Atlas Vector Search

Relationship to Assurance:

Requirement
→ Knowledge Retrieval
→ Gemini Assurance Agent
→ Suggested Claims
→ Human Approval
→ Assurance
