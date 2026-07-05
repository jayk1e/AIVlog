#!/usr/bin/env python3
"""
Scaffold a new SERIES (or a new EPISODE in an existing series) under AIVlog/series/.

Every episode is a small config module that imports the shared engine in AIVlog/lib/,
so there's no code to copy and bug fixes are global.

Usage
-----
  # new series, first episode (episode01), 8 clips:
  python lib/new_series.py "bombay-taxi"

  # new series with a chosen clip count:
  python lib/new_series.py "bombay-taxi" --clips 6

  # add another episode to an existing series:
  python lib/new_series.py "bangalore-1970s" --episode 2 --clips 9

Then edit the generated episodeNN.py (NARRATOR + PROMPTS + card text), add refs if
this series needs its own face, and run it. See README.md.
"""
import sys
from pathlib import Path

AIVLOG_ROOT = Path(__file__).resolve().parent.parent
SERIES_ROOT = AIVLOG_ROOT / "series"


def stub_prompts(n):
    lines = ["PROMPTS = ["]
    for i in range(1, n + 1):
        role = ("Opening beat - establish place + the gag." if i == 1
                else "Closing beat - wistful sign-off." if i == n
                else "A new spot along the walk/journey.")
        lines.append(f"    # {i} - {role}")
        lines.append(
            f'    "Selfie-vlog, arm\'s-length camera. {{you}} <ACTION + LOCATION for '
            f'clip {i}; describe camera move>. <lighting/film look>. The narrator says: '
            f'\\"<SPOKEN LINE for clip {i}>.\\" <Ambient sound cue>.",')
        lines.append("")
    lines.append("]")
    return "\n".join(lines)


TEMPLATE = '''#!/usr/bin/env python3
"""
{SERIES} — Episode {EPNUM:02d}.  (config only; engine lives in AIVlog/lib/)

Fill in NARRATOR (match your refs photos) and the {N} PROMPTS, then from this folder:
    ../../.venv/bin/python {SLUG}.py            # test clip 1 (~$0.80)
    ../../.venv/bin/python {SLUG}.py --all      # render all
    ../../.venv/bin/python {SLUG}.py --cards    # render title/end cards
    ../../lib/stitch.sh {SLUG}                  # -> {SERIES}_{SLUG}.mp4
Refs resolve: this folder's refs/ -> series refs/ -> global AIVlog/refs/.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
import veo_engine

SLUG = "{SLUG}"

# EDIT to match your refs photos (hair, beard, glasses, skin, clothing).
NARRATOR = (
    "The narrator is <AGE/GENDER/SKIN>, with <HAIR>, <FACIAL HAIR>, <GLASSES?>, "
    "wearing <CLOTHING>, holding the camera at arm's length (selfie-vlog framing). "
    "Same face as the reference images. Expression relaxed, warm, conversational - "
    "a natural easy smile, NOT wide-eyed. Background signage stays soft and blurred "
    "(no readable text)."
)

# One prompt per 8s clip. Add/remove entries to change the video length.
{PROMPTS}

# Title / end card text.
CARD_TITLE = "{SERIES}"
CARD_SUBTITLE = "<subtitle>"
CARD_END1 = "<end line 1>"
CARD_END2 = "<end line 2>"

if __name__ == "__main__":
    if "--cards" in sys.argv:
        import make_cards
        out = Path(__file__).resolve().parent / "clips" / SLUG
        t, e = make_cards.render(out, title=CARD_TITLE, subtitle=CARD_SUBTITLE,
                                 end_line1=CARD_END1, end_line2=CARD_END2)
        print("wrote", t, "and", e)
    else:
        veo_engine.run(
            __file__,
            narrator=NARRATOR,
            prompts=PROMPTS,
            slug=SLUG,
            # aspect_ratio="16:9",   # uncomment for YouTube landscape
        )
'''


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        sys.exit('Usage: new_series.py "<series-name>" [--episode N] [--clips N]')
    series = args[0]
    n = 8
    epnum = 1
    if "--clips" in args:
        n = int(args[args.index("--clips") + 1])
    if "--episode" in args:
        epnum = int(args[args.index("--episode") + 1])

    series_dir = SERIES_ROOT / series
    slug = f"episode{epnum:02d}"
    ep_file = series_dir / f"{slug}.py"

    new_series = not series_dir.exists()
    if ep_file.exists():
        sys.exit(f"ERROR: {ep_file} already exists. Pick another --episode number.")

    series_dir.mkdir(parents=True, exist_ok=True)
    (series_dir / "clips" / slug).mkdir(parents=True, exist_ok=True)
    if new_series:
        # .gitignore so heavy generated assets don't get committed.
        (series_dir / ".gitignore").write_text("clips/\n*.mp4\n*.mp3\n__pycache__/\n")

    ep_file.write_text(TEMPLATE.format(
        SERIES=series, SLUG=slug, EPNUM=epnum, N=n, PROMPTS=stub_prompts(n)))

    kind = "series + episode" if new_series else "episode"
    print(f"Created {kind}: {ep_file}")
    print(f"  {n} stubbed prompt(s) (~${n*8*0.10:.2f} at Fast/720p when rendered)")
    print("\nNext:")
    if new_series:
        print(f"  - This series uses the GLOBAL face in {AIVLOG_ROOT/'refs'} by default.")
        print(f"    To override, add me1/2/3.jpg to {series_dir/'refs'}/")
    print(f"  1. Edit NARRATOR + PROMPTS + card text in {ep_file}")
    print(f"  2. cd {series_dir}")
    print(f"  3. ../../.venv/bin/python {slug}.py            # test clip 1")
    print(f"  4. ../../.venv/bin/python {slug}.py --all      # render all")
    print(f"  5. ../../.venv/bin/python {slug}.py --cards && ../../lib/stitch.sh {slug}")


if __name__ == "__main__":
    main()
