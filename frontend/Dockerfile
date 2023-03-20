FROM python:3.9-slim-buster




ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN apt update && apt-get install -y supervisor
RUN pip install  kedro-fast-api --no-dependencies

RUN  pip install poetry

RUN poetry config virtualenvs.create false

COPY .env /
RUN mkdir /app
WORKDIR /app

COPY app /app
COPY pyproject.toml /app
COPY poetry.lock /app

RUN poetry install --only main

EXPOSE 8501
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]