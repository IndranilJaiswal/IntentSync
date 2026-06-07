# Roadmap

## Phase 1A - Claim Assurance Core

Status: Complete

### Completed

- Claim Library
- Claim Models
- Capability Matrix
- Approved Claims
- Evidence Request Model
- Evidence Request Builder

### Outcome

The platform can transform approved claims into observable evidence requirements.

---

## Phase 1B - Evidence Collection

Status: In Progress

### Goal

Collect real evidence from Dynatrace.

### Deliverables

- Dynatrace Evidence Adapter
- Evidence Record Model
- Evidence Collection Engine

### First Supported Evidence Type

SERVICE_EXISTS

### Example Flow

Approved Claim:
SERVICE_EXISTS

Evidence Request:
service_exists

Reality Source:
Dynatrace

Evidence Record:
Service observed or not observed

## Phase 1B - Evidence Collection

Status: In Progress

### Completed

- Evidence Record Model
- Dynatrace Evidence Adapter
- Service Existence Evidence Collection

### In Progress

- Failure Rate Evidence
- Response Time Evidence
- Problem Evidence

### Remaining

- Evidence Collection Engine
- Assurance Integration
### Completed

- Runtime Reality Model
- Reality Provider Abstraction
Completed:

✓ RuntimeReality model

✓ RealityProvider abstraction

✓ Mock Dynatrace Provider

In Progress:

□ Real Dynatrace Provider

□ Evidence Collection Engine

□ Assurance Integration
### Completed

- RuntimeReality model
- RealityProvider abstraction
- MockDynatraceProvider

### In Progress

- Live Dynatrace Provider
- Evidence Collection Engine
- Assurance Integration
### Completed

- Live Dynatrace Client
- Live Dynatrace Provider
- SERVICE entity ingestion

### Remaining

- Container ingestion
- Host ingestion
- Dependency ingestion
- Metrics ingestion
### Completed

- Live Dynatrace Provider
- SERVICE entity ingestion
- Runtime Reality normalization
- Live SERVICE_EXISTS evidence test
### Completed

✓ Live Dynatrace Client

✓ Live Dynatrace Provider

✓ Runtime Reality Normalization

✓ SERVICE Entity Ingestion

✓ Live SERVICE_EXISTS Validation

### Next

□ SERVICE_HEALTHY

□ NO_ACTIVE_PROBLEMS

□ DEPENDENCY_EXISTS

□ Assurance Engine Integration
### Completed

✓ Evidence Collection Engine

✓ End-to-End Evidence Collection Flow

### Completed

✓ RuntimeReality model

✓ RealityProvider abstraction

✓ Live Dynatrace Provider

✓ SERVICE entity ingestion

✓ Runtime Reality normalization

✓ Live SERVICE_EXISTS validation

✓ Evidence Collection Engine

✓ End-to-End Evidence Collection Flow

### Remaining

□ Assurance Engine Integration

□ SERVICE_HEALTHY

□ NO_ACTIVE_PROBLEMS

□ DEPENDENCY_EXISTS


## Phase 1C - Requirement Assurance

Status: In Progress

### Completed

- Requirement model
- Requirement configuration
- Requirement loader
- Assurance result model
- Claim Assurance Engine v1
- SERVICE_EXISTS assurance evaluation

### Next

- Requirement assurance rollup
- SERVICE_HEALTHY assurance
- Dashboard v1

### Completed

- Requirement assurance rollup model
- Requirement assurance engine
- Multi-claim requirement evaluation

### Next

- Dashboard v1
- SERVICE_HEALTHY evidence expansion

### Completed

- Dashboard v1
- End-to-end requirement assurance visualization

### Next

- Improve visual layout
- Add SERVICE_HEALTHY metrics evidence
- Add requirement selection

## Completed

- Streamlit Dashboard v1
- Requirement assurance visualization
- Claim evidence visibility
- Assurance explanation visibility

## Next

- SERVICE_HEALTHY claim
- Response time evidence
- Failure rate evidence
- Evidence gap detection

## Completed

### Phase 1E

Service Health Assurance

Implemented:

* SERVICE_HEALTHY claim
* Evidence coverage evaluation
* Evidence gap detection
* Missing evidence reporting

Current Evidence Sources

Collected

* service_exists

Planned

* response_time
* failure_rate

---

## Next

### Phase 1F

Live Dynatrace Metrics

Objectives

* Collect response time metrics
* Collect failure rate metrics
* Evaluate metric thresholds
* Produce VERIFIED and FAILED health outcomes

Expected Outcome

SERVICE_HEALTHY will move from:

INSUFFICIENT_EVIDENCE

to:

VERIFIED

or

FAILED

## Completed

### Phase 2A – Policy Agent Claim Discovery

Implemented:

* Policy model
* Policy objective model
* Policy loader
* Availability Policy Agent
* Policy-based claim suggestions
* Policy traceability

Current Capability

Requirement
↓
Policy Agent
↓
Suggested Claims

Output includes:

* Claim ID
* Policy ID
* Policy Name
* Objective ID
* Objective Description

---

## Next

### Phase 2B – Human Approval Workflow

Objectives

* Review suggested claims
* Approve candidate claims
* Reject candidate claims
* Generate approved claim set

Expected Architecture

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

## Completed

### Phase 2B – Human Approval Workflow

Implemented

* Claim suggestion model
* Claim approval engine
* Approval workflow
* Approval traceability

Current Flow

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Human Approval
↓
Approved Claims

Output

Approved claims become assurance scope.

Rejected claims are excluded from evidence collection.

---

## Next

### Phase 2C – Dashboard Approval Workflow

Objectives

* Display suggested claims
* Select claims for approval
* Display approved claims
* Persist approval decisions

Expected Architecture

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

## Completed

### Phase 2C – Dashboard Approval Workflow

Implemented

* Suggested claim visualization
* Claim approval interface
* Assurance scope visibility
* Approved claim display
* Integrated assurance execution

Current Flow

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

Dashboard Features

* Requirement selection
* Claim review
* Claim approval
* Assurance execution
* Evidence visibility
* Assurance visibility

---

## Next

### Phase 3A – AI Assurance Explanation

Objectives

* Explain assurance outcomes
* Explain evidence gaps
* Explain failed claims
* Generate executive summaries

Expected Architecture

Requirement
↓
Policy Agent
↓
Human Approval
↓
Evidence
↓
Assurance
↓
AI Explanation
↓
Dashboard

## Completed

### Phase 3A – Assurance Explanation Engine

Implemented

* Assurance explanation model
* Assurance explanation engine
* Deterministic explanation generation
* Explanation recommendations

Current Flow

Requirement
↓
Policy Agent
↓
Human Approval
↓
Evidence
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation
↓
Dashboard

Current Capabilities

* Explain verified requirements
* Explain partially assured requirements
* Explain failed requirements
* Recommend next actions

---

## Next

### Phase 3B – Dashboard Explanation Integration

Objectives

* Display explanations in dashboard
* Display recommendations
* Display evidence gap reasoning

Expected Architecture

Requirement Assurance
↓
Assurance Explanation Engine
↓
Dashboard Explanation Panel

---

### Future

Phase 3C – LLM-Assisted Assurance Explanation

Objectives

* Executive summaries
* Business impact explanations
* Natural language recommendations
* Audience-specific explanations

## Completed

### Phase 3A – Assurance Explanation Engine

Implemented

* Assurance explanation model
* Assurance explanation engine
* Deterministic explanation generation
* Recommendation generation

Current Flow

Requirement
↓
Policy Agent
↓
Human Approval
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation
↓
Dashboard

Current Capabilities

* Explain verified requirements
* Explain partially assured requirements
* Explain failed requirements
* Explain evidence gaps
* Recommend next actions

---

## Next

### Phase 3B – Dashboard Explanation Integration

Objectives

* Display assurance explanations
* Display recommendations
* Display evidence gap reasoning

Expected Architecture

Requirement Assurance
↓
Assurance Explanation Engine
↓
Dashboard Explanation Panel

---

### Future

Phase 3C – Gemini Assurance Explanation

Objectives

* Executive summaries
* Business impact narratives
* Audience-specific explanations
* Natural language recommendations

## Completed

### Phase 3B – Dashboard Assurance Explanation Integration

Implemented

* Dashboard explanation panel
* Explanation summary display
* Explanation detail display
* Recommendation display

Current Flow

Requirement
↓
Policy Agent
↓
Human Approval
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation
↓
Dashboard

Current User Experience

Users can:

* Review requirement assurance
* Review claim assurance
* Review evidence records
* Review explanations
* Review recommendations

---

## Next

### Phase 4A – Standards Agent Framework

Objectives

* Introduce standards-based claim discovery
* Support IEC 62443 mappings
* Support NIST mappings
* Support ISO mappings

Expected Architecture

Requirement
↓
Policy Agent
↓
Standards Agents
↓
Claim Synthesis
↓
Human Approval
↓
Assurance

## Phase 4A – MongoDB Knowledge Base

Status: IN PROGRESS

Completed

✓ MongoDB Atlas provisioning
✓ MongoDB Atlas connectivity
✓ MongoDB client implementation
✓ Knowledge base schema
✓ Knowledge base seed script

Next

□ Knowledge retrieval layer
□ Atlas Vector Search
□ Gemini Assurance Agent
