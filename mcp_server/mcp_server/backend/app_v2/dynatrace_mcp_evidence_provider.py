"""
dynatrace_mcp_evidence_provider.py

Evidence provider backed by the hosted Dynatrace Partner MCP server.

Purpose:
Convert real Dynatrace MCP tool responses into EvidenceRecord objects.

This is the real partner-MCP evidence path:

Approved Claim
    ↓
Required Evidence
    ↓
Dynatrace Partner MCP
    ↓
EvidenceRecord
    ↓
Claim Assurance Engine

Supported evidence:
- service_exists
- service_entity
- active_problems
- response_time
- failure_rate
- percentile_latency_p95
- percentile_latency_p99

Dependency metrics remain future scope.
"""

from statistics import mean

from dynatrace_partner_mcp_client import DynatracePartnerMCPClient
from evidence_records import EvidenceRecord


class DynatraceMCPEvidenceProvider:
    """
    Collects evidence through the hosted Dynatrace MCP server.

    This provider does not make assurance decisions.
    """

    def __init__(self):
        self.client = DynatracePartnerMCPClient()

    def collect_evidence(self, approved_claim):
        """
        Collect all evidence records required by an approved claim.
        """

        records = []

        for evidence_type in approved_claim.claim.evidence_required:
            records.append(
                self.collect_evidence_type(
                    approved_claim,
                    evidence_type,
                )
            )

        return records

    def collect_evidence_type(self, approved_claim, evidence_type: str):
        """
        Route evidence collection to the correct Dynatrace MCP tool.
        """

        if evidence_type in ["service_exists", "service_entity"]:
            return self._collect_service_entity(
                approved_claim,
                evidence_type,
            )

        if evidence_type == "active_problems":
            return self._collect_active_problems(
                approved_claim,
                evidence_type,
            )

        if evidence_type in [
            "response_time",
            "failure_rate",
            "percentile_latency_p95",
            "percentile_latency_p99",
        ]:
            return self._collect_service_health_metric(
                approved_claim,
                evidence_type,
            )

        return EvidenceRecord(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            evidence_type=evidence_type,
            source="dynatrace_partner_mcp",
            observed=False,
            value=None,
            details={
                "reason": "Evidence type not yet mapped to Dynatrace MCP.",
                "mcp_provider": "Dynatrace Hosted MCP Server",
            },
        )

    def _collect_service_entity(self, approved_claim, evidence_type: str):
        """
        Uses Dynatrace MCP tool:
        - get-entity-id
        """

        response = self.client.find_service(
            approved_claim.target_name
        )

        records = self._extract_records(response)

        observed = len(records) > 0

        value = records[0] if records else None

        if evidence_type == "service_exists":
            value = observed

        return EvidenceRecord(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            evidence_type=evidence_type,
            source="dynatrace_partner_mcp",
            observed=observed,
            value=value,
            details={
                "mcp_tool": "get-entity-id",
                "mcp_provider": "Dynatrace Hosted MCP Server",
                "records_returned": len(records),
                "records": records,
                "raw_response": response,
            },
        )

    def _collect_active_problems(self, approved_claim, evidence_type: str):
        """
        Uses Dynatrace MCP tool:
        - query-problems
        """

        response = self.client.query_active_problems(
            history="24h"
        )

        records = self._extract_records(response)

        active_records = [
            record
            for record in records
            if record.get("event.status") == "ACTIVE"
        ]

        return EvidenceRecord(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            evidence_type=evidence_type,
            source="dynatrace_partner_mcp",
            observed=True,
            value=len(active_records),
            details={
                "mcp_tool": "query-problems",
                "mcp_provider": "Dynatrace Hosted MCP Server",
                "active_problem_count": len(active_records),
                "active_problems": active_records,
                "raw_response": response,
            },
        )

    def _collect_service_health_metric(self, approved_claim, evidence_type: str):
        """
        Uses Dynatrace MCP tools:
        - create-dql
        - execute-dql

        The MCP server generates DQL and executes it against Grail.
        """

        dql_request = (
            "Get the average response time, failure rate, p95 latency, "
            "and p99 latency for the Dynatrace service "
            f"{approved_claim.target_name} for the last 2 hours."
        )

        dql_response = self.client.create_dql(dql_request)
        dql = self._extract_dql(dql_response)

        if not dql:
            return self._missing_metric_record(
                approved_claim=approved_claim,
                evidence_type=evidence_type,
                reason="Dynatrace MCP did not return a DQL query.",
                dql_response=dql_response,
                execute_response=None,
            )

        execute_response = self.client.execute_dql(dql)
        records = self._extract_records(execute_response)

        field_name = self._metric_field_name(evidence_type)

        value = self._extract_numeric_value(
            records=records,
            field_name=field_name,
        )

        observed = value is not None

        if not observed:
            return self._missing_metric_record(
                approved_claim=approved_claim,
                evidence_type=evidence_type,
                reason=(
                    f"Dynatrace MCP executed DQL but did not return "
                    f"a numeric value for {field_name}."
                ),
                dql_response=dql_response,
                execute_response=execute_response,
            )

        return EvidenceRecord(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            evidence_type=evidence_type,
            source="dynatrace_partner_mcp",
            observed=True,
            value=value,
            details={
                "mcp_tools": [
                    "create-dql",
                    "execute-dql",
                ],
                "mcp_provider": "Dynatrace Hosted MCP Server",
                "dql": dql,
                "field_name": field_name,
                "records": records,
                "dql_response": dql_response,
                "execute_response": execute_response,
            },
        )

    def _metric_field_name(self, evidence_type: str) -> str:
        mapping = {
            "response_time": "avg_response_time",
            "failure_rate": "failure_rate",
            "percentile_latency_p95": "p95_latency",
            "percentile_latency_p99": "p99_latency",
        }

        return mapping[evidence_type]

    def _extract_dql(self, response: dict) -> str | None:
        """
        Extract DQL from Dynatrace MCP create-dql response.
        """

        structured = (
            response
            .get("result", {})
            .get("structuredContent", {})
        )

        if structured.get("dql"):
            return structured["dql"]

        content = response.get("result", {}).get("content", [])

        for item in content:
            text = item.get("text", "")

            if "timeseries" in text or "fetch" in text:
                return text

        return None

    def _extract_records(self, response: dict) -> list[dict]:
        """
        Extract structured records from Dynatrace MCP response.
        """

        return (
            response
            .get("result", {})
            .get("structuredContent", {})
            .get("records", [])
        )

    def _extract_numeric_value(
        self,
        records: list[dict],
        field_name: str,
    ):
        """
        Extract a representative numeric value from Dynatrace DQL result.

        Dynatrace timeseries responses usually return arrays.
        We average non-null numeric values for the demo.
        """

        values = []

        for record in records:
            field_value = record.get(field_name)

            if isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, (int, float)):
                        values.append(item)

            elif isinstance(field_value, (int, float)):
                values.append(field_value)

        if not values:
            return None

        return mean(values)

    def _missing_metric_record(
        self,
        approved_claim,
        evidence_type: str,
        reason: str,
        dql_response: dict | None,
        execute_response: dict | None,
    ):
        return EvidenceRecord(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            evidence_type=evidence_type,
            source="dynatrace_partner_mcp",
            observed=False,
            value=None,
            details={
                "reason": reason,
                "mcp_provider": "Dynatrace Hosted MCP Server",
                "dql_response": dql_response,
                "execute_response": execute_response,
            },
        )
