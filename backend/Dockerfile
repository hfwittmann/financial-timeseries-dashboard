# FROM mubuntu:latest
FROM python:3.8

RUN apt update && apt-get install -y supervisor
RUN pip3 install pip-tools

COPY requirements /requirements
RUN pip-compile /requirements/.in --output-file /requirements/.txt
RUN pip install -r requirements/.txt

COPY .env /
COPY app /app
WORKDIR /app


EXPOSE 5000
COPY app/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]