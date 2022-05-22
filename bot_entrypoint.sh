#!/bin/sh

alembic upgrade head
python3 src/bot_handler.py