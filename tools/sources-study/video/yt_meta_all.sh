#!/bin/bash
cd "$(dirname "$0")"
# un video al minuto, 15 minuti di pausa dopo due errori di fila (HANDOFF §2, come yt_all_pass.sh)
fails=0
cut -f4 yt_june_candidates.tsv | tail -n +2 | while read id; do
  [ -s meta/$id.json ] && python3 -c "import json,sys; d=json.load(open('meta/$id.json')); sys.exit(0 if d and d.get('duration') else 1)" && continue
  ./yt_meta.sh $id >> yt_meta_all.log 2>&1
  if python3 -c "import json,sys; d=json.load(open('meta/$id.json')); sys.exit(0 if d and d.get('duration') else 1)" 2>/dev/null; then fails=0; else fails=$((fails+1)); fi
  if [ $fails -ge 2 ]; then echo "PAUSE 900s $(date -u +%H:%M:%S)" >> yt_meta_all.log; sleep 900; fails=0; fi
  sleep 60
done; echo METADONE $(date -u +%H:%M:%S) >> yt_meta_all.log
