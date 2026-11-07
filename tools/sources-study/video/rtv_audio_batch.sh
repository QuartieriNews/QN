#!/bin/bash
cd ${QN_NET:?export QN_NET=<scratchpad>/net}/video
for spec in "212993 council_II_cfd3a2d1" "213371 comm_II_ab917e2b" "214365 council_XV_26585534"; do
  set -- $spec
  echo "=== $2 $(date -u +%H:%M:%S)" >> rtv/audio/_results.log
  python3 rtv_audio.py "https://ovp2-live.akamaized.net/ac104_video/$1_audio_only.smil" "rtv/audio/$2" >> rtv/audio/_results.log 2>&1
  sleep 5
done
echo "BATCHDONE $(date -u +%H:%M:%S)" >> rtv/audio/_results.log
