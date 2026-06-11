
# 🎯 IntentSync

## Synchronizing Intent with Reality Through Continuous Assurance

IntentSync is an AI-powered Decision Assurance platform that continuously verifies whether operational reality satisfies business intent.

Built using Google Gemini, Google Cloud, Agent Builder-compatible MCP integrations, MongoDB, and Dynatrace.

Instead of asking:

> "What is happening?"

IntentSync answers:

> "Are we achieving the outcome we intended?"

---

# Problem

Organizations define requirements such as:

> The customer booking service must remain observable and healthy during runtime.

However, requirements, governance decisions, architecture, and runtime operations often become disconnected.

Monitoring tools answer:

* What happened?
* What is broken?
* What is the current state?

But they do not answer:

> Is the requirement actually being satisfied?

IntentSync closes that gap.

---

# Solution

IntentSync transforms:

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

# Google Cloud x Gemini Hackathon

IntentSync was built for the Google Cloud x Gemini Agent Builder Hackathon.

Challenge:

Build a functional agent powered by Gemini and Google Cloud Agent Builder that integrates a Partner MCP server to solve a real-world problem.

IntentSync demonstrates:

✅ Gemini reasoning

✅ Governance-aware AI workflows

✅ Agent Builder compatible MCP architecture

✅ Dynatrace Partner MCP integration

✅ Runtime evidence collection

✅ Explainable assurance outcomes

---

# Architecture

Requirement

↓

Gemini Claim Discovery

↓

Claim Review Package Generation

↓

Governance Approval

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

# Partner MCP Integration

IntentSync integrates with the Dynatrace Hosted MCP Server.

Evidence is collected through MCP tools including:

* get-entity-id
* query-problems
* create-dql
* execute-dql

Runtime evidence currently includes:

* Service existence
* Service health
* Active incidents
* Response time
* Failure rate
* P95 latency
* P99 latency

---

# Example Workflow

Requirement:

"The customer booking service must remain observable and healthy during runtime."

## Claim Discovery

IntentSync discovers:

* SERVICE_EXISTS
* SERVICE_HEALTHY
* SERVICE_OBSERVABLE

## Governance

Claims are reviewed and approved before entering assurance scope.

Example:

SERVICE_OBSERVABLE

↓

Governance Approved

↓

Capability Assessed

↓

Governed Claim Defined

## Runtime Evidence

Dynatrace MCP provides:

* Service inventory
* Runtime health
* Incident information
* Performance metrics

## Assurance

IntentSync produces:

* VERIFIED
* FAILED
* PARTIALLY_ASSURED
* INSUFFICIENT_EVIDENCE

results with explainable reasoning.

---

# Why This Is Different

Traditional Monitoring asks:

"What is happening?"

IntentSync asks:

"Is the intended outcome being achieved?"

This shifts operations from monitoring systems to assuring outcomes.

---

# Current Capabilities

* Requirement-to-Claim reasoning using Gemini
* Governance review package generation
* PML approval workflow
* Runtime evidence collection through MCP
* Dynatrace Partner MCP integration
* Explainable assurance outcomes
* Evidence-backed decision traceability

---

# Technology Stack

* Google Gemini
* Google Cloud Run
* Google Agent Builder Compatible MCP Services
* Dynatrace Hosted MCP
* MongoDB
* Python
* Streamlit

---

# Hosted Demo

Dashboard URL:

https://intentsync-demo-933962237463.us-central1.run.app

MCP URL:

https://intentsync-mcp-demo-933962237463.us-central1.run.app/mcp

---

# Open Source Repository

https://github.com/IndranilJaiswal/IntentSync

---

# Future Roadmap

* Dynamic evidence contract generation
* Autonomous capability discovery
* Multi-provider assurance
* Policy-as-code integration
* Continuous compliance assurance
* Portfolio-level assurance analytics

---

# License

Apache License 2.0

