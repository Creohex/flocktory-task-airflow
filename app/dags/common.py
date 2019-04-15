import os, psycopg2
from datetime import datetime
from contextlib import contextmanager


def datetime_hour_truncated(dt):
    return dt.replace(minute=0, second=0, microsecond=0)

def is_datetime_hour_trancated(dt):
    return dt.minute == 0 and dt.second == 0 and dt.microsecond == 0

def get_env_vars():
    required_vars = ['PGHOST', 'PGUSER', 'PGPORT', 'PGPASSWORD', 'PGDATABASE', 'E']
    missing_vars = [_ for _ in required_vars if _ not in os.environ.keys()]
    if len(missing_vars) > 0:
        raise Exception("Error: missing required variables: %s" % ', '.join(missing_vars))
    else:
        return {key: os.environ[key] for key in required_vars}

@contextmanager
def get_connection():
    params = get_env_vars()
    connection = psycopg2.connect(host='localhost', port=params['PGPORT'], 
                                  user=params['PGUSER'], password=params['PGPASSWORD'], 
                                  database=params['PGDATABASE'])
    try:
        yield connection
    finally:
        connection.close()

def get_logs(timestamp=datetime_hour_truncated(datetime.now())):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT timestamp, level, message FROM logs "
                           "WHERE timestamp = '%s'" % timestamp)
            return cursor.fetchall()

def write_log(timestamp, level, message):
    try:
        if not is_datetime_hour_trancated(timestamp):
            raise Exception("wrong timestamp arg (%s)" % timestamp)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO logs (timestamp, level, message) "
                               "VALUES ('%s', '%s', '%s')"
                               % (timestamp, level, message))
                conn.commit()
    except Exception as e:
        raise Exception("common::write_log exception: %s" % str(e))

def get_hourly(timestamp=datetime_hour_truncated(datetime.now())):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT hour, level, num_messages "
                           "FROM logs_hourly_stats WHERE timestamp = '%s'"
                           % timestamp)
            return cursor.fetchall()

def write_hourly(timestamp, level, num_messages):
    pass

def get_incidents(timestamp=datetime_hour_truncated(datetime.now())):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT hour, num_errors FROM incidents "
                           "WHERE hour = '%s'"
                           % timestamp)
            return cursor.fetchall()

def write_incident(timestamp, num_errors):
    pass
