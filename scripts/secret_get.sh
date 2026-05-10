#!/usr/bin/env bash
set -euo pipefail
NAME="$1"
ROOT="$HOME/shmry_cloud_hyperscale"
openssl enc -d -aes-256-cbc -pbkdf2 -in "$ROOT/secrets/$NAME.enc"
