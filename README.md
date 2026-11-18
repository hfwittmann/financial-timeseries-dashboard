# financial-timeseries-dashboard
This post is very much about technology integration. Its aim is to build a dashboard that allows the display of financial timeseries of multiple stocks simultaneously.

This repo is used and described in the following blog post: https://arthought.com/financial-timeseries-dashboard/

To run it locally (needs Docker with Compose):

````
docker compose up --build -d
````

No `.env` file is needed: the settings (`HOST`, `PYTHONPATH`) are in `docker-compose.yml`. The first
start has no data yet; fill it once with

````
docker compose exec dax-backend kedro run
docker compose restart dax-backend
````

After that the backend refreshes the data every day at 09:00.

The images for the server are built by GitHub Actions (`.github/workflows/images.yml`), checked by
`scripts/smoke-test.sh` and pushed to `ghcr.io/hfwittmann/financial-timeseries-dashboard/backend` and
`.../frontend`. The server pulls them by digest and never builds.

The dashboard is then at http://localhost:8501. The backend has no published port; its API is only
reachable from the frontend, inside the Compose network.