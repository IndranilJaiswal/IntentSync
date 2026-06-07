"""
dynatrace_partner_mcp_client.py

Client for the hosted Dynatrace Partner MCP server.

Purpose:
Call the real Dynatrace MCP endpoint exposed by Dynatrace:

https://{environment}.apps.dynatrace.com/platform-reserved/mcp-gateway/v0.1/servers/dynatrace-mcp/mcp

This client is intentionally low-level.

It knows:
- MCP endpoint
- Bearer token auth
- JSON-RPC protocol
- Tool invocation

It does NOT know:
- Claim assurance logic
- PML governance logic
- Dashboard logic
"""

import json
import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


class DynatracePartnerMCPClient:
    """Client for calling the hosted Dynatrace MCP server."""

    def __init__(self):
        self.url = os.getenv("DYNATRACE_MCP_URL")
        self.token = os.getenv("DYNATRACE_PLATFORM_TOKEN")

        if not self.url:
            raise ValueError("DYNATRACE_MCP_URL is not set.")

        if not self.token:
            raise ValueError("DYNATRACE_PLATFORM_TOKEN is not set.")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        self.request_id = 0

    def _next_id(self) -> int:
        self.request_id += 1
        return self.request_id

    def _post_jsonrpc(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> dict:
        """Send one JSON-RPC request to the Dynatrace MCP endpoint."""

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
        }

        if params is not None:
            payload["params"] = params

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return self._parse_response(response)

    def _parse_response(self, response: requests.Response) -> dict:
        """
        Parse a Dynatrace MCP response.

        The hosted MCP endpoint usually returns JSON, but MCP-compatible
        transports may also return text/event-stream. This method supports both.
        """

        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            return response.json()

        text = response.text.strip()

        if not text:
            return {}

        # Basic SSE parsing fallback.
        # Expected lines may look like:
        # data: {"jsonrpc":"2.0", ...}
        for line in text.splitlines():
            line = line.strip()

            if line.startswith("data:"):
                data = line.replace("data:", "", 1).strip()

                if data and data != "[DONE]":
                    return json.loads(data)

        # Last fallback: try raw JSON.
        return json.loads(text)

    def initialize(self) -> dict:
        """Initialize the MCP session."""

        return self._post_jsonrpc(
            method="initialize",
            params={
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "ai-decision-assurance-platform",
                    "version": "0.1.0",
                },
            },
        )

    def list_tools(self) -> dict:
        """List tools exposed by the hosted Dynatrace MCP server."""

        return self._post_jsonrpc(
            method="tools/list",
            params={},
        )

    def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict:
        """Call a Dynatrace MCP tool."""

        return self._post_jsonrpc(
            method="tools/call",
            params={
                "name": tool_name,
                "arguments": arguments,
            },
        )

    # ---------------------------------------------------------------------
    # Convenience wrappers for assurance evidence discovery
    # ---------------------------------------------------------------------

    def find_service(
        self,
        service_name: str,
    ) -> dict:
        """
        Find Dynatrace service entity by name.

        Maps to assurance evidence:
        - service_entity
        - service_exists
        """

        return self.call_tool(
            "get-entity-id",
            {
                "entityType": "dt.entity.service",
                "entityNameFilter": service_name,
                "includeTypes": True,
            },
        )

    def query_active_problems(
        self,
        history: str = "24h",
    ) -> dict:
        """
        Query active Davis problems.

        Maps to assurance evidence:
        - active_problems
        """

        return self.call_tool(
            "query-problems",
            {
                "status": "ACTIVE",
                "history": history,
                "includeTypes": True,
            },
        )

    def create_dql(
        self,
        request: str,
    ) -> dict:
        """
        Ask Dynatrace MCP to generate DQL from a natural language request.

        Used for:
        - response_time
        - failure_rate
        - p95 latency
        - p99 latency
        - dependency evidence
        """

        return self.call_tool(
            "create-dql",
            {
                "request": request,
            },
        )

    def execute_dql(
        self,
        dql_query: str,
    ) -> dict:
        """Execute a DQL query through Dynatrace MCP."""

        return self.call_tool(
            "execute-dql",
            {
                "dqlQueryString": dql_query,
                "includeTypes": True,
            },
        )

    def ask_docs(
        self,
        prompt: str,
    ) -> dict:
        """Ask Dynatrace docs through the hosted MCP server."""

        return self.call_tool(
            "ask-dynatrace-docs",
            {
                "prompt": prompt,
            },
        )
