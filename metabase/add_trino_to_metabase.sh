#!/bin/bash

# ==== Cấu hình thông tin Metabase và Trino ====
METABASE_HOST="http://localhost:3000"
METABASE_USER="admin@gmail.com"   # Email đăng nhập Metabase
METABASE_PASS="baphongpine2004"               # Password đăng nhập Metabase

TRINO_HOST="trino"
TRINO_PORT="8080"
TRINO_CATALOG="hive"
TRINO_SCHEMA="default"

echo "==== 1. Login lấy session token ===="
SESSION_TOKEN=$(curl -s -X POST "${METABASE_HOST}/api/session" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"${METABASE_USER}\", \"password\": \"${METABASE_PASS}\"}" \
    | sed -E 's/.*"id":"([^"]+)".*/\1/')

if [[ "$SESSION_TOKEN" == "null" || -z "$SESSION_TOKEN" ]]; then
  echo "❌ Login Metabase thất bại! Kiểm tra lại user/password."
  exit 1
fi


SESSION_TOKEN="6e3b16a9-4360-419b-b3d6-cdc5b4285a48"

echo "✅ Login thành công, lấy được Session Token."

# ==== 2. Gửi API thêm Database Trino ====
curl -s -X POST "${METABASE_HOST}/api/database" \
    -H "Content-Type: application/json" \
    -H "X-Metabase-Session: ${SESSION_TOKEN}" \
    -d "{
      \"name\": \"Trino Database\",
      \"engine\": \"trino\",
      \"details\": {
        \"host\": \"${TRINO_HOST}\",
        \"port\": ${TRINO_PORT},
        \"catalog\": \"${TRINO_CATALOG}\",
        \"schema\": \"${TRINO_SCHEMA}\",
        \"user\": \"admin\",
        \"password\": \"\",
        \"ssl\": false
      },
      \"is_full_sync\": true,
      \"is_on_demand\": false,
      \"schedules\": {}
    }"

echo "✅ Đã gửi yêu cầu tạo Database Trino."
