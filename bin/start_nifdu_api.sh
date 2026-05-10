#!/usr/bin/env bash
source "/home/badrpk/shmry_cloud_hyperscale/venv/bin/activate"
exec gunicorn -w 2 -b 0.0.0.0:5000 nifdu_api_www:app --chdir "/home/badrpk/shmry_cloud_hyperscale/bin" --access-logfile "/home/badrpk/shmry_cloud_hyperscale/logs/api_access.log" --error-logfile "/home/badrpk/shmry_cloud_hyperscale/logs/api_error.log"
