from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _world():
    return "World"


with DAG(
    dag_id="day_3_at_1800_every_month",
    schedule="0 18 3 * *",
    start_date=timezone.datetime(2023, 5, 1),
    catchup=False,
    tags=["DEB", "2023"],
):

    hello = BashOperator(
        task_id="hello",
        bash_command="echo 'Hello'",
    )

    world = PythonOperator(
        task_id="world",
        python_callable=_world,
    )

    hello >> world