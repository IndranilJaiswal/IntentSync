"""
IntentSync Dashboard

Synchronizing Intent with Reality Through Continuous Assurance.

Visible flow:

Requirement
↓
Claim Discovery
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
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "backend" / "app_v2"
sys.path.append(str(APP_DIR))


from assurance_explanation_engine import AssuranceExplanationEngine
from claim_assurance_engine import ClaimAssuranceEngine
from claim_discovery_agent import ClaimDiscoveryAgent
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_mcp_evidence_provider import DynatraceMCPEvidenceProvider
from dynatrace_partner_mcp_client import DynatracePartnerMCPClient
from pml_claim_mapping_agent import PMLClaimMappingAgent
from pml_governance_router import route_claim_review_package
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


st.set_page_config(
    page_title="IntentSync",
    layout="wide",
)

st.title("🎯 IntentSync")
st.caption(
    "Synchronizing Intent with Reality Through Continuous Assurance"
)

st.info(
    "Requirement → Claims → Governance → Evidence → Assurance"
)

st.markdown(
    """
### Transform Requirements into Assured Outcomes

IntentSync uses Gemini and Partner MCP integrations to discover assurance claims,
route them through governance, collect runtime evidence, and continuously assure
whether business intent is being satisfied.

**Built with:** Google Gemini • Google Cloud Run • Agent Builder MCP • Dynatrace MCP
"""
)


@dataclass
class DashboardClaimReviewPackage:
    claim_id: str
    category: str
    coverage_status: str


def status_badge(status: str) -> str:
    if status == "VERIFIED":
        return "✅ VERIFIED"
    if status == "PARTIALLY_ASSURED":
        return "⚠️ PARTIALLY ASSURED"
    if status == "FAILED":
        return "❌ FAILED"
    if status == "INSUFFICIENT_EVIDENCE":
        return "⚠️ INSUFFICIENT EVIDENCE"
    return status


def coverage_badge(status: str) -> str:
    if status == "SUPPORTED":
        return "✅ SUPPORTED"
    if status == "MAPPING_CANDIDATE":
        return "🧭 MAPPING CANDIDATE"
    if status == "COVERAGE_GAP":
        return "⚠️ COVERAGE GAP"
    return status


def governance_action_label(coverage_status: str) -> str:
    if coverage_status == "SUPPORTED":
        return "Approve for assurance"
    if coverage_status == "MAPPING_CANDIDATE":
        return "Approve mapping"
    if coverage_status == "COVERAGE_GAP":
        return "Classify / reject / defer"
    return "Manual review"


def get_claim_by_id(claims, claim_id):
    return next(claim for claim in claims if claim.claim_id == claim_id)


def build_claim_library_index(claims):
    return {claim.claim_id for claim in claims}


def calculate_coverage_score(assessed_claims) -> int:
    if not assessed_claims:
        return 0

    supported = [
        item
        for item in assessed_claims
        if item["coverage_status"] in ["SUPPORTED", "MAPPING_CANDIDATE"]
    ]

    return round((len(supported) / len(assessed_claims)) * 100)

def calculate_assurance_metrics(requirement_result, evidence_by_claim):
    """
    Calculate executive assurance metrics.

    Scoring model:
    - 60% claim assurance
    - 40% evidence coverage
    """

    claim_results = requirement_result.claim_results

    total_claims = len(claim_results)
    verified_claims = requirement_result.verified_claims
    failed_claims = requirement_result.failed_claims
    insufficient_claims = requirement_result.insufficient_claims

    evidence_records = []

    for records in evidence_by_claim.values():
        evidence_records.extend(records)

    total_evidence = len(evidence_records)

    observed_evidence = len(
        [
            evidence
            for evidence in evidence_records
            if evidence.observed is True
        ]
    )

    claim_score = (
        round((verified_claims / total_claims) * 100)
        if total_claims
        else 0
    )

    evidence_score = (
        round((observed_evidence / total_evidence) * 100)
        if total_evidence
        else 0
    )

    assurance_score = round(
        (claim_score * 0.6) + (evidence_score * 0.4)
    )

    if assurance_score >= 90 and failed_claims == 0 and insufficient_claims == 0:
        assurance_band = "HIGH"
    elif assurance_score >= 70 and failed_claims == 0:
        assurance_band = "MEDIUM"
    else:
        assurance_band = "LOW"

    return {
        "assurance_score": assurance_score,
        "assurance_band": assurance_band,
        "claim_score": claim_score,
        "evidence_score": evidence_score,
        "total_claims": total_claims,
        "verified_claims": verified_claims,
        "failed_claims": failed_claims,
        "insufficient_claims": insufficient_claims,
        "total_evidence": total_evidence,
        "observed_evidence": observed_evidence,
        "missing_evidence": total_evidence - observed_evidence,
    }


def render_assurance_scorecard(requirement_result, evidence_by_claim):
    """
    Render an executive assurance scorecard.
    """

    metrics = calculate_assurance_metrics(
        requirement_result=requirement_result,
        evidence_by_claim=evidence_by_claim,
    )

    st.markdown("### Assurance Scorecard")

    score_col1, score_col2, score_col3, score_col4 = st.columns(4)

    score_col1.metric(
        "Assurance Score",
        f"{metrics['assurance_score']}%",
    )

    score_col2.metric(
        "Claim Assurance",
        f"{metrics['claim_score']}%",
        f"{metrics['verified_claims']}/{metrics['total_claims']} verified",
    )

    score_col3.metric(
        "Evidence Coverage",
        f"{metrics['evidence_score']}%",
        (
            f"{metrics['observed_evidence']}/"
            f"{metrics['total_evidence']} observed"
        ),
    )

    score_col4.metric(
        "Confidence Band",
        metrics["assurance_band"],
    )

    if metrics["assurance_score"] >= 90:
        st.success(
            "High assurance achieved. Approved claims are supported by "
            "observed partner MCP evidence."
        )
    elif metrics["assurance_score"] >= 70:
        st.warning(
            "Partial assurance achieved. The requirement has meaningful "
            "evidence support, but some claims or evidence items still need "
            "attention."
        )
    else:
        st.error(
            "Low assurance. The requirement is not sufficiently supported by "
            "verified claims and observed evidence."
        )

    return metrics




@st.cache_data(ttl=60)
def recommend_pml_mapping(discovered_claim: str, governed_claims: list[str]):
    agent = PMLClaimMappingAgent()
    return agent.recommend_mapping(
        discovered_claim=discovered_claim,
        governed_claims=governed_claims,
    )


def assess_claim_coverage(suggestions, claim_library_ids):
    """
    Preserve two identities:
    - discovered_claim_id: Gemini output
    - governed_claim_id: executable claim library target

    The evidence engine only receives governed_claim_id.
    """

    assessed_claims = []
    governed_claims = list(claim_library_ids)

    for suggestion in suggestions:
        discovered_claim_id = suggestion.claim_id
        direct_match = discovered_claim_id in claim_library_ids

        mapping_recommendation = None
        governed_claim_id = discovered_claim_id
        mapping_status = "NOT_REQUIRED"

        if direct_match:
            coverage_status = "SUPPORTED"
        else:
            mapping_recommendation = recommend_pml_mapping(
                discovered_claim=discovered_claim_id,
                governed_claims=governed_claims,
            )

            candidate_mapping = mapping_recommendation.get("mapped_claim")
            confidence = mapping_recommendation.get("confidence", 0.0)

            if candidate_mapping in claim_library_ids and confidence >= 0.7:
                governed_claim_id = candidate_mapping
                coverage_status = "MAPPING_CANDIDATE"
                mapping_status = "PML_APPROVAL_REQUIRED"
            else:
                coverage_status = "COVERAGE_GAP"
                mapping_status = "NO_MAPPING_FOUND"

        route_status = (
            "SUPPORTED"
            if coverage_status in ["SUPPORTED", "MAPPING_CANDIDATE"]
            else "COVERAGE_GAP"
        )

        package = DashboardClaimReviewPackage(
            claim_id=governed_claim_id,
            category="Availability",
            coverage_status=route_status,
        )

        governance_route = route_claim_review_package(package)

        assessed_claims.append(
            {
                "suggestion": suggestion,
                "claim_id": governed_claim_id,
                "discovered_claim_id": discovered_claim_id,
                "governed_claim_id": governed_claim_id,
                "mapped_from": (
                    discovered_claim_id
                    if discovered_claim_id != governed_claim_id
                    else None
                ),
                "coverage_status": coverage_status,
                "route_status": route_status,
                "governance_route": governance_route,
                "mapping_status": mapping_status,
                "mapping_recommendation": mapping_recommendation,
                "source_type": "GEMINI_DISCOVERED_CLAIM",
            }
        )

    return assessed_claims


def add_existing_executable_claims(
    assessed_claims,
    selected_requirement,
    claim_library_ids,
):
    existing_governed_claim_ids = {
        item["governed_claim_id"]
        for item in assessed_claims
    }

    for claim_id in selected_requirement.claim_ids:
        if claim_id not in existing_governed_claim_ids and claim_id in claim_library_ids:

            suggestion = type(
                "ExistingExecutableClaimSuggestion",
                (),
                {
                    "claim_id": claim_id,
                    "policy_id": "CLAIM_LIBRARY",
                    "policy_name": "Existing Governed Claim Library",
                    "objective_id": "EXECUTABLE_ASSURANCE_SCOPE",
                    "objective_description": (
                        "Existing approved claim already available in the "
                        "governed executable claim library."
                    ),
                    "requirement": selected_requirement.description,
                    "rationale": (
                        "This claim is part of the existing governed assurance "
                        "scope for the selected requirement."
                    ),
                    "business_impact": (
                        "If this claim is not assured, the requirement may "
                        "not be fully supported by runtime evidence."
                    ),
                    "governance_need": (
                        "PML may approve this existing claim for evidence "
                        "collection and assurance evaluation."
                    ),
                },
            )()

            package = DashboardClaimReviewPackage(
                claim_id=claim_id,
                category="Availability",
                coverage_status="SUPPORTED",
            )

            governance_route = route_claim_review_package(package)

            assessed_claims.append(
                {
                    "suggestion": suggestion,
                    "claim_id": claim_id,
                    "discovered_claim_id": claim_id,
                    "governed_claim_id": claim_id,
                    "mapped_from": None,
                    "coverage_status": "SUPPORTED",
                    "route_status": "SUPPORTED",
                    "governance_route": governance_route,
                    "mapping_status": "NOT_REQUIRED",
                    "mapping_recommendation": None,
                    "source_type": "EXISTING_EXECUTABLE_CLAIM",
                }
            )

    return assessed_claims


def render_ai_explanation(suggestion):
    st.markdown("#### AI Explanation")

    st.write(
        "**Rationale:** "
        + getattr(suggestion, "rationale", suggestion.objective_description)
    )

    st.write(
        "**Business Impact:** "
        + getattr(
            suggestion,
            "business_impact",
            "If this claim is not assured, the requirement may not be fully "
            "supported by observable evidence.",
        )
    )

    st.write(
        "**Governance Need:** "
        + getattr(
            suggestion,
            "governance_need",
            "PML must classify this claim before execution.",
        )
    )


def render_ai_decision_trace(
    selected_requirement,
    assessed_claims,
    approved_claim_ids,
):
    existing_claims = [
        item
        for item in assessed_claims
        if item.get("source_type") == "EXISTING_EXECUTABLE_CLAIM"
    ]

    gemini_claims = [
        item
        for item in assessed_claims
        if item.get("source_type") == "GEMINI_DISCOVERED_CLAIM"
    ]

    supported_claims = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "SUPPORTED"
    ]

    mapping_candidates = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "MAPPING_CANDIDATE"
    ]

    coverage_gaps = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "COVERAGE_GAP"
    ]

    st.markdown("## Intent Resolution Trace")

    reason_col, plan_col, act_col = st.columns(3)

    with reason_col:
        st.subheader("Reason")
        st.write(
            "Gemini reasons over the requirement and known claim patterns "
            "to identify what must be assured."
        )
        st.metric("Gemini Claims", len(gemini_claims))
        st.metric("Existing Executable Claims", len(existing_claims))

    with plan_col:
        st.subheader("Plan")
        st.write(
            "IntentSync plans assurance by separating executable claims, "
            "mapping candidates, and coverage gaps."
        )
        st.metric("Supported Claims", len(supported_claims))
        st.metric("Mapping Candidates", len(mapping_candidates))
        st.metric("Coverage Gaps", len(coverage_gaps))

    with act_col:
        st.subheader("Act")
        st.write(
            "IntentSync acts through the hosted Dynatrace Partner MCP "
            "server after governed claims enter assurance scope."
        )
        st.metric("Approved for Evidence", len(approved_claim_ids))
        st.write("Dynatrace MCP evidence is requested only for approved claims.")


def render_governed_assurance_scope(
    approved_governed_claim_ids,
    assessed_claims,
):
    st.markdown("### Approved Claim Details")

    if not approved_governed_claim_ids:
        st.warning("No supported claims approved yet.")
        return

    approved_items = [
        item
        for item in assessed_claims
        if item["governed_claim_id"] in approved_governed_claim_ids
    ]

    if not approved_items:
        st.warning(
            "Approved claim IDs exist, but none match the currently assessed "
            "claims."
        )
        return

    for item in approved_items:
        suggestion = item["suggestion"]

        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            col1.write(
                f"**Discovered Claim:** `{item['discovered_claim_id']}`"
            )
            col2.write(
                f"**Governed Claim:** `{item['governed_claim_id']}`"
            )
            col3.write(
                f"**Coverage:** {coverage_badge(item['coverage_status'])}"
            )

            st.write(f"**Route:** `{item['governance_route']}`")
            st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

            if item.get("mapped_from"):
                mapping = item.get("mapping_recommendation") or {}

                st.info(
                    f"PML mapping approved for assurance scope. "
                    f"`{item['mapped_from']}` is normalized into "
                    f"`{item['governed_claim_id']}`."
                )

                st.write(
                    "**Mapping Confidence:** "
                    + str(mapping.get("confidence", "N/A"))
                )

                st.write(
                    "**Mapping Rationale:** "
                    + mapping.get("rationale", "No rationale provided.")
                )

            st.write(f"**Discovery Source:** {suggestion.policy_name}")
            st.write(f"**Objective:** `{suggestion.objective_id}`")

            render_ai_explanation(suggestion)

            st.markdown("#### Partner MCP Evidence Handoff")
            st.success(
                "Approved for evidence collection. The platform will request "
                "evidence from the hosted Dynatrace Partner MCP server for "
                f"governed claim `{item['governed_claim_id']}`."
            )


@st.cache_data(ttl=60)
def load_dynatrace_mcp_status():
    """
    Validate connectivity to the hosted Dynatrace Partner MCP server.

    This is not an assurance decision.
    It only confirms that the partner MCP server can be initialized and that
    tools are available for evidence retrieval.
    """

    client = DynatracePartnerMCPClient()

    initialize_result = client.initialize()
    tools_result = client.list_tools()

    tools = tools_result.get("result", {}).get("tools", [])

    return {
        "initialize": initialize_result,
        "tool_count": len(tools),
        "tools": [
            {
                "name": tool.get("name"),
                "title": tool.get("title"),
            }
            for tool in tools
        ],
    }


@st.cache_data(ttl=60)
def discover_claims_with_gemini(requirement_text: str):
    agent = ClaimDiscoveryAgent()
    return agent.discover(requirement_text)


def build_fallback_suggestions(selected_requirement):
    suggestions = []

    for claim_id in selected_requirement.claim_ids:
        suggestion = type(
            "FallbackClaimSuggestion",
            (),
            {
                "claim_id": claim_id,
                "policy_id": "FALLBACK",
                "policy_name": "Requirement Claim Mapping",
                "objective_id": "REQUIREMENT_DEFAULT",
                "objective_description": (
                    "Fallback claim from requirement configuration."
                ),
                "requirement": selected_requirement.description,
                "rationale": (
                    "Fallback claim mapped from requirement configuration."
                ),
                "business_impact": (
                    "If this claim is not assured, the requirement may not be "
                    "fully supported by observable evidence."
                ),
                "governance_need": (
                    "PML should review whether this claim remains in the "
                    "assurance scope."
                ),
            },
        )()

        suggestions.append(suggestion)

    return suggestions


def run_assurance_for_requirement(requirement, approved_governed_claim_ids):
    """
    Run assurance only for PML-approved governed claims.

    Evidence is collected through the hosted Dynatrace Partner MCP server.

    Flow:
    PML-approved governed claim
        ↓
    Dynatrace Partner MCP tools
        ↓
    EvidenceRecord objects
        ↓
    Claim Assurance Engine
        ↓
    Requirement Assurance Engine
    """

    claims = load_claim_library()

    evidence_provider = DynatraceMCPEvidenceProvider()

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    claim_results = []
    evidence_by_claim = {}

    for governed_claim_id in approved_governed_claim_ids:
        claim = get_claim_by_id(claims, governed_claim_id)

        approved_claim = ApprovedClaim(
            claim=claim,
            target_name="easyTravel-Business",
            thresholds={},
        )

        evidence_records = evidence_provider.collect_evidence(
            approved_claim
        )

        claim_result = claim_assurance_engine.evaluate(
            approved_claim,
            evidence_records,
        )

        claim_results.append(claim_result)
        evidence_by_claim[governed_claim_id] = evidence_records

    requirement_result = requirement_assurance_engine.evaluate(
        requirement,
        claim_results,
    )

    return {
        "requirement": requirement,
        "requirement_result": requirement_result,
        "evidence_by_claim": evidence_by_claim,
    }


def render_evidence_records(evidence_records):
    if not evidence_records:
        st.warning("No evidence records were collected for this claim.")
        return

    for evidence in evidence_records:
        evidence_col1, evidence_col2, evidence_col3 = st.columns(3)

        evidence_col1.write(f"**Evidence Type:** `{evidence.evidence_type}`")
        evidence_col2.write(f"**Source:** `{evidence.source}`")
        evidence_col3.write(f"**Observed:** `{evidence.observed}`")

        st.markdown("**Evidence Details**")

        st.json(
            {
                "value": evidence.value,
                "details": evidence.details,
            }
        )


def render_claim_result(claim_result, evidence_by_claim):
    with st.expander(
        f"{claim_result.claim_id} — {status_badge(claim_result.status)}",
        expanded=False,
    ):
        col1, col2, col3 = st.columns(3)

        col1.write(f"**Target:** `{claim_result.target_name}`")
        col2.write(f"**Confidence:** `{claim_result.confidence}`")
        col3.write(f"**Status:** {status_badge(claim_result.status)}")

        st.markdown("##### Claim Assurance Explanation")
        st.info(claim_result.explanation)

        if claim_result.evidence_gaps:
            st.warning(
                "Missing evidence: "
                + ", ".join(claim_result.evidence_gaps)
            )

        st.markdown("##### Evidence Records")

        evidence_records = evidence_by_claim.get(
            claim_result.claim_id,
            [],
        )

        render_evidence_records(evidence_records)


def render_assurance_explanation(requirement_result, evidence_by_claim):
    explanation_engine = AssuranceExplanationEngine()
    explanation = explanation_engine.explain(requirement_result)

    metrics = calculate_assurance_metrics(
        requirement_result=requirement_result,
        evidence_by_claim=evidence_by_claim,
    )

    st.markdown("## Assurance Explanation")

    with st.container(border=True):
        st.subheader("Executive Assurance Summary")

        st.write(
            f"Requirement assurance score is "
            f"**{metrics['assurance_score']}%** with a "
            f"**{metrics['assurance_band']}** confidence band."
        )

        st.write(
            f"The platform verified **{metrics['verified_claims']} of "
            f"{metrics['total_claims']}** approved claims and observed "
            f"**{metrics['observed_evidence']} of "
            f"{metrics['total_evidence']}** required evidence items through "
            f"Dynatrace Partner MCP."
        )

        if metrics["missing_evidence"] == 0 and metrics["failed_claims"] == 0:
            st.success(
                "No failed claims or missing evidence items were detected in "
                "this assurance run."
            )
        else:
            st.warning(
                f"{metrics['missing_evidence']} evidence item(s), "
                f"{metrics['insufficient_claims']} insufficient claim(s), "
                f"and {metrics['failed_claims']} failed claim(s) require "
                "review."
            )

        with st.expander("Detailed Explanation", expanded=False):
            st.subheader(explanation.title)
            st.write(explanation.summary)

            st.markdown("### Details")
            for detail in explanation.details:
                st.write(f"• {detail}")

        with st.expander("Recommendations", expanded=True):
            for recommendation in explanation.recommendations:
                st.write(f"• {recommendation}")

            if metrics["assurance_score"] >= 90:
                st.write("• Continue monitoring for runtime evidence drift.")
                st.write("• Retain the current governed claim scope.")
            elif metrics["assurance_score"] >= 70:
                st.write("• Review missing evidence and insufficient claims.")
                st.write("• Prioritize evidence gaps affecting runtime health.")
            else:
                st.write("• Escalate assurance gaps for PML and system owner review.")
                st.write("• Do not rely on this requirement as fully assured.")


def render_requirement_result(item):
    requirement = item["requirement"]
    requirement_result = item["requirement_result"]
    evidence_by_claim = item["evidence_by_claim"]

    st.markdown("## Intent Assurance Result")

    with st.container(border=True):
        st.subheader(requirement.title)
        st.write(requirement.description)

        st.markdown(
            f"### Requirement Status: "
            f"{status_badge(requirement_result.status)}"
        )

        st.info(requirement_result.explanation)

        render_assurance_scorecard(
            requirement_result=requirement_result,
            evidence_by_claim=evidence_by_claim,
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Verified Claims", requirement_result.verified_claims)
        col2.metric(
            "Insufficient Evidence",
            requirement_result.insufficient_claims,
        )
        col3.metric("Failed Claims", requirement_result.failed_claims)

        st.markdown("#### Claim Assurance Detail")

        for claim_result in requirement_result.claim_results:
            render_claim_result(
                claim_result,
                evidence_by_claim,
            )

    render_assurance_explanation(
        requirement_result=requirement_result,
        evidence_by_claim=evidence_by_claim,
    )


# ---------------------------------------------------------------------------
# Main dashboard
# ---------------------------------------------------------------------------

SYSTEMS = {
    "easyTravel": {
        "description": (
            "Demo system monitored by Dynatrace and used for governed "
            "runtime assurance."
        ),
        "target_service": "easyTravel-Business",
        "evidence_source": "Dynatrace Partner MCP",
    }
}

selected_system_name = st.selectbox(
    "System",
    list(SYSTEMS.keys()),
)

selected_system = SYSTEMS[selected_system_name]

st.markdown("## System")
st.write(selected_system["description"])

system_col1, system_col2, system_col3 = st.columns(3)
system_col1.metric("System", selected_system_name)
system_col2.metric("Target Service", selected_system["target_service"])
system_col3.metric("Evidence Source", selected_system["evidence_source"])

requirements = load_requirements()
claims = load_claim_library()
claim_library_ids = build_claim_library_index(claims)

selected_requirement = st.selectbox(
    "Select Requirement",
    requirements,
    format_func=lambda requirement: (
        f"{requirement.requirement_id} - {requirement.title}"
    ),
)

st.markdown("## Requirement")
st.write(selected_requirement.description)


st.markdown("## Gemini Claim Discovery")

st.info(
    "Gemini reasons over the selected requirement and known claim patterns "
    "retrieved from the knowledge base to suggest assurance claims."
)

try:
    suggestions = discover_claims_with_gemini(
        selected_requirement.description
    )

    st.success("Gemini claim discovery completed.")

except Exception as exc:
    st.warning(
        "Gemini claim discovery failed. Falling back to requirement claim IDs."
    )
    st.code(str(exc))

    suggestions = build_fallback_suggestions(selected_requirement)


assessed_claims = assess_claim_coverage(
    suggestions=suggestions,
    claim_library_ids=claim_library_ids,
)

assessed_claims = add_existing_executable_claims(
    assessed_claims=assessed_claims,
    selected_requirement=selected_requirement,
    claim_library_ids=claim_library_ids,
)


approved_governed_claim_ids = st.session_state.get(
    "approved_governed_claim_ids",
    [],
)

if not approved_governed_claim_ids:
    approved_governed_claim_ids = [
        item["governed_claim_id"]
        for item in assessed_claims
        if item["coverage_status"] in ["SUPPORTED", "MAPPING_CANDIDATE"]
    ]



supported_claims = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "SUPPORTED"
]

mapping_candidates = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "MAPPING_CANDIDATE"
]

coverage_gaps = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "COVERAGE_GAP"
]

coverage_score = calculate_coverage_score(assessed_claims)

st.markdown("## Assurance Overview")

summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)

summary_col1.metric("Claims in Review", len(assessed_claims))
summary_col2.metric("Supported Claims", len(supported_claims))
summary_col3.metric("Mapping Candidates", len(mapping_candidates))
summary_col4.metric("Coverage Gaps", len(coverage_gaps))
summary_col5.metric("Assurance Coverage", f"{coverage_score}%")


st.markdown("## Coverage Assessment")

st.info(
    "This section shows both existing executable claims and Gemini-discovered "
    "claims. Discovered claim names are preserved. Mapped governed claims are "
    "used only for execution."
)

for item in assessed_claims:
    suggestion = item["suggestion"]

    expander_title = (
        f"{item['discovered_claim_id']} → "
        f"{item['governed_claim_id']} | "
        f"{coverage_badge(item['coverage_status'])}"
    )

    with st.expander(expander_title, expanded=False):
        col1, col2, col3, col4 = st.columns([1.5, 1.5, 2, 2])

        col1.write(
            f"**Discovered Claim:** `{item['discovered_claim_id']}`"
        )
        col2.write(
            f"**Governed Claim:** `{item['governed_claim_id']}`"
        )
        col3.write(f"**Coverage:** {coverage_badge(item['coverage_status'])}")
        col4.write(
            f"**PML Action:** "
            f"{governance_action_label(item['coverage_status'])}"
        )

        st.write(f"**Route:** `{item['governance_route']}`")
        st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

        if item.get("mapped_from"):
            mapping = item.get("mapping_recommendation") or {}

            st.info(
                f"PML Claim Mapping Agent recommends mapping "
                f"`{item['mapped_from']}` → `{item['governed_claim_id']}` "
                f"with confidence `{mapping.get('confidence', 'N/A')}`."
            )

            st.write(
                "**Mapping Rationale:** "
                + mapping.get("rationale", "No rationale provided.")
            )

        st.write(f"**Discovery Source:** {suggestion.policy_name}")
        st.write(f"**Policy ID:** `{suggestion.policy_id}`")
        st.write(f"**Objective:** `{suggestion.objective_id}`")

        render_ai_explanation(suggestion)

        if item["coverage_status"] == "SUPPORTED":
            st.success(
                "This is an existing governed claim with executable "
                "assurance coverage."
            )

        elif item["coverage_status"] == "MAPPING_CANDIDATE":
            st.info(
                "This discovered claim can be normalized into an existing "
                "governed claim if PML approves the mapping."
            )

        elif item["coverage_status"] == "COVERAGE_GAP":
            st.warning(
                "This is a new or unsupported claim. It cannot enter evidence "
                "collection until PML classifies it."
            )


with st.expander(
    f"PML Review ({len(approved_governed_claim_ids)} approved)",
    expanded=False,
):
    st.markdown("## PML Review")

    st.info(
        "PML determines which claims can enter assurance scope. Supported claims "
        "and approved mappings proceed to partner MCP evidence collection. "
        "Coverage gaps remain under review."
    )

    selected_governed_claim_ids = []

    for index, item in enumerate(assessed_claims):
        is_approvable = item["coverage_status"] in [
            "SUPPORTED",
            "MAPPING_CANDIDATE",
        ]

        with st.container(border=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                selected = st.checkbox(
                    item["discovered_claim_id"],
                    value=(
                        item["governed_claim_id"] in approved_governed_claim_ids
                        and is_approvable
                    ),
                    disabled=not is_approvable,
                    key=(
                        f"{selected_requirement.requirement_id}_"
                        f"pml_{index}_"
                        f"{item['discovered_claim_id']}_"
                        f"{item['governed_claim_id']}_"
                        f"{item.get('source_type', 'UNKNOWN')}"
                    ),
                )

            with col2:
                st.write(
                    f"**Discovered Claim:** `{item['discovered_claim_id']}`"
                )
                st.write(
                    f"**Governed / Executable Claim:** "
                    f"`{item['governed_claim_id']}`"
                )
                st.write(
                    f"**Coverage:** "
                    f"{coverage_badge(item['coverage_status'])}"
                )
                st.write(f"**Route:** `{item['governance_route']}`")
                st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

                if item.get("mapped_from"):
                    st.info(
                        f"`{item['mapped_from']}` can be normalized into "
                        f"`{item['governed_claim_id']}` before assurance execution."
                    )

                if item["coverage_status"] == "MAPPING_CANDIDATE":
                    st.success(
                        "PML action: approve semantic mapping to existing "
                        "governed claim before assurance scope."
                    )

                elif item["coverage_status"] == "SUPPORTED":
                    st.success(
                        "PML action: approve existing governed claim for "
                        "assurance scope."
                    )

                else:
                    st.warning(
                        "PML action: classify as new governance claim, reject, "
                        "or defer."
                    )

            if selected and is_approvable:
                selected_governed_claim_ids.append(item["governed_claim_id"])


    if st.button("Approve Supported Claims and Mappings for Assurance"):
        approved_governed_claim_ids = selected_governed_claim_ids
        st.session_state["approved_governed_claim_ids"] = approved_governed_claim_ids

        if approved_governed_claim_ids:
            st.success(
                "Approved governed claims: "
                + ", ".join(approved_governed_claim_ids)
            )
        else:
            st.warning("No claims or mappings were approved.")


st.markdown("## Evidence Collection")

with st.container(border=True):
    st.subheader("Dynatrace Partner MCP Evidence Collection")

    st.info(
        "Runtime evidence is requested from the hosted Dynatrace Partner MCP "
        "server only when assurance is executed. This avoids loading the large "
        "MCP tool catalog on every dashboard refresh."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Approved Claims", len(approved_governed_claim_ids))
    col2.metric("Evidence Provider", "Dynatrace MCP")
    col3.metric("Target Service", "easyTravel-Business")

    with st.expander("MCP Tools Used During Assurance", expanded=False):
        st.write("• `get-entity-id` for service entity evidence")
        st.write("• `query-problems` for active Davis problem evidence")
        st.write("• `create-dql` for service health and latency DQL")
        st.write("• `execute-dql` for runtime metric evidence")


st.markdown("## Run Assurance")

st.info(
    "Assurance is executed only for PML-approved governed claims. "
    "Coverage gaps remain in review."
)

if approved_governed_claim_ids:
    if st.button("Run Assurance"):
        with st.spinner("Collecting evidence through Dynatrace Partner MCP..."):
            result = run_assurance_for_requirement(
                selected_requirement,
                approved_governed_claim_ids,
            )

        st.session_state["last_assurance_result"] = result
        st.success("Assurance run completed.")
else:
    st.warning("Approve at least one governed claim before running assurance.")


if "last_assurance_result" in st.session_state:
    st.divider()
    render_requirement_result(st.session_state["last_assurance_result"])
st.divider()
st.caption(
    "IntentSync • Requirement → Claims → Governance → Evidence → Assurance"
)
st.caption(
    "Powered by Gemini, Google Cloud, Agent Builder MCP and Dynatrace."
)
