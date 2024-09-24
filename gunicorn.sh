#!/bin/sh
gunicorn main -b 0.0.0.0:$PORT