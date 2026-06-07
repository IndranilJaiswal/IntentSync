"""
decision_assurance_agent.py

AI Decision Assurance Agent
===========================

Purpose
-------
This is the Google ADK / Agent Builder orchestration layer for the
AI Decision Assurance Platform.

The agent itself does not perform assurance.

Instead, it orchestrates MCP tools that implement the platform workflow.

Architecture
------------

Google ADK Agent (Gemini 3.1 Flash Lite)
            │
            ▼

    Assurance MCP Server
            │
            ├── discover_claims()
            └── map_claim()

            ▼

    Dynatrace MCP Server
            │
            ├── get_runtime_reality()
            ├── query_service_entity()
            ├── query_service_health_evidence()
            ├── query_active_problems()
            └── query_dependency_topology()

            ▼

    PML Governance Workflow
            │
            ▼

    Claim Assurance Engine
            │
            ▼

    Requirement Assurance

Reason → Plan → Act Mapping
---------------------------

Reason:
    discover_claims()

Plan:
    map_claim()

Act:
    query_service_health_evidence()
    query_service_entity()
    query_active_problems()
    query_dependency_topology()

Governance:
    Human-in-the-loop PML approval remains
    inside the dashboard workflow.

Important
---------
The agent MUST NOT:
- bypass PML governance
- approve claims automatically
- modify production systems
- declare assurance without evidence evaluation

The agent MAY:
- discover claims
- recommend mappings
- collect runtime evidence
- identify assurance gaps
- explain results
"""

from google.adk.agents import LlmAgent

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioServerParameters,
)

from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
)


# ============================================================
# MCP TOOLSET #1
#
# AI Decision Assurance MCP Server
#
# Exposes:
# - discover_claims()
# - map_claim()
#
# This is the Reason + Plan layer.
# ============================================================

assurance_mcp_tools = McpToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=[
            "backend/app_v2/assurance_mcp_server.py",
        ],
    )
)


# ============================================================
# MCP TOOLSET #2
#
# Dynatrace Observability MCP Server
#
# Exposes:
# - get_runtime_reality()
# - query_service_entity()
# - query_service_health_evidence()
# - query_active_problems()
# - query_dependency_topology()
#
# This is the Act layer.
# ============================================================

dynatrace_mcp_tools = McpToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=[
            "backend/app_v2/dynatrace_mcp_server.py",
        ],
    )
)


# ============================================================
# ROOT AGENT
#
# This is the Agent Builder / ADK entry point.
# ============================================================

root_agent = LlmAgent(
    name="ai_decision_assurance_agent",

    # Hackathon model
    model="gemini-3.1-flash-lite",

    description=(
        "AI Decision Assurance Agent that discovers assurance claims, "
        "maps them into governed assurance scope, and collects "
        "runtime evidence using MCP-connected observability tools."
    ),

    instruction="""
You are an AI Decision Assurance Agent.

Mission
-------
Assure business and technical requirements through a governed,
evidence-based workflow.

You must reason, plan, and act using MCP tools.

Workflow
========

STEP 1 - REASON

Use discover_claims()

Goal:
Discover assurance claims required to satisfy a requirement.

Examples:

"The service shall remain highly available"

may produce:

SERVICE_HEALTHY
SERVICE_RECOVERABLE
SERVICE_REDUNDANT


STEP 2 - PLAN

Use map_claim()

Goal:
Map discovered claims into governed executable claims.

Important:

Mapping recommendations are NOT approvals.

All mapped claims require PML approval before
they enter assurance scope.


STEP 3 - ACT

Use Dynatrace MCP tools.

Available tools:

query_service_entity()
query_service_health_evidence()
query_active_problems()
query_dependency_topology()
get_runtime_reality()

Goal:
Collect runtime evidence needed to support
governed assurance claims.


STEP 4 - GOVERNANCE

PML approval is mandatory.

You must never:

- approve claims
- approve mappings
- bypass governance

You may only recommend.


STEP 5 - ASSURANCE

Evidence alone is not assurance.

Runtime observations must be evaluated by
the Assurance Engine before a claim can be:

VERIFIED
FAILED
INSUFFICIENT_EVIDENCE


Output Requirements
===================

When responding:

1. Explain discovered claims.
2. Explain mapping recommendations.
3. Identify required PML approvals.
4. Summarize runtime evidence.
5. Identify assurance gaps.
6. Explain business impact.

Never claim assurance without evidence evaluation.

Never modify production systems.

Never bypass governance controls.
""",

    # ========================================================
    # MCP TOOLSETS AVAILABLE TO THE AGENT
    # ========================================================

    tools=[
        assurance_mcp_tools,
        dynatrace_mcp_tools,
    ],
)
