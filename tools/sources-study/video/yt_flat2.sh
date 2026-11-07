#!/bin/bash
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for pair in I:UCEZtd0d0UV5e8ZCWkNOiNjw III:UChY0aiTcSAD8kPloMkKkEBA IV:UCDkssC9QHfunvVFoWy2F5ww V:UCBuQMoXjwR8re80z3YdcCQQ VI:UCTzjPrb12wVS2Io2QN_Mo0g VII:UCFPJMVjnDQTH-SFy0T8IDng IX:UC6F3Fj68gnOeC1yXU2JOQEA X:UCXqdJyDd_eLFIqr_Hy7N_gA XIV:UC_XtcIeCkpWjt3U5t_k7QVw XV:UCtzN-SvgJbm3iQjypGzmzUw CCMOB:UCXHyBiqY5a3gxhlOEeFcjnA RC:UCCQygqTutREYU9AbTHfHhTw MUNROMA:UCdL4K4vJi_rcuY35SiaOZOA; do
  m=${pair%%:*}; c=${pair##*:}
  for tab in videos streams; do
    timeout 600 yt-dlp -J --flat-playlist --playlist-end 600 --no-warnings --extractor-args "youtube:lang=it" --extractor-args "youtubetab:approximate_date" "https://www.youtube.com/channel/$c/$tab" > yt_flat_${m}_${tab}.json 2> yt_flat_${m}_${tab}.err
    echo "$m $tab rc=$? size=$(stat -c %s yt_flat_${m}_${tab}.json) $(date -u +%H:%M:%S)"
  done
done; echo ALLDONE $(date -u +%H:%M:%S)
