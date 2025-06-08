#!/usr/bin/env bash
#
# run_all.sh — Orchestrator: build/start containers, health checks, simulate business
#
set -euo pipefail

API_URL="${API_URL:-http://localhost:5000}"

echo
echo " Uruchamiam health checki Dockera (wszystkie usługi)..."
python3 scripts/health_checks/docker/check_all.py

echo
echo " Szybki test PostgreSQL..."
bash scripts/postgres_check.sh

echo
echo " Uruchamiam symulację biznesową (Flask API)..."
./scripts/simulate_business.sh

echo
echo "Wszystko gotowe! Zweryfikuj endpointy:"
echo "   • Użytkownicy: curl $API_URL/users"
echo "   • Zamówienia:  curl $API_URL/orders"
echo
