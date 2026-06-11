# 🎯 IntentSync

## Synchronizing Intent with Reality Through Continuous Assurance

IntentSync is an AI-powered Decision Assurance platform that continuously verifies whether operational reality satisfies business intent.

Built using Google Gemini, Google Cloud, Agent Builder-compatible MCP integrations, MongoDB, and Dynatrace.

Instead of asking:

> What is happening?

IntentSync answers:

> Are we achieving the outcome we intended?

---

## Problem

Organizations define requirements such as:

> The customer booking service must remain observable and healthy during runtime.

Monitoring tools provide metrics, logs, and alerts.

However, they cannot directly answer:

> Is the requirement actually being satisfied?

IntentSync closes that gap.

---

## Solution

Requirement

↓

Claims

↓

Governance

↓

Evidence

↓

Assurance

The platform converts human intent into executable assurance workflows backed by runtime evidence.

---

## Google Cloud x Gemini Hackathon

IntentSync demonstrates:

- Gemini reasoning
- Governance-aware AI workflows
- Agent Builder compatible MCP architecture
- Dynatrace Partner MCP integration
- Runtime evidence collection
- Explainable assurance outcomes

---

## Architecture

Requirement

↓

Gemini Claim Discovery

↓

Governance Review

↓

Capability Validation

↓

Partner MCP Evidence Collection

↓

Claim Assurance

↓

Requirement Assurance

↓

Assurance Explanation

---

## Partner MCP Integration

Dynatrace Hosted MCP provides:

- Service existence
- Service health
- Active incidents
- Response time
- Failure rate
- P95 latency
- P99 latency

MCP tools used:

- get-entity-id
- query-problems
- create-dql
- execute-dql

---

## Example Workflow

Requirement:

"The customer booking service must remain observable and healthy during runtime."

Discovered Claims:

- SERVICE_EXISTS
- SERVICE_HEALTHY
- SERVICE_OBSERVABLE

Governance Outcome:

- SERVICE_EXISTS → Executable
- SERVICE_HEALTHY → Executable
- SERVICE_OBSERVABLE → Governed Claim Defined

Runtime Evidence:

- Dynatrace runtime telemetry
- Service inventory
- Active incidents
- Performance metrics

Assurance Outcomes:

- VERIFIED
- FAILED
- PARTIALLY_ASSURED
- INSUFFICIENT_EVIDENCE

---

## Technology Stack

- Google Gemini
- Google Cloud Run
- Agent Builder Compatible MCP Services
- Dynatrace Hosted MCP
- MongoDB Atlas
- Python
- Streamlit

---

## Hosted Demo

Dashboard:

https://intentsync-demo-933962237463.us-central1.run.app


---

## Open Source License

Apache License 2.0

