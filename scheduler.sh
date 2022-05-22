#!/bin/sh

alembic upgrade head
python3 src/scheduler.py