from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, length, trim, lower, regexp_replace, to_timestamp, to_date, date_format
from pyspark.sql.types import StructType, StringType
import requests
import socket
import time

def wait_for_kafka(host, port, timeout=60):
    start_time = time.time()
    while True:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print("✅ Kafka is ready!")
            break
        except Exception as e:
            if time.time() - start_time > timeout:
                raise Exception(f"Timeout waiting for Kafka at {host}:{port}")
            print("⏳ Waiting for Kafka to be ready...")
            time.sleep(2)

# Trước khi create SparkSession
wait_for_kafka("kafka", 29092)



# Khởi tạo Spark session
spark = SparkSession.builder \
    .appName("KafkaSentimentTransform") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin123") \
    .config("spark.hadoop.fs.s3a.secret.key", "admin123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Schema cho dữ liệu Kafka
schema = StructType() \
    .add("id", StringType()) \
    .add("name", StringType()) \
    .add("date", StringType()) \
    .add("title", StringType()) \
    .add("content", StringType()) \
    .add("sentiment_score", StringType())

# Đọc và parse dữ liệu từ Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "load_raw_data")
    .option("startingOffsets", "latest")
    .option("maxOffsetsPerTrigger", 100)  # <= giới hạn batch size
    .load()
)

parsed_df = (
    df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# Làm sạch dữ liệu và chuyển đổi ngày
clean_df = (
    parsed_df
    .filter(col("content").isNotNull())
    .filter(length(trim(col("content"))) > 5)
    .withColumn("content", lower(col("content")))
    .withColumn("content", regexp_replace("content", "[\\n\\r]", " "))
    .withColumn("content", regexp_replace("content", "http\\S+", ""))
    .withColumn("content", regexp_replace("content", "[^a-zA-Z0-9à-ỹÀ-Ỹ\\s#@]", ""))
    .withColumn("content", regexp_replace("content", "\\s+", " "))
    .filter(length(trim(col("content"))) > 5)
    .withColumn("date", to_timestamp("date"))
    .withColumn("date_only", to_date("date"))
    .withColumn("month", date_format("date", "yyyy-MM"))
)

# Hàm xử lý batch
def process_batch(batch_df, epoch_id):
    if batch_df.rdd.isEmpty():
        print(f"[Epoch {epoch_id}] ❗Batch is empty.")
        return

    pdf = batch_df.toPandas()
    texts = pdf["content"].tolist()

    print(f"[Epoch {epoch_id}] 🚀 Processing {len(texts)} texts...")

    try:
        response = requests.post("http://model-sentiment-service:5000/predict_batch", json={"texts": texts})
        sentiments = response.json().get("labels", ["error"] * len(texts))
    except Exception as e:
        print(f"[Epoch {epoch_id}] ❌ Error calling API: {e}")
        sentiments = ["error"] * len(texts)

    for i, (text, sentiment) in enumerate(zip(texts, sentiments)):
        print(f"[Epoch {epoch_id}] #{i+1}: \"{text[:100]}\" → {sentiment}")

    pdf["sentiment"] = sentiments
    result_sdf = spark.createDataFrame(pdf)

    result_sdf.selectExpr("to_json(struct(*)) AS value") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("topic", "social_sentiment_cleaned") \
    .save()

    # result_sdf.write.mode("append").parquet("/data/social_sentiment_cleaned")
    result_sdf.write.mode("append").parquet("s3a://sentiment-results/social_sentiment_cleaned")
    print(f"[Epoch {epoch_id}] ✅ Done processing batch.\n")

# Stream xử lý batch
(
    clean_df.writeStream
    .foreachBatch(process_batch)
    .option("checkpointLocation", "/tmp/spark-checkpoint-foreach")
    .start()
    .awaitTermination()
)
