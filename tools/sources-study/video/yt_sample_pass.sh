#!/bin/bash
# sample-only pass: one video every 60 s, 15-minute pause after 2 consecutive failures, up to 4 rounds
cd "$(dirname "$0")"
sleep ${1:-60}
echo "SAMPLEPASS $(date -u +%H:%M:%S)" >> yt_meta_all.log
for round in 1 2 3 4; do
  fails=0; missing=0
  while read id; do
    [ -s caps/$id.it.json3 ] && continue
    missing=$((missing+1))
    ./yt_meta.sh $id cap >> yt_meta_all.log 2>&1
    if [ -s caps/$id.it.json3 ]; then fails=0; else fails=$((fails+1)); fi
    if [ $fails -ge 2 ]; then echo "PAUSE 900s $(date -u +%H:%M:%S)" >> yt_meta_all.log; sleep 900; fails=0; fi
    sleep 60
  done < sample_ids.txt
  [ $missing -eq 0 ] && break
  echo "ROUND $round done, missing=$missing $(date -u +%H:%M:%S)" >> yt_meta_all.log
done; echo SAMPLEDONE $(date -u +%H:%M:%S) >> yt_meta_all.log
