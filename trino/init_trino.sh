#!/bin/sh

echo '⏳ Waiting for Trino...'
until curl -s http://trino:8080/v1/info; do
  echo '🔁 Still waiting for Trino...'; sleep 5;
done

echo '✅ Trino is up! Running init_sentiment_table.sql...'

curl --request POST http://trino:8080/v1/statement \
  --header "X-Trino-User: admin" \
  --header "X-Trino-Schema: default" \
  --header "X-Trino-Catalog: hive" \
  --header "Content-Type: text/plain" \
  --data-binary "@/init_sentiment_table.sql"

echo '✅ Table sentiment created successfully!'

# Keep container alive
tail -f /dev/null
