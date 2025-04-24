from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from kafka import KafkaProducer
import json
import os

def send_to_kafka():
    file_path = "/opt/airflow/data/raw_data.csv"  # <-- nên mount rõ vào /opt/airflow/data
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    df = pd.read_csv(file_path).sample(n=1000)
    producer = KafkaProducer(
        bootstrap_servers='kafka:29092',  # <-- sử dụng listener DOCKER (nội bộ Docker)
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    for _, row in df.iterrows():
        producer.send("load_raw_data", row.to_dict())
    producer.flush()

default_args = {
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    "extract_to_kafka",
    schedule_interval="*/5 * * * *",
    catchup=False,
    default_args=default_args,
) as dag:

    send_task = PythonOperator(
        task_id="send_batch_kafka",
        python_callable=send_to_kafka
    )
