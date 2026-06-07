"""
test_dynatrace_partner_mcp_client.py

Smoke test for hosted Dynatrace Partner MCP connectivity.

This validates:
- MCP initialize
- tools/list
- service entity lookup
- active problem query
- DQL generation
"""

import json

from dynatrace_partner_mcp_client import DynatracePartnerMCPClient


def print_section(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def pretty_print(data):
    print(json.dumps(data, indent=2)[:5000])


def main():
    client = DynatracePartnerMCPClient()

    print_section("MCP INITIALIZE")
    initialize_result = client.initialize()
    pretty_print(initialize_result)

    print_section("MCP TOOLS LIST")
    tools_result = client.list_tools()

    tools = tools_result.get("result", {}).get("tools", [])

    for tool in tools:
        print(f"- {tool.get('name')} :: {tool.get('title')}")

    print_section("FIND SERVICE ENTITY")
    service_result = client.find_service("easyTravel-Business")
    pretty_print(service_result)

    print_section("QUERY ACTIVE PROBLEMS")
    problems_result = client.query_active_problems(history="24h")
    pretty_print(problems_result)

    print_section("CREATE DQL FOR SERVICE HEALTH")
    dql_result = client.create_dql(
        "Get the average response time, failure rate, p95 latency, "
        "and p99 latency for the Dynatrace service easyTravel-Business "
        "for the last 2 hours."
    )
    pretty_print(dql_result)

    dql = (
        dql_result
        .get("result", {})
        .get("structuredContent", {})
        .get("dql")
    )

    if not dql:
        # Some MCP servers return tool payloads inside content.
        content = dql_result.get("result", {}).get("content", [])

        for item in content:
            text = item.get("text", "")

            if "fetch" in text or "timeseries" in text:
                dql = text
                break

    if dql:
        print_section("EXECUTE GENERATED DQL")
        execute_result = client.execute_dql(dql)
        pretty_print(execute_result)
    else:
        print_section("EXECUTE GENERATED DQL")
        print("No DQL found in create-dql response.")


if __name__ == "__main__":
    main()
