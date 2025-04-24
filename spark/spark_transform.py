from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import requests

# Khởi tạo Spark session
spark = SparkSession.builder.appName("KafkaSentimentTransform").getOrCreate()

# Schema cho dữ liệu Kafka
schema = StructType().add("content", StringType()).add("user", StringType())

# Đọc dữ liệu từ Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "load_raw_data")
    .option("startingOffsets", "latest")
    .load()
)

# Parse JSON
parsed_df = (
    df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# Hàm xử lý theo batch
def process_batch(batch_df, epoch_id):
    if batch_df.rdd.isEmpty():
        print(f"[Epoch {epoch_id}] ❗Batch is empty.")
        return

    # Convert sang pandas để xử lý dễ hơn
    pdf = batch_df.toPandas()
    texts = pdf["content"].tolist()

    print(f"[Epoch {epoch_id}] 🚀 Processing {len(texts)} texts...")

    # Gọi API batch
    try:
        response = requests.post("http://model-sentiment-service:5000/predict_batch", json={"texts": texts})
        sentiments = response.json().get("labels", ["error"] * len(texts))
    except Exception as e:
        print(f"[Epoch {epoch_id}] ❌ Error calling API: {e}")
        sentiments = ["error"] * len(texts)

    # In log kết quả từng dòng
    for i, (text, sentiment) in enumerate(zip(texts, sentiments)):
        print(f"[Epoch {epoch_id}] #{i+1}: \"{text}\" → {sentiment}")

    # Gán lại kết quả vào pandas và convert ngược lại
    pdf["sentiment"] = sentiments
    result_sdf = spark.createDataFrame(pdf)

    # Ghi vào Kafka
    (
        result_sdf
        .selectExpr("to_json(struct(*)) AS value")
        .write
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("topic", "social_sentiment_cleaned")
        .save()
    )

    # Ghi vào Parquet
    (
        result_sdf
        .write
        .mode("append")
        .parquet("/data/social_sentiment_cleaned")
    )

    print(f"[Epoch {epoch_id}] ✅ Done processing batch.\n")

# Dùng foreachBatch để stream
(
    parsed_df.writeStream
    .foreachBatch(process_batch)
    .option("checkpointLocation", "/tmp/spark-checkpoint-foreach")
    .start()
    .awaitTermination()
)
# Đóng Spark session
# spark.stop()