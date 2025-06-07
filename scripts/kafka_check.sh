#!/bin/bash
set -a
source .env
set +a

echo "Sprawdzam basic Kafka topic health…"
docker-compose exec kafka \
  kafka-topics --bootstrap-server kafka:"$KAFKA_PORT" \
               --create --topic health_check --partitions 1 --replication-factor 1 \
  && \
  docker-compose exec kafka \
  kafka-topics --bootstrap-server kafka:"$KAFKA_PORT" \
               --describe --topic health_check

echo "Sprawdzam Avro-consumer (schema-registry)…"
docker-compose exec kafka-tools \
  kafka-avro-console-consumer \
    --bootstrap-server kafka:"$KAFKA_PORT" \
    --topic dbserver1.public.test_table \
    --from-beginning \
    --property schema.registry.url=http://schema-registry:"$SCHEMA_REGISTRY_PORT" \
    --timeout-ms 1000
