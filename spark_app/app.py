from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

# 1) Zdefiniuj schemat JSON (taki, jaki Debezium wypuszcza przy zmianach)
schema = StructType() \
    .add("before", StructType([...])) \
    .add("after", StructType([
        ("id", IntegerType()),
        ("name", StringType()),
        ("email", StringType()),
        ("created_at", TimestampType()),
        ("updated_at", TimestampType())
    ])) \
    .add("op", StringType()) \
    .add("ts_ms", TimestampType())

spark = SparkSession.builder \
    .appName("DebeziumJSON") \
    .getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "dbserver1.public.users") \
    .option("startingOffsets", "earliest") \
    .load()

parsed = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.after.*")

query = parsed.writeStream \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
