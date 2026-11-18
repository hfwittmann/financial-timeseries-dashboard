# Frontend: the Streamlit dashboard. It finds the backend through HOST (for example
# dax-backend:8000), set in the environment at runtime, never from a .env file.
FROM python:3.11-slim@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535

COPY --from=ghcr.io/astral-sh/uv:0.13.9@sha256:d3b601f0c7b118bc1753febf7c41cc80981df678445e0254284eecf84db79a7d /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock /requirements/
RUN cd /requirements \
 && uv export --frozen --no-dev --no-emit-project --no-hashes -o requirements.txt \
 && uv pip install --system --no-cache -r requirements.txt

COPY app /app

# The root filesystem is read-only on the server; HOME=/tmp (a tmpfs) takes Streamlit's files.
RUN useradd --system --uid 10001 --no-create-home app
ENV HOME=/tmp PYTHONDONTWRITEBYTECODE=1
USER app
WORKDIR /app

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
