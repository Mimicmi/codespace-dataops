from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def _validate_data():
    # Implémentation de Great Expectations ira ici
    pass


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

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /usr/app/dbt && dbt run'
    )

    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=_validate_data
    )

    load_data >> dbt_run >> validate_data
