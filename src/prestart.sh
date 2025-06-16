#!/usr/bin/env bash

set -e

echo "Try apply migrations"
cd src
python -m alembic upgrade head
echo "Migrations complete"
cd ..

exec "$@"