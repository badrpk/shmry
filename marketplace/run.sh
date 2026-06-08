#!/usr/bin/env bash
cd "/home/badrpk/shmry_cloud_hyperscale/marketplace"
exec gunicorn -w 2 -b 0.0.0.0:5060 shmry_marketplace:app
