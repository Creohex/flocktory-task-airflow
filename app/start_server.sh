#!/bin/bash
echo "starting server..."

# wait for db to be accessible: ...
python ./wait_for_db.py

# run tests
python ./tests.py

if [ $? == "1" ]; then
    echo "tests failed, skipping airflow server/scheduler..."
else
    # init/start server + scheduler
    airflow initdb
    airflow list_dags
    airflow webserver &
    airflow scheduler
fi
