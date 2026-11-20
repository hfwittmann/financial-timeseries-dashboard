# Backend: FastAPI app and the daily 09:00 pipeline run, both under supervisord.
# The code is inside the image; settings (PYTHONPATH) come from the environment at runtime, never
# from a .env file.
FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90

COPY --from=ghcr.io/astral-sh/uv:0.13.9@sha256:d3b601f0c7b118bc1753febf7c41cc80981df678445e0254284eecf84db79a7d /uv /usr/local/bin/uv

RUN apt-get update \
 && apt-get install -y --no-install-recommends supervisor \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock /requirements/
RUN cd /requirements \
 && uv export --frozen --no-dev --no-emit-project --no-hashes -o requirements.txt \
 && uv pip install --system --no-cache -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY kedro-backend /app

# data/ is a volume on the server; the empty folders here seed a new volume with the right owner.
# logs/ and /tmp are tmpfs, because the root filesystem is read-only. HOME=/tmp gives yfinance
# a writable cache folder.
RUN useradd --system --uid 10001 --no-create-home app \
 && mkdir -p /app/data/01_raw /app/data/02_intermediate /app/data/06_models /app/data/09_predictor /app/logs \
 && chown -R app:app /app/data /app/logs
ENV HOME=/tmp PYTHONDONTWRITEBYTECODE=1
USER app
WORKDIR /app

EXPOSE 8000
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
