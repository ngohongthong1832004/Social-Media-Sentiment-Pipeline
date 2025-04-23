# transform_pipeline/spark_app.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import requests

spark = SparkSession.builder \
    .appName("SentimentTransform") \
    .master("spark://spark-master:7077") \
    .config("spark.rpc.message.maxSize", "256") \
    .getOrCreate()


# Đọc file từ thư mục đã mount (data-raw)
df = spark.read.option("header", True).csv("/opt/sentiment/data-raw/input.csv")

# UDF gọi model-service
def get_sentiment(text):
    try:
        res = requests.post("http://model-service:5000/predict", json={"text": text}, timeout=5)
        return res.json()[0]['label']
    except:
        return "error"

sentiment_udf = udf(get_sentiment, StringType())

# Thêm cột sentiment
df = df.withColumn("sentiment", sentiment_udf(df["text"]))

# Ghi kết quả ra output
df.write.mode("overwrite").option("header", True).csv("/opt/sentiment/data/output")
