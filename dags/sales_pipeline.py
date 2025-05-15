from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def _validate_data():
    # context = DataContext(
    #     "/Users/simon/Documents/Epsi/i2/DataOps/codespace-dataops/great_expectations")
    # checkpoint = LegacyCheckpoint(
    #     name="my_checkpoint",
    #     data_context=context,
    #     config_version=1.0,
    #     class_name="LegacyCheckpoint",
    #     run_name_template="%Y%m%d-%H%M%S",
    #     validations=[
    #         {
    #             "batch_request": {
    #                 "datasource_name": "my_datasource",
    #                 "data_connector_name": "default_runtime_data_connector_name",
    #                 "data_asset_name": "sales_data",
    #                 "runtime_parameters": {
    #                     "path": "/usr/local/airflow/data/sales.csv"
    #                 },
    #                 "batch_identifiers": {"default_identifier_name": "default_id"}
    #             },
    #             "expectation_suite_name": "sales.expectations"
    #         }
    #     ]
    # )
    # results = checkpoint.run()
    # if not results["success"]:
    #     raise ValueError("Data validation failed")

    # A 14h30 rien ne fonctionne, code supprimé

    return


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
