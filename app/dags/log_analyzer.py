from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from dateutil import parser
import psycopg2
import common


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': common.datetime_hour_truncated(datetime.now()).replace(hour=0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'pool': 'backfill',
}

dag = DAG('log_analyzer', default_args=default_args, 
          schedule_interval=timedelta(hours=1))

def analyze_hourly(ds, **kwargs):
    try:
        ts = parser.parse(kwargs['ts'])
        # TODO: ...
        return "hourly results..."
    except Exception as e:
        return "Error in 'analyze_hourly'. Info: \n\n%s" % str(e)

def analyze_indicents(ds, **kwargs):
    try:
        ts = parser.parse(kwargs['ts'])
        # TODO: ...
        return "incident results..."
    except Exception as e:
        return "Error in 'analyze_incidents'. Info: \n\n%s" % str(e)

hourly_analyzer = PythonOperator(
    task_id="hourly_analyzer",
    provide_context=True,
    python_callable=analyze_hourly,
    dag=dag)

indicent_analyzer = PythonOperator(
    task_id="incident_analyzer",
    provide_context=True,
    python_callable=analyze_indicents,
    dag=dag)

indicent_analyzer.set_upstream(hourly_analyzer)
