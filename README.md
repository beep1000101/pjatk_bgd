# Mini Data Platform with Spark

## Overview

This project simulates a business process, streams change data via Debezium+Kafka, processes events with Spark Structured Streaming, and stores results in MinIO as Delta Lake tables.

## Architecture

* **PostgreSQL**: source database with two tables (`users`, `orders`)
* **Debezium**: captures CDC from PostgreSQL into Kafka topics
* **Kafka**: message broker holding CDC events
* **Spark**: processes Kafka streams, transforms data, writes to Delta format
* **MinIO**: S3-compatible storage for Delta files
* **Flask API**: serves processed data via HTTP

## Verifying Spark

To ensure Spark is working:

1. **Start Spark Master & Worker**:

   ```sh
   docker-compose up -d spark-master spark-worker
   ```
2. **Submit a Test Job**:

   ```sh
   docker exec -it spark-master spark-submit \
     --master spark://spark-master:7077 \
     /opt/app/scripts/spark_test.py
   ```
3. **Check Logs**:

   ```sh
   docker logs -f spark-master
   ```

   You should see your job start, tasks executed, and completion messages.
4. **Web UI**:
   Visit `http://localhost:8080` to inspect active jobs and executors.

## Example Spark Script

Place under `scripts/spark_test.py`:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestSpark") \
    .getOrCreate()

data = spark.range(0, 100)
data_count = data.count()
print(f"Counted {data_count} records in Spark test.")

spark.stop()
```

## Integrating in Project

* Add streaming logic in `scripts/`:

  * Read from Kafka:

    ```python
    spark.readStream.format("kafka") \
         ...
    ```
  * Transform and write to MinIO/Delta:

    ```python
    df.writeStream \
      .format("delta") \
      .option("checkpointLocation", "/delta/checkpoint") \
      .start("s3a://minio/bucket/path")
    ```

## Usage

1. Build & run services:

   ```sh
   ```

docker-compose up --build -d

````
2. Seed database:
   ```sh
python database/db_seed.py
````

3. Register Debezium connector:

   ```sh
   ```

scripts/generate\_register\_json.py &&&#x20;
curl -X POST -H "Content-Type: application/json"&#x20;
\--data @register-postgres.json [http://localhost:8083/connectors](http://localhost:8083/connectors)

```
4. Submit Spark streaming job (as above).

## Contributing
- Write unit tests for Spark logic under `tests/`
- Update this README with new commands and architecture changes

```
