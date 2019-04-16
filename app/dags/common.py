import os, psycopg2
from datetime import datetime


def datetime_hour_truncated(dt):
    """ Remove minutes/seconds/microseconds from datetime object """
    return dt.replace(minute=0, second=0, microsecond=0)

def is_datetime_hour_truncated(dt):
    """ Verify that datetime object has 
        minutes/seconds/microseconds set to 0 """
    return dt.minute == 0 and dt.second == 0 and dt.microsecond == 0

def get_env_vars():
    """ Return dict containing required environemnt variables """
    required_vars = ['PGHOST', 'PGUSER', 'PGPORT', 
                     'PGPASSWORD', 'PGDATABASE', 'E']
    missing_vars = [_ for _ in required_vars if _ not in os.environ.keys()]
    if len(missing_vars) > 0:
        raise Exception("Error: missing required variables: %s" 
                        % ', '.join(missing_vars))
    else:
        return {key: os.environ[key] for key in required_vars}

def get_connection():
    """ Return connection based on current environment variables """
    params = get_env_vars()
    return psycopg2.connect(host=params['PGHOST'], port=params['PGPORT'], 
                user=params['PGUSER'], password=params['PGPASSWORD'], 
                database=params['PGDATABASE'])

def query_db(query_str):
    """ Execute db query and return results """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_str)
                conn.commit()
                try:
                    return cursor.fetchall()
                except Exception:
                    return []
    except psycopg2.DatabaseError as e:
        raise Exception("query_db error:\n%s" % str(e))

def select_log_levels():
    """ Return existing log levels """
    return query_db("SELECT level FROM level")

def select_logs(ts=datetime_hour_truncated(datetime.now())):
    """ Return log records for a given hour """
    if not is_datetime_hour_truncated(ts):
        raise Exception("wrong timestamp arg (%s)" % ts)
    return query_db(
        "SELECT timestamp, level, message FROM logs "
        "WHERE timestamp::date = '%s'::timestamp::date "
        "AND extract(hour from timestamp) = extract(hour from '%s'::timestamp)"
        % (ts, ts))

def insert_log(timestamp, level, message):
    """ Insert new logs table record """
    return query_db("INSERT INTO logs (timestamp, level, message) VALUES "
                    "('%s', '%s', '%s')" % (timestamp, level, message))

def select_hourly(timestamp=datetime_hour_truncated(datetime.now())):
    """ Return logs_hourly_stats records for a given hour """
    return query_db("SELECT hour, level, num_messages "
                    "FROM logs_hourly_stats WHERE hour = '%s'"
                    % timestamp)

def insert_hourly(timestamp, level, num_messages):
    """ Insert new logs_hourly_stats table record """
    if not is_datetime_hour_truncated(timestamp):
        raise Exception("wrong timestamp arg (%s)" % timestamp)
    return query_db(
        "INSERT INTO logs_hourly_stats (hour, level, num_messages) VALUES "
        "('%s', '%s', %s)" % (timestamp, level, num_messages))

def select_incidents(timestamp=datetime_hour_truncated(datetime.now())):
    """ Return incidents records for a given hour """
    return query_db("SELECT hour, num_errors FROM incidents WHERE hour = '%s'"
                    % timestamp)

def insert_incident(timestamp, num_errors):
    """ Insert new incidents table record """
    if not is_datetime_hour_truncated(timestamp):
        raise Exception("wrong timestamp arg (%s)" % timestamp)
    return query_db(
        "INSERT INTO incidents (hour, num_errors) VALUES ('%s', %s)" 
        % (timestamp, num_errors))
