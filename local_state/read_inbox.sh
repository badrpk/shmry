#!/bin/bash
echo "📬 --- SHMRY RECENT INBOX ---"
tail -n 20 ~/shmry_core/logs/raw_inbox.log | sed 's/923401083725/LAIBA/g' | sed 's/923335198427/FARIHA/g'
echo "----------------------------"
