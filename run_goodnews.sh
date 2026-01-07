#!/bin/sh
cd /home/fabrice/goodnews || exit 1
/home/fabrice/goodnews/venv/bin/python /home/fabrice/goodnews/daily_good_news.py >> /home/fabrice/goodnews/logs/anacron.log 2>&1
