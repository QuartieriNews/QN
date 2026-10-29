#!/bin/bash
S=/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad; T=$(cat $S/secrets/apify_org)
RUNS="danHMaCdbPdPIyFMS 2ruTebBWAZ5Rw9Frb cTOkvbmVHLcHkMAU0 aCShgbn0dB4ZOD2MY dYdSFLqGUFkbqmEQq"
while true; do
  active=0; out=""
  for r in $RUNS; do
    line=$(curl -sS -H "Authorization: Bearer $T" "https://api.apify.com/v2/actor-runs/$r" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['status'], d.get('usageTotalUsd',0), d['defaultDatasetId'])")
    st=${line%% *}; out="$out$r $line"$'\n'
    case $st in READY|RUNNING) active=1;; esac
  done
  date -u +%H:%M:%S; echo "$out"
  [ $active = 0 ] && break
  sleep 60
done
echo ALL_DONE
