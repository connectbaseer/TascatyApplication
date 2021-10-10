#!/bin/bash
NAME="Tascaty"
cd /apps/tascaty
gunicorn tascaty_project.wsgi:application --bind 0.0.0.0:8000 --name $NAME