  FROM python:3.11-slim

  ENV PYTHONPATH=${PYTHONPATH}:${PWD}

  RUN apt update && apt-get install -y supervisor
  RUN pip install uv

  RUN mkdir /requirements
  COPY pyproject.toml uv.lock /requirements/
  WORKDIR /requirements
  RUN uv export --frozen --no-dev --no-emit-project --no-hashes -o requirements.txt && uv pip install --system -r requirements.txt

  COPY .env /
  RUN mkdir /app
  WORKDIR /app

  EXPOSE 8000

  COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

  CMD ["/usr/bin/supervisord"]