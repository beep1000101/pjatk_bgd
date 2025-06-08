#!/bin/bash
set -a
source .env
set +a

# docker-compose exec postgres psql \
#   -U "$POSTGRES_USER" \
#   -d "$POSTGRES_DB" \
#   -c "CREATE TABLE test_table(id SERIAL PRIMARY KEY, val TEXT); INSERT INTO test_table(val) VALUES('foo');"

# Dodaj przykładowego użytkownika i zamówienie (jeśli istnieją odpowiednie tabele)
docker-compose exec postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -c "INSERT INTO users(name, email) VALUES('Dummy User', 'dummy_$(date +%s)@example.com') ON CONFLICT DO NOTHING;"

docker-compose exec postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -c "INSERT INTO orders(customer_id, product, quantity) SELECT id, 'Dummy Product', 1 FROM users WHERE name='Dummy User' ORDER BY id DESC LIMIT 1;"

