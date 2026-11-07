#!/bin/bash
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
i=0
while IFS= read -r q; do i=$((i+1))
  timeout 120 yt-dlp -J --flat-playlist --no-warnings "ytsearch15:$q" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for e in d.get('entries',[]):
    print(repr(sys.argv[1]), '|', e.get('channel') or e.get('uploader'), '|', e.get('channel_id') or e.get('uploader_id'), '|', (e.get('title') or '')[:80])
" "$q"
done <<'Q'
Municipio Roma II commissione 2026
Municipio II Roma consiglio municipale
Municipio Roma VIII commissione
Municipio VIII Roma consiglio 2026
Municipio Roma XI commissione
Municipio XI Roma consiglio municipale 2026
Municipio Roma XII commissione
Municipio XII Roma consiglio 2026
Municipio Roma XIII commissione
Municipio XIII Roma consiglio 2026
Municipio Roma XIV commissione
Municipio XIV Roma consiglio municipale 2026
commissione capitolina Roma Capitale giugno 2026
Assemblea Capitolina seduta giugno 2026
Q
echo SEARCHDONE
