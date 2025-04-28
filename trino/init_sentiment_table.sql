CREATE TABLE IF NOT EXISTS hive.default.sentiment (
    id VARCHAR,
    name VARCHAR,
    date TIMESTAMP,
    title VARCHAR,
    content VARCHAR,
    sentiment_score VARCHAR,
    date_only DATE,
    month VARCHAR,
    sentiment VARCHAR
)
WITH (
    external_location = 's3a://sentiment-results/social_sentiment_cleaned/',
    format = 'PARQUET'
);
