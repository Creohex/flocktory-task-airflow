#!/bin/bash
echo "starting server..."

airflow initdb
airflow list_dags
airflow webserver &
airflow scheduler
