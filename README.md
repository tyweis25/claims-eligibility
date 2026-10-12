# claims-eligibility

Small FastAPI service that checks whether a member's plan covers a service. Rules live in memory so the demo has no database.

A request is eligible when all three are true:

- `member_id` is enrolled (`M1001`, `M1002`, `M1003`)
- `plan_code` matches that enrollment (`PPO-100` or `HMO-200`)
- `service_code` is covered by the plan (`99213` and `80053` on both plans; `93000` on `PPO-100` only)

## Run locally

```bash
cd claims-eligibility
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API listens on http://127.0.0.1:8000. Interactive docs are at http://127.0.0.1:8000/docs.

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/eligibility \
  -H 'Content-Type: application/json' \
  -d '{"member_id":"M1001","plan_code":"PPO-100","service_code":"99213"}'
```

## Test

From `claims-eligibility`, with the virtualenv activated:

```bash
pytest
```

## Docker

```bash
docker build -t claims-eligibility .
docker run --rm -p 8000:8000 claims-eligibility
```

The image uses `python:3.12-slim` and runs as the non-root user `app`.
