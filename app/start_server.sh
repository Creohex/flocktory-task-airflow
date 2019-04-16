#!/bin/bash
echo "starting server..."

# wait for db to be accessible: ...
python ./wait_for_db.py

# run tests
python ./tests.py

if [ $? == "1" ]; then
    echo "tests failed, skipping airflow server/scheduler..."
    exit 1
fi

# insert logs for testing purposes
if [ "$GENERATE_TEST_LOGS" == "true" ]; then
    python ./db_insert_test_values.py
fi

# init/start server + scheduler
airflow initdb
airflow list_dags
airflow webserver &
airflow scheduler
