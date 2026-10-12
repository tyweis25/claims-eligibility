#!/bin/sh
# Usage: scripts/demo-tunnel.sh [namespace]
# Forward svc/claims-eligibility to http://127.0.0.1:18080.
# Namespace defaults to qa.

NS="${1:-qa}"
exec kubectl port-forward -n "$NS" --address 127.0.0.1 svc/claims-eligibility 18080:80
