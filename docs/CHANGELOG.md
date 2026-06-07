# Changelog

## Version 0.7.0 - Gemini Reason → Plan → Govern → Act Architecture

### Overview

The AI Decision Assurance Platform has evolved from a recommendation engine into a governed assurance platform with explicit Reason, Plan, Govern, Act, and Assure layers.

---

### Gemini Reasoning Layer

Implemented Gemini-powered claim discovery.

Capabilities:

* Requirement analysis
* Assurance claim discovery
* Business impact explanation
* Coverage gap identification

Output:

* Discovered assurance claims
* Claim rationale
* Business impact statements

---

### Gemini Planning Layer

Implemented governed claim mapping.

Capabilities:

* Claim-to-library mapping
* Existing executable claim reuse
* Coverage gap identification
* Human approval workflow preparation

Output:

* Approved executable claims
* Coverage gaps
* Mapping recommendations

---

### PML Governance Layer

Implemented human-in-the-loop governance.

Capabilities:

* PML claim review
* Mapping approval
* Executable claim approval
* Coverage gap tracking

Output:

* Governed assurance scope
* Approved claims
* Blocked claims
* Coverage gap backlog

---

### Dynatrace Runtime Evidence

Integrated Dynatrace runtime evidence collection.

Capabilities:

* Service entity discovery
* Active problem retrieval
* Runtime reality normalization

Evidence Types Currently Supported:

* service_exists
* service_entity
* active_problems

Known Constraints:

* Metrics API access currently unavailable due to Dynatrace API permissions.
* Response time, failure rate, and latency metrics remain capability gaps until metrics.read access is available.

---

### Claim Assurance Engine

Implemented executable claim evaluation.

Capabilities:

* Evidence gap detection
* Claim evaluation
* Confidence scoring
* Assurance status generation

Statuses:

* VERIFIED
* FAILED
* INSUFFICIENT_EVIDENCE

---

### MCP Strategy

Implemented partner MCP architecture.

Current Partner Domain:

* Dynatrace Observability MCP

Capabilities:

* Service context requests
* Service health requests
* Latency analysis requests
* Dependency analysis requests

Purpose:

The platform translates governed assurance requirements into partner MCP evidence requests.

---

### Google ADK Agent

Implemented Gemini 3.1 Flash Lite orchestration layer.

Workflow:

Reason:
Discover claims

Plan:
Map claims

Govern:
PML approval

Act:
Partner MCP evidence requests

Assure:
Evidence evaluation

Explain:
Dashboard and assurance outputs

---

### New Files

backend/app_v2/mcp_request_models.py

backend/app_v2/test_mcp_request_models.py

agent_builder/decision_assurance_agent.py

backend/app_v2/assurance_mcp_server.py

backend/app_v2/dynatrace_mcp_server.py

---

### Architecture Status

Core Platform:
Complete

Reasoning:
Complete

Planning:
Complete

Governance:
Complete

Evidence Collection:
Partial

Assurance:
Complete

MCP Strategy:
Complete

Partner MCP Integration:
In Progress

Google Cloud Agent Builder Deployment:
Pending

cat > docs/CHANGELOG.md <<'EOF'
# Changelog

## 0.8.0 - Hosted Dynatrace Partner MCP Integration

### Added
- Added hosted Dynatrace Partner MCP connectivity.
- Added `dynatrace_partner_mcp_client.py`.
- Added `dynatrace_mcp_evidence_provider.py`.
- Added MCP evidence request models.
- Added Google ADK agent wrapper using `gemini-3.1-flash-lite`.
- Added MCP server discovery and hosted MCP validation flow.

### Verified
- Dynatrace MCP `initialize` succeeds.
- Dynatrace MCP `tools/list` succeeds.
- Dynatrace MCP exposes tools including:
  - `get-entity-id`
  - `query-problems`
  - `create-dql`
  - `execute-dql`
  - `explain-dql`
  - anomaly and forecasting tools
- `get-entity-id` returns `easyTravel-Business` service entities.
- `query-problems` returns active Davis problems.
- `create-dql` generates DQL for service health metrics.
- `execute-dql` returns service response time, failure count, p95 latency, and p99 latency time series.

### Architecture Update
The evidence path now moves from local Dynatrace REST adapter toward hosted Dynatrace Partner MCP:

Requirement  
→ Gemini claim discovery  
→ Gemini/PML claim mapping  
→ PML approval  
→ Dynatrace Partner MCP evidence request  
→ EvidenceRecord normalization  
→ Claim assurance  
→ Requirement assurance  
→ Dashboard explanation

### Known Issues
- Dashboard run-assurance integration still needs final validation with `DynatraceMCPEvidenceProvider`.
- Some legacy REST-based Dynatrace files remain and should be marked legacy or archived during cleanup.
- Cloud deployment is pending.
EOF

## Dashboard Refactor – AI Systems Assurance Platform

### Platform Rename

* Renamed platform from "AI Decision Assurance Platform" to "AI Systems Assurance Platform".
* Shifted platform focus from individual assurance decisions to end-to-end system assurance.

### Dashboard Simplification

* Removed AI Decision Trace section.
* Reduced dashboard clutter and improved executive readability.
* Reorganized workflow around the assurance lifecycle.

### Coverage Assessment Improvements

* Converted claim assessment cards into collapsible sections.
* Improved visibility of supported claims, mapping candidates, and coverage gaps.
* Reduced vertical scrolling for large claim sets.

### PML Review Improvements

* Renamed "PML Governance Review" to "PML Review".
* Converted PML Review into a collapsible section.
* Simplified governance workflow presentation.

### Assurance Scope Simplification

* Removed duplicate "Current Governed Assurance Scope" section.
* Consolidated approval and assurance scope information into Coverage Assessment and PML Review.
* Eliminated redundant metrics.

### Evidence Collection Improvements

* Renamed "Evidence Plane" to "Evidence Collection".
* Clarified Dynatrace Partner MCP role in evidence gathering.
* Removed unnecessary MCP status and tool catalog loading from dashboard refresh path.

### System-Centric Dashboard Design

* Introduced system-oriented assurance model.
* Added foundation for multi-system support.
* Prepared dashboard structure for future system tabs.

### Assurance Reporting Enhancements

* Added executive-style assurance summary.
* Introduced assurance scorecard concepts:

  * Assurance Score
  * Claim Assurance Coverage
  * Evidence Coverage
  * Confidence Band
* Improved assurance explanation structure.

### User Experience Improvements

* Reduced dashboard complexity.
* Improved readability for judges and executives.
* Better alignment with:
  System → Requirements → Claims → Evidence → Assurance.

### Strategic Direction

This refactor transitions the platform from a technical assurance workflow prototype toward a scalable AI Systems Assurance Platform capable of supporting multiple systems, governed assurance workflows, and partner MCP-based evidence collection.
## v0.1.0 - IntentSync Production Baseline

### Platform Evolution

* Renamed platform from AI Decision Assurance Platform to IntentSync
* Introduced AI Systems Assurance Platform positioning
* Established IntentSync product branding

### Deployment

* Created dedicated IntentSync repository
* Deployed production instance to Google Cloud Run
* Integrated MongoDB Atlas knowledge base
* Integrated Dynatrace Partner MCP evidence collection

### Assurance Workflow

* Gemini Claim Discovery operational
* PML Review workflow operational
* Runtime evidence collection operational
* Assurance evaluation operational
* Assurance explanation operational

### Production Validation

Verified end-to-end workflow:

Requirement
→ Claims
→ Governance
→ Evidence
→ Assurance

### Release Status

Production Baseline Established
Version: v0.1.0
