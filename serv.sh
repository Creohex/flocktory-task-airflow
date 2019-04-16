#!/bin/bash

if [ -z "$1" ]; then
    echo -e "Manage airflow container.\nUsage: $0 [ build | run | stop ]"
    exit 1
fi

if [ $1 == "build" ]; then
    echo "building airflow server/scheduler..."
    docker build -t=airflow-local .
fi

if [ $1 == "run" ]; then
    echo "running airflow server/scheduler..."

    if [ ! -f ./airflow-server.env ]; then
        echo -e "" > ./airflow-server.env
    fi

    docker rm airflow-local > /dev/null 2>&1

    docker run -d -p 8080:8080 --env-file=./airflow-server.env \
    -v $(pwd)/app/dags:/root/airflow/dags \
    --name="airflow-local" airflow-local

    docker logs -f airflow-local
fi

if [ $1 == "stop" ]; then
    echo "stopping airflow server/scheduler..."
    docker stop airflow-local > /dev/null 2>&1
    docker rm airflow-local > /dev/null 2>&1
fi
