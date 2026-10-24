#!/bin/bash
# uso: poll_any.sh <logfile> <runId...>
S=/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad; T=$(cat $S/secrets/apify_org); LOG=$1; shift
while true; do
  active=0; out=""
  for r in "$@"; do
    line=$(curl -sS -H "Authorization: Bearer $T" "https://api.apify.com/v2/actor-runs/$r" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['status'], round(d.get('usageTotalUsd',0),3), d['defaultDatasetId'])" 2>/dev/null || echo "ERR 0 -")
    st=${line%% *}; out="$out$r $line"$'\n'
    case $st in READY|RUNNING|ERR) active=1;; esac
  done
  { date -u +%H:%M:%S; echo "$out"; } > $LOG.tmp; mv $LOG.tmp $LOG
  [ $active = 0 ] && break
  sleep 90
done
echo ALL_DONE >> $LOG
