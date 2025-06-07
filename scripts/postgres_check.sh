#!/bin/bash
set -a
source .env
set +a

docker-compose exec postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -c "CREATE TABLE test_table(id SERIAL PRIMARY KEY, val TEXT); INSERT INTO test_table(val) VALUES('foo');"

