from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from dateutil import parser
import psycopg2, os, common, traceback, sys


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': common.datetime_hour_truncated(datetime.now()).replace(hour=0),
    'start_date': parser.parse('2019-04-15 01:00:00'),
    'email': ['example@mailbox.flock'],
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
        recap = 'recap:'
        ts = common.datetime_hour_truncated(parser.parse(kwargs['ts'])) # scheduled hour
        logs = common.select_logs(ts)
        for level, in common.select_log_levels():
            num_messages = len(list(filter(lambda x: x[1] == level, logs)))
            common.insert_hourly(ts, level, num_messages)
            recap += '\n%s: %s' % (level, num_messages)
        return "Done calculating hourly logs (for: %s).\n\n%s" % (ts, recap)
    except Exception as e:
        return "Error in 'analyze_hourly'. Info: \n\n%s\n\n%s" % (str(e), traceback.format_exc())

def analyze_indicents(ds, **kwargs):
    try:
        ts = common.datetime_hour_truncated(parser.parse(kwargs['ts'])) # scheduled hour
        E = int(os.environ['E'])
        hourly = common.select_hourly(ts)
        num = next((_ for _ in hourly if _[1] == "ERROR"), 0)[2]
        if num > E:
            common.insert_incident(ts, num)
        return "Done analyzing indicents."
    except Exception as e:
        return "Error in 'analyze_incidents'. Info: \n\n%s\n\n%s" % (str(e), traceback.format_exc())

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
