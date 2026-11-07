#!/bin/bash
# usage: yt_meta.sh <id> [cap]  -> meta/<id>.json via the first player client that returns captions/duration; caps/<id>.it.json3 when "cap"
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=/root/.ccr/ca-bundle.crt CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt
id=$1; mkdir -p meta caps
for c in android tv_simply; do
  timeout 180 yt-dlp -J --skip-download --ignore-no-formats-error --no-warnings --extractor-args "youtube:player_client=$c" --extractor-args "youtube:lang=it" "https://www.youtube.com/watch?v=$id" > meta/$id.json 2> meta/$id.err
  ok=$(python3 -c "
import json,sys
try: d=json.load(open('meta/$id.json'))
except Exception: print('bad'); sys.exit()
print('ok' if d and d.get('duration') else 'nodur')
")
  echo "$id client=$c $ok" >> meta/_log.txt
  [ "$ok" = "ok" ] && break
  sleep 2
done
python3 - "$id" "$2" <<'PY'
import json,sys,subprocess
id,mode=sys.argv[1],sys.argv[2] if len(sys.argv)>2 else ''
d=json.load(open(f'meta/{id}.json')) or {}
ac=d.get('automatic_captions') or {}; subs=d.get('subtitles') or {}
def pick(m):
    for k in ('it','it-orig','it-IT'):
        if k in m:
            for f in m[k]:
                if f.get('ext')=='json3': return f['url']
    return ''
u=pick(subs) or pick(ac)
print(id, 'upload=',d.get('upload_date'),'dur=',d.get('duration'),'live=',d.get('live_status'),'subs=',','.join(subs.keys()) or '-','auto_it=',bool(pick(ac)))
if mode=='cap' and u:
    r=subprocess.run(['curl','-sS','-o',f'caps/{id}.it.json3','-w','%{http_code} %{size_download}',u],capture_output=True,text=True)
    try:
        json.load(open(f'caps/{id}.it.json3')); print(id,'CAP',r.stdout)
    except Exception:
        import os; os.remove(f'caps/{id}.it.json3'); print(id,'CAP_BLOCKED',r.stdout)
PY
