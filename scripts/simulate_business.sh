#!/usr/bin/env bash
#
# scripts/simulate_business.sh
# Symuluje prosty workflow biznesowy: dodaje użytkowników i zamówienia
# Wymaga: curl, jq

set -euo pipefail

API_URL="${API_URL:-http://localhost:5000}"

echo "=== Symulacja: tworzenie użytkowników ==="
declare -a USER_NAMES=("Test User" "Alice" "Bob" "Carol")
USERS=()
for i in "${!USER_NAMES[@]}"; do
  # Generuj unikalny email na podstawie czasu i indeksu
  unique_hash=$(date +%s%N)$i
  email="user_${unique_hash}@example.com"
  USERS+=("{\"name\":\"${USER_NAMES[$i]}\",\"email\":\"$email\"}")
done

USER_IDS=()
for payload in "${USERS[@]}"; do
  resp=$(curl -s -X POST "$API_URL/users" \
    -H "Content-Type: application/json" \
    -d "$payload")
  id=$(echo "$resp" | jq -r '.id')
  if [[ "$id" == "null" || -z "$id" ]]; then
    echo "Błąd: nie udało się utworzyć użytkownika, odpowiedź: $resp"
  else
    USER_IDS+=("$id")
    echo "Użytkownik utworzony: id=$id, dane=$payload"
  fi
done

if [[ ${#USER_IDS[@]} -eq 0 ]]; then
  echo "Brak poprawnie utworzonych użytkowników, przerywam."
  exit 1
fi

echo
echo "=== Symulacja: tworzenie zamówień ==="
ORDERS=()
PRODUCTS=("Widget" "Gadget" "Doohickey" "Widget")
QUANTITIES=(5 2 1 10)
for i in "${!PRODUCTS[@]}"; do
  ORDERS+=("{\"customer_id\":${USER_IDS[0]},\"product\":\"${PRODUCTS[$i]}\",\"quantity\":${QUANTITIES[$i]}}")
done

for payload in "${ORDERS[@]}"; do
  resp=$(curl -s -X POST "$API_URL/orders" \
    -H "Content-Type: application/json" \
    -d "$payload")
  order_id=$(echo "$resp" | jq -r '.id')
  echo "Order created: id=$order_id, data=$payload"
done

echo
echo "=== Gotowe! ==="
echo "Możesz teraz zweryfikować dane np. poprzez:"
echo "  curl $API_URL/users"
echo "  curl $API_URL/orders"
