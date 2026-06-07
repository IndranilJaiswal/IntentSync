import sys
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel


ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "backend" / "app_v2"
sys.path.append(str(APP_DIR))


from assurance_service import (  # noqa: E402
    run_assurance_for_requirement,
    serialize_assurance_result,
)


app = FastAPI(
    title="IntentSync API",
    version="0.2.0",
    description=(
        "API tools for IntentSync Agent Builder integration. "
        "IntentSync synchronizes intent with reality through continuous "
        "assurance."
    ),
)


class AssuranceRequest(BaseModel):
    requirement_id: str
    approved_governed_claim_ids: Optional[List[str]] = None
    target_name: str = "easyTravel-Business"


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "IntentSync API",
        "version": "0.2.0",
    }


@app.post("/run-assurance")
def run_assurance(request: AssuranceRequest):
    result = run_assurance_for_requirement(
        requirement_id=request.requirement_id,
        approved_governed_claim_ids=request.approved_governed_claim_ids,
        target_name=request.target_name,
    )

    return serialize_assurance_result(result)
