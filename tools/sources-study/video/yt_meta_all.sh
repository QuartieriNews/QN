#!/bin/bash
cd "$(dirname "$0")"
cut -f4 yt_june_candidates.tsv | tail -n +2 | while read id; do
  [ -s meta/$id.json ] && python3 -c "import json,sys; d=json.load(open('meta/$id.json')); sys.exit(0 if d and d.get('duration') else 1)" && continue
  ./yt_meta.sh $id >> yt_meta_all.log 2>&1
  sleep 1
done; echo METADONE $(date -u +%H:%M:%S) >> yt_meta_all.log
