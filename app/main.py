"""Minimal claims eligibility API for a live demo."""

from fastapi import FastAPI
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
    "PPO-100": {"99213", "80053", "93000"},
    "HMO-200": {"99213", "80053"},
}


class EligibilityRequest(BaseModel):
    member_id: str = Field(min_length=1)
    plan_code: str = Field(min_length=1)
    service_code: str = Field(min_length=1)


class EligibilityResponse(BaseModel):
    eligible: bool
    reason: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/eligibility")
def check_eligibility(body: EligibilityRequest) -> EligibilityResponse:
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
