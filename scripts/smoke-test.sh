#!/usr/bin/env bash
# Smoke test of the two images, run the way the server runs them: read-only root filesystem, no
# capabilities, no-new-privileges, no code mounted from the host, settings only from the environment.
#   scripts/smoke-test.sh BACKEND_IMAGE FRONTEND_IMAGE
# Runs the pipeline once (needs the internet), starts both containers and checks that the dashboard
# reaches the backend. Exit 0 when every check passes.
set -uo pipefail
backend="$1"; frontend="$2"
run_id="smoke-$$"
log="$(mktemp)"
fail=0
ok()  { printf 'ok    %s\n' "$1"; }
bad() { printf 'FAIL  %s\n' "$1"; fail=1; }
cleanup() {
  docker rm -f "$run_id-backend" "$run_id-frontend" >/dev/null 2>&1
  docker network rm "$run_id" >/dev/null 2>&1
  docker volume rm "$run_id-data" >/dev/null 2>&1
}
trap cleanup EXIT

hardening=(--read-only --cap-drop ALL --security-opt no-new-privileges:true --tmpfs /tmp)
docker network create "$run_id" >/dev/null
docker volume create "$run_id-data" >/dev/null

# 1. Nothing secret or local is baked in, and nothing runs as root.
for image in "$backend" "$frontend"; do
  if docker run --rm --entrypoint sh "$image" -c 'test ! -e /.env && test ! -e /app/.env'; then
    ok "$image has no .env"
  else bad "$image contains a .env file"; fi
  user="$(docker image inspect -f '{{.Config.User}}' "$image")"
  [[ -n "$user" && "$user" != root && "$user" != 0 && "$user" != 0:* ]] \
    && ok "$image runs as user '$user'" || bad "$image runs as root (User='$user')"
done

# 2. The pipeline fills the data volume (the daily 09:00 job runs the same command).
backend_run=(docker run --rm "${hardening[@]}" --tmpfs /app/logs -v "$run_id-data:/app/data"
  -e PYTHONPATH=. "$backend")
if timeout 1200 "${backend_run[@]}" kedro run >"$log" 2>&1; then
  ok "kedro run finished"
else bad "kedro run failed: $(tail -20 "$log")"; fi

# 3. The backend API answers on the internal network.
docker run -d --name "$run_id-backend" --network "$run_id" --network-alias dax-backend \
  "${hardening[@]}" --tmpfs /app/logs -v "$run_id-data:/app/data" -e PYTHONPATH=. \
  -p 127.0.0.1:18000:8000 "$backend" >/dev/null
for _ in $(seq 60); do
  curl -fsS -o /dev/null http://127.0.0.1:18000/Tickerlist_provider?datatype=tickerlist 2>/dev/null && break
  sleep 2
done
if curl -fsS http://127.0.0.1:18000/Tickerlist_provider?datatype=tickerlist | grep -q myData; then
  ok "backend serves the ticker list"
else bad "backend does not answer: $(docker logs --tail 30 "$run_id-backend" 2>&1)"; fi

# 4. The frontend starts and reaches the backend by the name given in HOST.
docker run -d --name "$run_id-frontend" --network "$run_id" "${hardening[@]}" \
  -e HOST=dax-backend:8000 -e PYTHONPATH=. -p 127.0.0.1:18501:8501 "$frontend" >/dev/null
for _ in $(seq 60); do
  [ "$(curl -fsS http://127.0.0.1:18501/_stcore/health 2>/dev/null)" = ok ] && break
  sleep 2
done
[ "$(curl -fsS http://127.0.0.1:18501/_stcore/health 2>/dev/null)" = ok ] \
  && ok "frontend is healthy" || bad "frontend not healthy: $(docker logs --tail 30 "$run_id-frontend" 2>&1)"
if docker exec "$run_id-frontend" python -c \
  'from subs.access_backend import get_tickerlist; assert len(get_tickerlist()) > 0' 2>&1; then
  ok "frontend reaches the backend through HOST"
else bad "frontend cannot load the ticker list from the backend"; fi

exit $fail
