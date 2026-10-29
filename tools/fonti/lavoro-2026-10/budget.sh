#!/bin/bash
# uso: budget.sh <stima_usd>  -> stampa il margine e esce 1 se spesa_mese + stima supera CAP (159 dal 25 ottobre: +12 $ per il secondo giro dei post e il resto se la differenza è minima, approvati dall'owner)
S=/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad; T=$(cat $S/secrets/apify_org)
curl -sS -H "Authorization: Bearer $T" https://api.apify.com/v2/users/me/limits | python3 -c "
import sys,json; u=json.load(sys.stdin)['data']['current']['monthlyUsageUsd']; est=float(sys.argv[1]); ok=u+est<=159
print(f'spesa {u:.2f} + stima {est:.2f} = {u+est:.2f} / 159 -> {\"OK\" if ok else \"STOP\"}'); sys.exit(0 if ok else 1)" "$1"
