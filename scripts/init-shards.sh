#!/bin/bash
set -e
BASE_DB=${POSTGRES_DB:-mall_gamification}
COUNT=${SHARD_COUNT:-1}
for i in $(seq 0 $((COUNT-1))); do
    DB="${BASE_DB}_shard${i}"
    echo "Creating database ${DB}"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE "$DB";
EOSQL
done
