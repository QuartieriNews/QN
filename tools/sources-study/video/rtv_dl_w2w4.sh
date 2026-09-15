#!/bin/bash
cd ${QN_NET:?export QN_NET=<scratchpad>/net}/video
echo "START $(date -u +%H:%M:%S)" >> rtv/audio/_dl_w2w4.log
cut -f1,2 rtv/audio/_list_w2w4.tsv | xargs -P 4 -L 1 bash -c 'python3 rtv_audio.py "$0" "rtv/audio/comm_$1" >> "rtv/audio/_dl_$1.log" 2>&1; echo "DONE $1 $(date -u +%H:%M:%S) rc=$?" >> rtv/audio/_dl_w2w4.log'
echo "ALLDONE $(date -u +%H:%M:%S)" >> rtv/audio/_dl_w2w4.log
