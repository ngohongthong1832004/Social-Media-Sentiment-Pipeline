Dựa trên yêu cầu **tập trung vào mảng Data Engineering** và từ file `docker-compose.yml` bạn gửi, mình đã viết lại README cho dự án theo phong cách chuyên nghiệp hơn, đúng trọng tâm "Data Engineer" như sau:

---

# 🛠️ Social Media Sentiment Data Pipeline (Dockerized, Data Engineering Focus)

Một hệ thống **Data Pipeline** hiện đại, tập trung xử lý dữ liệu từ các nền tảng mạng xã hội (YouTube, TikTok, Facebook...), được thiết kế theo kiến trúc **ETL** và **Streaming**, vận hành hoàn toàn bằng **Docker Compose**.

Hệ thống ứng dụng các công nghệ tiên tiến trong lĩnh vực **Data Engineering** như Airflow, Kafka, Spark, Trino, MinIO, Hive Metastore để **di chuyển - xử lý - lưu trữ - truy vấn** dữ liệu.

---

## 📐 Kiến trúc tổng quan

```
[Airflow] → Kafka → [Spark Structured Streaming (Clean + Predict)] → Great Expectations (Validation) → Parquet files → MinIO (S3)
                                                                                                              ↓
                                                                                                           Trino
                                                                                                              ↓
                                                                                                 Metabase / Superset (BI Tools)
```

---

## 🧩 Thành phần hệ thống

| Thành phần             | Vai trò chính                                                            |
|-------------------------|--------------------------------------------------------------------------|
| **Apache Airflow**       | Orchestration, Scheduling cho toàn bộ pipeline ETL                      |
| **Apache Kafka**         | Message broker cho Data Streaming                                        |
| **Apache Spark**         | Xử lý dữ liệu lớn + Sentiment Analysis theo dạng Structured Streaming    |
| **PyTorch Transformers** | Phân tích cảm xúc bằng mô hình ngôn ngữ pretrained                       |
| **Great Expectations**   | Data Validation, kiểm tra chất lượng dữ liệu đầu ra                      |
| **MinIO**                | Object Storage S3-compatible để lưu trữ file parquet                    |
| **Trino (PrestoSQL)**    | SQL Query Engine nhanh, scale-out, kết nối MinIO, MariaDB, Postgres      |
| **Hive Metastore + MariaDB** | Quản lý metadata cho Trino truy vấn dữ liệu parquet              |
| **Superset**             | Data Visualization và Dashboarding                                      |

---

## 📁 Cấu trúc thư mục

```bash
sentiment-data-pipeline/
├── airflow/               # DAGs xử lý luồng dữ liệu ETL
├── kafka/                 # Kafka configuration
├── spark/                 # Spark jobs, phân tích dữ liệu, sentiment prediction
├── minio/                 # MinIO storage setup
├── trino/                 # Trino + Hive metastore cấu hình kết nối dữ liệu
├── superset/              # Superset setup cho trực quan hóa dữ liệu
├── model_service/         # Flask service phục vụ model phân tích cảm xúc
├── docker-compose.yml     # Docker Compose orchestration file
└── README.md              # Tài liệu hướng dẫn
```

---

## 🚀 Hướng dẫn triển khai

### 1. Clone repository

```bash
git clone https://github.com/your-org/sentiment-data-pipeline.git
cd sentiment-data-pipeline
```

### 2. Chuẩn bị dữ liệu đầu vào

- Copy dữ liệu social media vào thư mục `./data/`.
- Đặt tên file dữ liệu là `input.csv` hoặc chỉnh lại volume trong docker-compose.

### 3. Khởi động toàn bộ hệ thống

```bash
docker-compose up --build
```

### 4. Truy cập các dịch vụ

| Dịch vụ         | URL                             | Thông tin đăng nhập        |
|-----------------|----------------------------------|-----------------------------|
| **Airflow UI**  | [http://localhost:8089](http://localhost:8089) | admin/admin |
| **Superset**    | [http://localhost:8088](http://localhost:8088) | admin/admin |
| **MinIO**       | [http://localhost:9001](http://localhost:9001) | admin123/admin123 |
| **Kafka UI**    | [http://localhost:9003](http://localhost:9003) | - |

---

## 📊 Dòng dữ liệu chính (ETL Flow)

1. **Extract**: Airflow DAG đẩy dữ liệu social media lên Kafka topic `load_raw_data`.
2. **Transform**: Spark job đọc từ Kafka, thực hiện cleaning + sentiment prediction.
3. **Validation**: Dùng Great Expectations để validate dữ liệu đã clean.
4. **Load**: Lưu file parquet kết quả vào MinIO.
5. **Query**: Trino truy vấn file parquet.
6. **Visualize**: Superset / Metabase kết nối Trino để vẽ biểu đồ phân tích cảm xúc.

---

## 🔥 Kế hoạch phát triển mở rộng

- [v] Multi-language Sentiment Analysis (EN, VI, JP...)
- [ ] Monitoring bằng Prometheus + Alert nếu dữ liệu sentiment tiêu cực tăng mạnh
- [ ] Auto retraining pipeline khi phát hiện data drift
- [ ] Giao diện quản lý pipeline bằng Streamlit

---

## Cách chay thử

```bash
./run.bat
```
or

```bash
docker-compose up --build
```

## Một số lưu ý
- spark-streaming: đọc từ Kafka, xử lý dữ liệu, lưu vào MinIO nên cần dùng lượng lớn RAM và CPU. Nên dùng máy có cấu hình mạnh.
- Superset: dùng để trực quan hóa dữ liệu, Có thể tự động tạo dashboard từ các truy vấn SQL.
- Trino: dùng để truy vấn dữ liệu từ MinIO, Hive Metastore. Chưa tự tạo được schema tự động.

## Một số câu lệnh cần chạy thử
- Trino: '''
CREATE TABLE hive.default.sentiment (
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
'''