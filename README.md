# flocktory-pipeline-task
Interview task (apache airflow, docker compose, postresql)

### Usage:

#### Start/Init database:
       
    docker-compose up


#### run airflow server/scheduler:

a) Build/Run locally:

    bash ./serv.sh build
    bash ./serv.sh run

b) Run using dockerhub image:

    docker run -i -p 8080:8080 -v $(pwd)/app/dags:/root/airflow/dags \
        -e "E=10" -e "PGHOST=localhost" -e "PGUSER=docker" -e "PGPORT=5432" \
        -e "PGPASSWORD=P@ssw0rd" -e "PGDATABASE=main" \
        creohex/flocktory-airflow
