#!/usr/bin/env bash
# Stitch one episode: [title card] + clips + [end card] -> <series>_<slug>.mp4
#
# Cards are pre-rendered PNGs (make_cards.py) because this machine's ffmpeg has
# no drawtext filter; we turn them into short video segments and concat.
#
# Usage (run from inside a series folder, e.g. series/bangalore-1970s/):
#   ../../lib/stitch.sh episode01              # title + end cards
#   ../../lib/stitch.sh episode01 --no-cards   # clips only
#
# Reads clips from   ./clips/<slug>/clip_*.mp4
# Reads cards from    ./clips/<slug>/card_00_title.png , card_99_end.png
# Writes             ./<seriesFolderName>_<slug>.mp4
set -euo pipefail

SLUG="${1:-}"
[ -z "$SLUG" ] && { echo "Usage: stitch.sh <episode_slug> [--no-cards]"; exit 1; }
USE_CARDS=1
[ "${2:-}" = "--no-cards" ] && USE_CARDS=0

# Run relative to the CURRENT working dir (the series folder), not the script dir.
SERIES_DIR="$(pwd)"
SERIES_NAME="$(basename "$SERIES_DIR")"
CLIPS="clips/$SLUG"
WORK="$CLIPS/_work"
OUT="${SERIES_NAME}_${SLUG}.mp4"

[ -d "$CLIPS" ] || { echo "No clips dir: $CLIPS (did you render episode '$SLUG'?)"; exit 1; }
mkdir -p "$WORK"
rm -f "$WORK"/*.mp4 "$CLIPS/_concat_list.txt" 2>/dev/null || true

CARD_SECONDS=2.5
shopt -s nullglob
clips=("$CLIPS"/clip_*.mp4)
if [ "${#clips[@]}" -eq 0 ]; then
  echo "No clip_*.mp4 in $CLIPS. Render the episode first."
  exit 1
fi

first="${clips[0]}"
CW="$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$first" | tr -d '[:space:]')"
CH="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$first" | tr -d '[:space:]')"
FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$first" | awk -F/ '{ if ($2) print $1/$2; else print $1 }')"
[ -z "${CW:-}" ] && { echo "Could not probe clip geometry."; exit 1; }
echo "Episode '$SLUG': ${#clips[@]} clip(s), ${CW}x${CH} @ ${FPS}fps"

card_segment () {  # $1=png $2=out.mp4 $3=ambient src (opt) $4=in|out (opt)
  local png="$1" out="$2" amb="${3:-}" dir="${4:-in}"
  local VF="scale=${CW}:${CH}:force_original_aspect_ratio=decrease,pad=${CW}:${CH}:(ow-iw)/2:(oh-ih)/2:color=0x120e0a,fps=${FPS},format=yuv420p"
  if [ -n "$amb" ] && [ -f "$amb" ]; then
    local AF="volume=0.5,afade=t=${dir}:st=0:d=${CARD_SECONDS}"
    ffmpeg -y -loop 1 -t "$CARD_SECONDS" -i "$png" -t "$CARD_SECONDS" -i "$amb" \
      -vf "$VF" -af "$AF" -map 0:v -map 1:a -c:v libx264 -c:a aac -ar 48000 -shortest "$out" 2>/dev/null
  else
    ffmpeg -y -loop 1 -t "$CARD_SECONDS" -i "$png" \
      -f lavfi -t "$CARD_SECONDS" -i anullsrc=channel_layout=stereo:sample_rate=48000 \
      -vf "$VF" -c:v libx264 -c:a aac -shortest "$out" 2>/dev/null
  fi
}

normalize_clip () { ffmpeg -y -i "$1" -vf "scale=${CW}:${CH},fps=${FPS},format=yuv420p" -c:v libx264 -c:a aac -ar 48000 "$2" 2>/dev/null; }

LIST="$CLIPS/_concat_list.txt"
: > "$LIST"
first_clip="${clips[0]}"
last_clip="${clips[${#clips[@]}-1]}"

if [ "$USE_CARDS" -eq 1 ] && [ -f "$CLIPS/card_00_title.png" ]; then
  card_segment "$CLIPS/card_00_title.png" "$WORK/seg_00_title.mp4" "$first_clip" in
  echo "file '_work/seg_00_title.mp4'" >> "$LIST"
fi

i=0
for c in "${clips[@]}"; do
  seg="$WORK/seg_$(printf '%02d' "$i")_clip.mp4"
  normalize_clip "$c" "$seg"
  echo "file '_work/$(basename "$seg")'" >> "$LIST"
  i=$((i+1))
done

if [ "$USE_CARDS" -eq 1 ] && [ -f "$CLIPS/card_99_end.png" ]; then
  card_segment "$CLIPS/card_99_end.png" "$WORK/seg_99_end.mp4" "$last_clip" out
  echo "file '_work/seg_99_end.mp4'" >> "$LIST"
fi

echo "Concatenating $(wc -l < "$LIST" | tr -d ' ') segment(s)..."
( cd "$CLIPS" && ffmpeg -y -fflags +genpts -f concat -safe 0 -i "_concat_list.txt" -c copy -movflags +faststart "$SERIES_DIR/$OUT" )
echo "Done: $OUT"
