from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ELIGIBLE = {
    "member_id": "M1001",
    "plan_code": "PPO-100",
    "service_code": "99213",
}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_eligible_when_plan_covers_service():
    response = client.post("/eligibility", json=ELIGIBLE)

    assert response.status_code == 200
    assert response.json() == {
        "eligible": True,
        "reason": "Service 99213 is covered by plan PPO-100",
    }


def test_ineligible_when_member_is_unknown():
    response = client.post(
        "/eligibility",
        json={**ELIGIBLE, "member_id": "M9999"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["eligible"] is False
    assert body["reason"] == "Member not found"


def test_ineligible_when_plan_does_not_match_enrollment():
    response = client.post(
        "/eligibility",
        json={**ELIGIBLE, "plan_code": "HMO-200"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["eligible"] is False
    assert body["reason"] == "Member is enrolled in PPO-100, not HMO-200"


def test_ineligible_when_service_is_not_covered():
    response = client.post(
        "/eligibility",
        json={
            "member_id": "M1002",
            "plan_code": "HMO-200",
            "service_code": "93000",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["eligible"] is False
    assert body["reason"] == "Service 93000 is not covered by plan HMO-200"


def test_invalid_when_field_is_missing():
    response = client.post(
        "/eligibility",
        json={"member_id": "M1001", "plan_code": "PPO-100"},
    )

    assert response.status_code == 422


def test_invalid_when_field_is_empty():
    response = client.post(
        "/eligibility",
        json={**ELIGIBLE, "service_code": ""},
    )

    assert response.status_code == 422


def test_invalid_when_field_has_wrong_type():
    response = client.post(
        "/eligibility",
        json={**ELIGIBLE, "member_id": ["M1001"]},
    )

    assert response.status_code == 422
