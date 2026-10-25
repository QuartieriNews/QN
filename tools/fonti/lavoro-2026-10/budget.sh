#!/bin/bash
# uso: budget.sh <stima_usd>  -> stampa il margine e esce 1 se spesa_mese + stima supera 150
S=/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad; T=$(cat $S/secrets/apify_org)
curl -sS -H "Authorization: Bearer $T" https://api.apify.com/v2/users/me/limits | python3 -c "
import sys,json; u=json.load(sys.stdin)['data']['current']['monthlyUsageUsd']; est=float(sys.argv[1]); ok=u+est<=150
print(f'spesa {u:.2f} + stima {est:.2f} = {u+est:.2f} / 150 -> {\"OK\" if ok else \"STOP\"}'); sys.exit(0 if ok else 1)" "$1"
