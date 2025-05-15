from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
import psycopg2

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def _validate_data():
    conn = psycopg2.connect(
        "dbname=ta_base user=ton_user password=ton_mdp host=ton_hote")
    cursor = conn.cursor()

    # 1) Check nulls on CustomerID and UnitPrice
    cursor.execute("""
        SELECT COUNT(*) FROM row_sales
        WHERE CustomerID IS NULL OR UnitPrice IS NULL;
    """)
    null_count = cursor.fetchone()[0]
    if null_count > 0:
        raise ValueError(
            f"Data validation failed: {null_count} rows have NULL CustomerID or UnitPrice")

    # 2) Check duplicates on InvoiceNo + StockCode
    cursor.execute("""
        SELECT InvoiceNo, StockCode, COUNT(*) FROM row_sales
        GROUP BY InvoiceNo, StockCode
        HAVING COUNT(*) > 1;
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        raise ValueError(
            f"Data validation failed: Found duplicates on InvoiceNo + StockCode: {duplicates}")

    cursor.close()
    conn.close()


with DAG(
    'sales_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    template_searchpath=['/opt/airflow/sql']
) as dag:

    load_data = PostgresOperator(
        task_id='load_sales_data',
        postgres_conn_id='postgres_default',
        sql='load_sales.sql',
    )

    dbt_run = DockerOperator(
        task_id='dbt_run',
        image='custom-dbt',
        command='dbt run --profiles-dir /usr/app/dbt',
        network_mode='codespace-dataops_epsi_dataops_network',
        mounts=[
            {
                "source": "/Users/simon/Documents/Epsi/i2/DataOps/codespace-dataops/dbt",
                "target": "/usr/app/dbt",
                "type": "bind",
            }
        ],
        mount_tmp_dir=False,
        auto_remove=True,
        dag=dag,
    )

    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=_validate_data
    )

    load_data >> dbt_run >> validate_data
