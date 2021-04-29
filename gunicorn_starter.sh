#!/bin/sh
gunicorn --log-level $CAR_POOLING_LOG_LEVEL --bind 0.0.0.0:9091 app:app
