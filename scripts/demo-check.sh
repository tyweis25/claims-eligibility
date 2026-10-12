#!/bin/sh
# Usage: scripts/demo-check.sh
# Check health and eligibility through the local tunnel on port 18080.

base=http://127.0.0.1:18080

curl --max-time 5 -sS "$base/health"
echo

for code in 99213 99441; do
  curl --max-time 5 -sS -X POST "$base/eligibility" \
    -H 'Content-Type: application/json' \
    -d "{\"member_id\":\"M1001\",\"plan_code\":\"PPO-100\",\"service_code\":\"$code\"}"
  echo
done
