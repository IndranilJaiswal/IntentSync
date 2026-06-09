from mcp_request_models import MCPEvidenceRequestBuilder


def main():
    builder = MCPEvidenceRequestBuilder()

    requests = builder.build_requests_for_claim(
        claim_id="SERVICE_HEALTHY",
        target_name="easyTravel-Business",
        evidence_required=[
            "service_entity",
            "response_time",
            "failure_rate",
            "active_problems",
        ],
    )

    print("\n==============================")
    print("MCP EVIDENCE REQUESTS")
    print("==============================\n")

    for request in requests:
        print(request)


if __name__ == "__main__":
    main()
