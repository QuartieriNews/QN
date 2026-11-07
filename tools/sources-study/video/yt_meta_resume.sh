#!/bin/bash
# slow-paced per-video metadata (sample first, captions downloaded for sample ids); one video a minute; 900 s pause after 2 consecutive failures (HANDOFF §2)
cd "$(dirname "$0")"
sleep ${1:-300}
echo "RESUME $(date -u +%H:%M:%S)" >> yt_meta_all.log
fails=0
while read id; do
  mode=""; grep -qx "$id" sample_ids.txt && mode="cap"
  if [ -s meta/$id.json ] && python3 -c "import json,sys; d=json.load(open('meta/$id.json')); sys.exit(0 if d and d.get('duration') else 1)"; then
    if [ "$mode" = "cap" ] && [ ! -s caps/$id.it.json3 ]; then ./yt_meta.sh $id cap >> yt_meta_all.log 2>&1; sleep 60; fi
    continue
  fi
  ./yt_meta.sh $id $mode >> yt_meta_all.log 2>&1
  if python3 -c "import json,sys; d=json.load(open('meta/$id.json')); sys.exit(0 if d and d.get('duration') else 1)"; then fails=0; else fails=$((fails+1)); fi
  if [ $fails -ge 2 ]; then echo "PAUSE 900s $(date -u +%H:%M:%S)" >> yt_meta_all.log; sleep 900; fails=0; fi
  sleep 60
done < priority_list.txt; echo METADONE $(date -u +%H:%M:%S) >> yt_meta_all.log
