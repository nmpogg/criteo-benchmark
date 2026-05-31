#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

HDFS_LAKE_ROOT="/user/ctr/lake"
ZONES=("raw_events" "processed_features" "predictions" "marts")

echo "Creating HDFS lake root: ${HDFS_LAKE_ROOT}"
docker compose exec -T hdfs-namenode hdfs dfs -mkdir -p "${HDFS_LAKE_ROOT}"

for zone in "${ZONES[@]}"; do
  local_path="data/lake/${zone}"
  hdfs_path="${HDFS_LAKE_ROOT}/${zone}"

  if [[ ! -d "${local_path}" ]]; then
    echo "Skip ${zone}: ${local_path} does not exist yet"
    continue
  fi

  echo "Sync ${local_path} -> hdfs://${hdfs_path}"
  docker compose exec -T hdfs-namenode hdfs dfs -rm -r -f "${hdfs_path}" >/dev/null 2>&1 || true
  docker compose exec -T hdfs-namenode hdfs dfs -put "/host_data/lake/${zone}" "${hdfs_path}"
done

echo "Create/repair Hive external tables"
docker compose exec -T hive-server beeline \
  -u jdbc:hive2://localhost:10000/default \
  -f /opt/hive/scripts/ctr_lake_tables.sql

echo "HDFS lake layout"
docker compose exec -T hdfs-namenode hdfs dfs -ls "${HDFS_LAKE_ROOT}"
