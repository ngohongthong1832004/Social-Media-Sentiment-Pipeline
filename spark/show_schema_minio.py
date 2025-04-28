from pyspark.sql import SparkSession

# Kết nối Spark
spark = SparkSession.builder \
    .appName("Check Parquet Schema") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin123") \
    .config("spark.hadoop.fs.s3a.secret.key", "admin123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Đọc file Parquet
df = spark.read.parquet("s3a://sentiment-results/social_sentiment_cleaned/")

# In schema thực tế
df.printSchema()
