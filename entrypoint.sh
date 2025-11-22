#!/bin/sh
set -e

DB_FILE="receipts.db"

if [ ! -f "$DB_FILE" ]; then
  echo "database not found, initializing..."
  python -m database.init_db
fi

python app.py
