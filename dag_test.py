import datetime
from airflow import DAG
from airflow.models import Variable

conn = "russpass_dev"
env = "test_project_for_CISM"
config = Variable.get(f"{env}_rus", deserialize_json = True)


with DAG(env, description=env,
          schedule_interval=None,
          start_date=datetime.datetime(2021, 11, 7),
          catchup=False) as dag:
    from airflow.operators.dummy import DummyOperator
    from airflow.operators.python import PythonOperator
    from airflow.providers.postgres.operators.postgres import PostgresOperator
    import reference_module
    from test_project.module_for_test_pj import LocalCsvToPostgresOperator


    start_step = DummyOperator(task_id="start_step",dag=dag)
    end_step = DummyOperator(task_id="end_step",dag=dag)


    TABLE_NAME = "public.opensky"
    insert_data_to_postgres = LocalCsvToPostgresOperator(task_id='insert_data_to_postgres', local_path="plugins/test_project", postgres_conn_id=conn,
                                                         table_name=TABLE_NAME, columns_name=config["columns_name"], contains_substring="flightlist")
    

start_step >> insert_data_to_postgres >> end_step
