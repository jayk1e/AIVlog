# AIVlog — TODO / Next Steps

## Done
- [x] Bangalore 1970s ep1 (MG Road) — rendered + stitched (~77s).
- [x] Project reorg: shared engine `lib/` + per-episode configs under `series/`.
- [x] GitHub repo (jayk1e/AIVlog) — code + docs pushed, secrets/media gitignored.
- [x] Grand Court Chronicles ep1 (Red Fort 1648) — rendered + stitched (~69s).
- [x] Fixed Veo manic-expression default (firm negative wording in NARRATOR).
- [x] Verified seed-frame vs face-refs are mutually exclusive on this key.
- [x] Continuity files (CONTEXT.md, TODO.md).

## Open / possible next
- [ ] **Review GCC ep1 with sound** — confirm the wry tone lands in Veo's voice.
      Re-roll any clip whose expression still reads off (`episode01.py --clips N`).
- [ ] **Own-voice option?** Decide if any episode should use JK's real voice
      (mute clips, overlay recording) instead of Veo's AI voice. (README has the how.)
- [ ] **Next GCC episode:** Hampi 1510 (diamond markets) — teased in ep1's outro.
      Scaffold with `new_series.py "Grand Court Chronicles" --episode 2`.
- [ ] **Other series from the brief** (not started):
      - Retro India: Bombay 1978 (Bollywood disco), Calcutta 1920s.
      - Everyday Anomalies: Indus Valley / Mohenjo-daro 2500 BCE.
- [ ] **Accuracy escalation when needed:** for a location WITH real reference imagery
      (e.g. a photographable Diwan-i-Khas) where prompting falls short, try a
      seed-framed ESTABLISHING clip (no face) before a face-ref selfie clip. See ACCURACY.md.
- [ ] **Demo output on GitHub?** mp4s are gitignored. If a public demo is wanted,
      attach a finished mp4 to a GitHub Release (don't commit 30MB into git history).

## Known limitations to keep in mind
- Character consistency drifts past ~12–15 chained clips.
- Clips rendered in separate batches can differ slightly in lighting/look.
- Backgrounds sometimes lean generic rather than the specific named landmark.
- A few frames catch open-mouth mid-syllable (unavoidable during speech).
