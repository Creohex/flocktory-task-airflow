FROM python:3.6.8-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install apache-airflow[postgres] \
    && apt-get purge -y --auto-remove gcc python-dev

COPY ./requirements.txt /

RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

COPY ./app/* /app/

WORKDIR /app

ENTRYPOINT ["bash", "start_server.sh"]
