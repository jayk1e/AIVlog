# AIVlog — Project Context (restart here after a context clear)

**What this is:** A generator for AI "time-traveler selfie-vlog" videos using Google
Veo 3.1 (Gemini Developer API). A narrator (you) walks through a photoreal historical
scene, talking to camera; the video is built from stitched 8-second clips with native
synchronized speech, and the narrator's face is locked across clips via reference photos.

## Current state (as of 2026-07-06)
- **Two series exist**, both under `series/`:
  - `bangalore-1970s/` — episode01 "MG Road 1975". **DONE** (`bangalore-1970s_episode01.mp4`, ~77s).
  - `Grand Court Chronicles/` — episode01 "Red Fort, Delhi 1648". **DONE** (`Grand Court Chronicles_episode01.mp4`, ~69s).
- **Architecture:** shared engine in `lib/`, each video is a per-episode config in
  `series/<name>/episodeNN.py`. See README.md for the full structure diagram.
- **Repo:** https://github.com/jayk1e/AIVlog — code + docs only (mp4s, refs, .env gitignored).

## How to make/render (quick reference — full detail in README.md)
```bash
# From a series folder, e.g. cd "series/Grand Court Chronicles"
../../.venv/bin/python episode01.py            # test clip 1 (~$0.80)
../../.venv/bin/python episode01.py --all      # all clips
../../.venv/bin/python episode01.py --clips 5  # re-render one drifted clip
../../.venv/bin/python episode01.py --cards    # title/end cards
../../lib/stitch.sh episode01                  # -> <series>_episode01.mp4
# New series:  ./.venv/bin/python lib/new_series.py "name" --clips 8
```

## Hard-won facts (don't rediscover these — they cost money/time)
1. **Key must be PAID tier.** Veo isn't on the free tier. Key lives in root `.env`
   (copied from Deal_Analyzer). It IS paid-tier and working.
2. **Vertex-only params that FAIL on this key:** `seed`, `generate_audio`,
   `negative_prompt`. Audio is on by default. Fold "avoid X" into the positive prompt.
   (Details: VEO_API_NOTES.md)
3. **Seed frame (`image=`) and face `reference_images` are MUTUALLY EXCLUSIVE** on this
   key. One or the other per clip. Seed frames = accurate location but NO face lock.
   (Details: ACCURACY.md)
4. **Submitting a generate_videos call = a billable job (~$0.80)** the instant it's
   accepted, even if you never poll it. Don't probe field validity by submitting.
5. **Veo defaults to a wide-eyed manic "excited YouTuber" face.** Override with firm
   negative wording in NARRATOR ("calm, deadpan, NOT wide-eyed, NOT bug-eyed…").
6. **Reference photos beat prompt text for clothing.** Can't script a wardrobe change
   against t-shirt refs — the tee wins and flickers. Keep wardrobe consistent with the
   refs, or give a series its own in-costume refs. (Lessons: ACCURACY.md)

## Key docs
- `README.md` — full process, structure, config, troubleshooting.
- `VEO_API_NOTES.md` — API auth + rejected-fields detail.
- `ACCURACY.md` — the accuracy ladder (prompt enrichment → seed frames → PD refs) + prompting lessons.
- `TODO.md` — open items / next steps.
- Auto-memory: `~/.claude/projects/-Users-jkadambiold-.../memory/` (persists across sessions).

## Cost so far (rough)
Bangalore ep1 ~$10 (incl. a $3.20 probe mistake). GCC ep1 ~$14 (incl. re-rolls for
expression + wardrobe fixes, and 2 test clips). Fast/720p = $0.10/s = $0.80 per 8s clip.
