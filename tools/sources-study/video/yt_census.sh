#!/bin/bash
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for pair in I:UCEZtd0d0UV5e8ZCWkNOiNjw III:UChY0aiTcSAD8kPloMkKkEBA IV:UCDkssC9QHfunvVFoWy2F5ww V:UCBuQMoXjwR8re80z3YdcCQQ VI:UCTzjPrb12wVS2Io2QN_Mo0g VII:UCFPJMVjnDQTH-SFy0T8IDng IX:UC6F3Fj68gnOeC1yXU2JOQEA X:UCXqdJyDd_eLFIqr_Hy7N_gA XV:UCtzN-SvgJbm3iQjypGzmzUw; do
  m=${pair%%:*}; c=${pair##*:}
  echo "START $m $c $(date +%T)"
  timeout 1500 yt-dlp -J --playlist-end 150 --dateafter 20260601 --break-on-reject --no-warnings "https://www.youtube.com/channel/$c/videos" > yt_full_$m.json 2> yt_full_$m.err
  echo "END $m $(date +%T) size $(stat -c %s yt_full_$m.json)"
done
echo ALLDONE
