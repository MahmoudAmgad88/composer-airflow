import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'db_backup',
    default_args=default_args,
    description='db salakawy dag',
    schedule_interval='*/10 * * * *',
    max_active_runs=2,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10)
)

stopvm = BashOperator(
    task_id='stopvm',
    bash_command='gcloud compute instances stop database --project=airflow-composer-392913 --zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    do_xcom_push=False)

create_image = BashOperator(
    task_id='create_image',
    bash_command='gcloud compute machine-images create databaseimage --source-instance=database --project=airflow-composer-392913 --source-instance-zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    do_xcom_push=False)


startvm = BashOperator(
    task_id='startvm',
    bash_command='gcloud compute instances start database --project=airflow-composer-392913 --zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    trigger_rule='one_success',
    do_xcom_push=False)

create_snapshot = BashOperator(
    task_id='create_snapshot',
    bash_command='gcloud compute snapshots create databasesnapshot --source-disk=database --project=airflow-composer-392913 --source-disk-zone=us-west4-b',
    dag=dag,
    trigger_rule='one_failed',
    depends_on_past=False,
    do_xcom_push=False)

stopvm >> create_image >> startvm
create_image >> create_snapshot
create_snapshot >> startvm