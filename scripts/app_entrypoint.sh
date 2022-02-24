#!/bin/sh

scripts/run_migrations.sh
gunicorn $2 --bind 0.0.0.0:5000 --workers 3 $1:app