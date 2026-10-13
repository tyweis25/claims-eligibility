"""Minimal claims eligibility API for a live demo."""

import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="claims-eligibility")

# member_id -> plan the member is enrolled in
ENROLLMENT = {
    "M1001": "PPO-100",
    "M1002": "HMO-200",
    "M1003": "PPO-100",
}

# plan_code -> service codes that plan covers
PLAN_COVERAGE = {
    "PPO-100": {"99213", "80053", "93000", "99441"},
    "HMO-200": {"99213", "80053", "99441"},
}


class EligibilityRequest(BaseModel):
    member_id: str = Field(min_length=1)
    plan_code: str = Field(min_length=1)
    service_code: str = Field(min_length=1)


class EligibilityResponse(BaseModel):
    eligible: bool
    reason: str


# Counts POST /eligibility calls while FEATURE_Y is true. Calls 1, 2, 6, 7, ...
# fail, which is 2 of every 5 (40 percent). Health never consults this.
_eligibility_calls = 0


def _feature_y_failure() -> JSONResponse | None:
    global _eligibility_calls
    if os.getenv("FEATURE_Y") != "true":
        return None
    _eligibility_calls += 1
    if _eligibility_calls % 5 in (1, 2):
        return JSONResponse(status_code=500, content={"detail": "eligibility unavailable"})
    return None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/eligibility", response_model=None)
def check_eligibility(body: EligibilityRequest) -> EligibilityResponse | JSONResponse:
    failure = _feature_y_failure()
    if failure is not None:
        return failure

    enrolled_plan = ENROLLMENT.get(body.member_id)
    if enrolled_plan is None:
        return EligibilityResponse(eligible=False, reason="Member not found")

    if body.plan_code != enrolled_plan:
        return EligibilityResponse(
            eligible=False,
            reason=f"Member is enrolled in {enrolled_plan}, not {body.plan_code}",
        )

    if body.service_code not in PLAN_COVERAGE.get(body.plan_code, set()):
        return EligibilityResponse(
            eligible=False,
            reason=f"Service {body.service_code} is not covered by plan {body.plan_code}",
        )

    return EligibilityResponse(
        eligible=True,
        reason=f"Service {body.service_code} is covered by plan {body.plan_code}",
    )
