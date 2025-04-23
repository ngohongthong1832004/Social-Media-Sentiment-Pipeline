from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("run_spark_sentiment", start_date=datetime(2023, 1, 1), schedule_interval="@daily", catchup=False) as dag:
    run_spark = BashOperator(
        task_id="run_spark_job",
        bash_command="spark-submit /opt/sentiment/transform_pipeline/spark_app.py"
    )
