#!/usr/bin/env bash
set -euo pipefail
NAME="$1"
VALUE="$2"
ROOT="$HOME/shmry_cloud_hyperscale"
mkdir -p "$ROOT/secrets"
printf "%s" "$VALUE" | openssl enc -aes-256-cbc -pbkdf2 -salt -out "$ROOT/secrets/$NAME.enc"
echo "secret stored: secrets/$NAME.enc"
