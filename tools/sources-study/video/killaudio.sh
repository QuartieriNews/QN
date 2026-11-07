#!/bin/bash
# stop a running audio batch: anchored patterns so the caller's own shell never matches
for pid in $(pgrep -f "^python3 rtv_audio\.py|^/bin/bash \./rtv_audio_batch"); do kill $pid 2>/dev/null; done
sleep 1
echo "left: $(pgrep -fc "^python3 rtv_audio\.py|^/bin/bash \./rtv_audio_batch")"
