# flocktory-pipeline-task
Interview task (apache airflow, docker compose, postresql)

Usage:

I. start / init / migrate database:
       
    docker-compose up


II. run airflow server/scheduler:

a) build/run locally:

    bash ./serv.sh build
    bash ./serv.sh run

b) run from dockerhub image:

    docker run -i -p 8080:8080 -v $(pwd)/app/dags:/root/airflow/dags \
        -e "E=10" -e "PGHOST=localhost" -e "PGUSER=docker" -e "PGPORT=5432" \
        -e "PGPASSWORD=P@ssw0rd" -e "PGDATABASE=main" \
        creohex/flocktory-airflow
