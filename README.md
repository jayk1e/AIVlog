# AIVlog — AI "time-traveler selfie vlog" generator (Veo 3.1)

Generate narrated, character-consistent selfie-vlog videos of **any length** by
producing a series of 8-second Veo 3.1 clips and stitching them into one file.
Each clip has native synchronized speech (the narrator talks on camera); the face
is locked across clips using up to 3 reference photos.

**Architecture:** one shared engine in `lib/`, and each video is a tiny **episode
config** under `series/<name>/`. Fix a bug in `lib/` once and every series benefits.
See the [directory structure](#directory-structure) at the bottom.

---

## How length works (read this first)

Veo generates in fixed **8-second** clips (8s is required when using reference
images). Length is just **clip count** — one prompt per 8-second beat:

| Target length | Clips | Approx cost (Fast, 720p) |
|---|---|---|
| ~30 s | 4 | ~$3.20 |
| ~60 s | 8 | ~$6.40 |
| ~75 s | 9 | ~$7.20 |
| ~2 min | 15 | ~$12.00 |

To make a video longer, add prompts; shorter, remove some. `stitch.sh` concatenates
the clips in order plus optional title/end cards — that step turns N short clips
into one arbitrary-length video.

> Practical ceiling: consistency drifts the more clips you chain. Past ~12–15,
> expect to re-render several. No hard cap, just cost + drift.

---

## One-time setup (already done here)

To reproduce on a fresh machine:
1. **venv + SDK** (macOS ships `pip3`, not `pip`):
   ```bash
   python3 -m venv .venv
   ./.venv/bin/python -m pip install google-genai python-dotenv pillow
   ```
2. **ffmpeg**: `brew install ffmpeg`.
3. **Paid-tier** Google AI Studio key in `.env` at the repo root:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   > ⚠️ Veo is NOT free tier. Billing must be enabled. See `VEO_API_NOTES.md`.
4. **Global reference photos** in `refs/` as `me1.jpg me2.jpg me3.jpg` (front-facing,
   good light). These are the default face for every series.

The venv, `.env`, and global `refs/` are **shared** — every series/episode uses them
automatically. No per-series setup unless you override (below).

---

## Make a new video

### New series (recommended)
```bash
./.venv/bin/python lib/new_series.py "bombay-taxi"            # 8 clips (default)
./.venv/bin/python lib/new_series.py "bombay-taxi" --clips 6  # set length up front
```
Creates `series/bombay-taxi/episode01.py` — a config stub with `<PLACEHOLDER>`
markers telling you exactly what to fill in. It uses the **global face** in `refs/`
unless you add a `series/bombay-taxi/refs/` of its own.

### Another episode in an existing series
```bash
./.venv/bin/python lib/new_series.py "bangalore-1970s" --episode 2 --clips 9
```
Creates `series/bangalore-1970s/episode02.py`. Episodes live **flat** in the series
folder; each produces its own `<series>_<episodeNN>.mp4`.

---

## The process (per episode)

From inside the series folder (e.g. `cd series/bangalore-1970s`):

1. **Edit the episode config** (`episodeNN.py`): fill in `NARRATOR` (must match your
   refs photos — hair, beard, glasses, clothing), the `PROMPTS` list (one per 8s
   clip, each with a `The narrator says: "…"` line for lip-synced speech), and the
   card text.
2. **Test one clip** (~$0.80):
   ```bash
   ../../.venv/bin/python episode01.py            # renders clip 1 only
   ```
3. **Render all**:
   ```bash
   ../../.venv/bin/python episode01.py --all
   ```
4. **Re-render only what drifted** (saves money — no seed on this key, so each
   re-roll varies, good for fishing for a better take):
   ```bash
   ../../.venv/bin/python episode01.py --clips 5
   ../../.venv/bin/python episode01.py --clips 2,4-6,9
   ```
5. **Make title/end cards**:
   ```bash
   ../../.venv/bin/python episode01.py --cards
   ```
6. **Stitch** → `<series>_<episode>.mp4`:
   ```bash
   ../../lib/stitch.sh episode01              # title + end cards
   ../../lib/stitch.sh episode01 --no-cards   # clips only
   ```

Clips land in `clips/<episode>/clip_NN.mp4`; the final video sits in the series
folder next to the episode config.

---

## Reference photos (the face) — override chain

Refs resolve in this order, first match wins:
1. `series/<name>/<episode>/refs/` — not used by default (episodes are flat), but supported
2. `series/<name>/refs/` — **per-series override** (a different look/person for this series)
3. `refs/` — **global default** (usually you)

So: drop your photos in the global `refs/` once. Only add a `series/<name>/refs/`
when *that series* needs a different face. Max 3 images; front-facing beats profiles.

---

## Config (defaults in `lib/veo_engine.py`, override per-episode)

Pass overrides to `veo_engine.run(...)` in an episode, e.g. `aspect_ratio="16:9"`.

| Setting | Default | Notes |
|---|---|---|
| `model` | `veo-3.1-fast-generate-preview` | Fast=$0.10/s. `veo-3.1-generate-preview`=4×. |
| `aspect_ratio` | `9:16` | `16:9` for YouTube (also set `landscape=True` in the card call). |
| `resolution` | `720p` | `1080p`=$0.12/s on Fast. |
| `duration_seconds` | `8` | Required 8 with reference images. |
| `reference_images` | `me1/2/3.jpg` | Max 3. |

### Fields that FAIL on this key (Vertex/Enterprise-only)
`seed`, `generate_audio` (audio is on by default anyway), `negative_prompt`.
To exclude something, phrase it in the positive prompt ("signage soft/blurred, no
readable text"). Full detail in `VEO_API_NOTES.md`.

---

## Using your own voice
Veo speaks the quoted lines in an AI voice. For your real voice: generate normally,
then in an editor (CapCut/DaVinci/Premiere) mute the clip audio and lay your
recording (or an ElevenLabs clone) over the timeline, aligned to the mouth. Keep
Veo's ambient low underneath for the street sound.

---

## Troubleshooting
- **"only supported in Gemini Enterprise Agent Platform mode"** → a Vertex-only field
  (`seed`/`generate_audio`/`negative_prompt`) slipped in. Remove it.
- **429 / permission on clip 1** → key isn't paid-tier. Enable billing.
- **"No audio"** → first 2.5s (title card) is quiet by design + inline players often
  start muted. Audio is there from clip 1. Verify:
  `ffmpeg -i <file>.mp4 -af volumedetect -f null /dev/null 2>&1 | grep mean_volume`
- **Face drifts** → re-render that clip: `episodeNN.py --clips N`; repeat.
- **Gibberish shop signs** → normal; keep the camera moving. Named landmarks render
  more legibly than generic storefronts.

---

## Directory structure

```
AIVlog/
├── .env                      GEMINI_API_KEY (paid tier)          ← shared, gitignored
├── .venv/                    Python env with google-genai        ← shared
├── .gitignore
├── README.md                 this file
├── VEO_API_NOTES.md          hard-won API quirks (auth, rejected fields, cost)
│
├── lib/                      SHARED ENGINE (all series use this)
│   ├── veo_engine.py         generation logic; run() called by each episode
│   ├── make_cards.py         title/end card renderer (render() function)
│   ├── stitch.sh             stitch one episode:  stitch.sh <episode_slug>
│   └── new_series.py         scaffold a new series or episode
│
├── refs/                     GLOBAL default face (your photos)
│   ├── me1.jpg  me2.jpg  me3.jpg
│   └── _originals/           originals kept for reference
│
└── series/                   ALL VIDEO SERIES live here
    └── bangalore-1970s/      one SERIES (flat: episodes side by side)
        ├── episode01.py      episode config: NARRATOR + PROMPTS + card text
        ├── script.md         narration script / shot notes (template for new eps)
        ├── refs/             (optional) per-series face override — absent = global
        ├── bangalore-1970s_episode01.mp4        ← the finished video
        ├── bangalore-1970s_episode01_audio.mp3  ← extracted audio (optional)
        └── clips/
            └── episode01/    raw per-episode assets (gitignored)
                ├── clip_01.mp4 … clip_09.mp4
                ├── card_00_title.png  card_99_end.png
                └── _work/     transient stitch scratch
```

**Rules of thumb**
- Global/repo-wide (venv, key, engine, global refs) live at the root or in `lib/` and
  `refs/` — accessible to every series.
- Each **series** is a folder in `series/`. Each **episode** is one `episodeNN.py`
  config + its `<series>_<episodeNN>.mp4`, sitting flat together.
- Raw clips are isolated per-episode in `clips/<episode>/` so nothing collides.
