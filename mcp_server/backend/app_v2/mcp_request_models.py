"""
mcp_request_models.py

Purpose:
Define MCP evidence request models for the AI Decision Assurance Platform.

These models describe what the assurance agent needs from a partner MCP server,
without tying the platform to a specific vendor implementation.

Current Partner MCP Domain:
- Dynatrace Observability MCP

Design Principle:
Dynatrace MCP provides observability context.
The AI Decision Assurance Platform performs governance and assurance.
"""

from dataclasses import asdict, dataclass
from typing import List


@dataclass
class MCPEvidenceRequest:
    request_id: str
    intent: str
    target_name: str
    required_evidence: List[str]
    partner_domain: str
    partner_server: str
    requested_by_claim: str
    approval_context: str

    def to_dict(self) -> dict:
        return asdict(self)


class MCPEvidenceRequestBuilder:
    """
    Builds MCP evidence requests from approved governed claims.

    The builder does not call MCP tools.
    It creates structured requests that can be sent to a partner MCP server.
    """

    def build_requests_for_claim(
        self,
        claim_id: str,
        target_name: str,
        evidence_required: List[str],
    ) -> List[dict]:

        requests = []

        service_context_evidence = [
            evidence
            for evidence in evidence_required
            if evidence in [
                "service_exists",
                "service_entity",
            ]
        ]

        if service_context_evidence:
            requests.append(
                MCPEvidenceRequest(
                    request_id=f"MCP-REQ-{claim_id}-SERVICE-CONTEXT",
                    intent="service_context",
                    target_name=target_name,
                    required_evidence=service_context_evidence,
                    partner_domain="Observability MCP",
                    partner_server="Dynatrace MCP Server",
                    requested_by_claim=claim_id,
                    approval_context="PML_APPROVED_ASSURANCE_SCOPE",
                ).to_dict()
            )

        service_health_evidence = [
            evidence
            for evidence in evidence_required
            if evidence in [
                "response_time",
                "failure_rate",
                "active_problems",
            ]
        ]

        if service_health_evidence:
            requests.append(
                MCPEvidenceRequest(
                    request_id=f"MCP-REQ-{claim_id}-SERVICE-HEALTH",
                    intent="service_health",
                    target_name=target_name,
                    required_evidence=service_health_evidence,
                    partner_domain="Observability MCP",
                    partner_server="Dynatrace MCP Server",
                    requested_by_claim=claim_id,
                    approval_context="PML_APPROVED_ASSURANCE_SCOPE",
                ).to_dict()
            )

        latency_evidence = [
            evidence
            for evidence in evidence_required
            if evidence in [
                "percentile_latency_p95",
                "percentile_latency_p99",
            ]
        ]

        if latency_evidence:
            requests.append(
                MCPEvidenceRequest(
                    request_id=f"MCP-REQ-{claim_id}-LATENCY",
                    intent="latency_analysis",
                    target_name=target_name,
                    required_evidence=latency_evidence,
                    partner_domain="Observability MCP",
                    partner_server="Dynatrace MCP Server",
                    requested_by_claim=claim_id,
                    approval_context="PML_APPROVED_ASSURANCE_SCOPE",
                ).to_dict()
            )

        dependency_evidence = [
            evidence
            for evidence in evidence_required
            if evidence in [
                "dependency_entity",
                "dependency_call_success_rate",
                "dependency_response_time",
            ]
        ]

        if dependency_evidence:
            requests.append(
                MCPEvidenceRequest(
                    request_id=f"MCP-REQ-{claim_id}-DEPENDENCY",
                    intent="dependency_analysis",
                    target_name=target_name,
                    required_evidence=dependency_evidence,
                    partner_domain="Observability MCP",
                    partner_server="Dynatrace MCP Server",
                    requested_by_claim=claim_id,
                    approval_context="PML_APPROVED_ASSURANCE_SCOPE",
                ).to_dict()
            )

        return requests
