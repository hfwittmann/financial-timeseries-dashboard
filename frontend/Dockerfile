FROM python:3.9




ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN apt update && apt-get install -y supervisor
# RUN pip install  kedro-fast-api --no-dependencies
RUN  pip install poetry


RUN mkdir /requirements
RUN poetry config virtualenvs.create false
COPY pyproject.toml /requirements
# COPY poetry.lock /requirements
WORKDIR /requirements
RUN poetry install --only main


COPY .env /
RUN mkdir /app
WORKDIR /app

EXPOSE 8501

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]