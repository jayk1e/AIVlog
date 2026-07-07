# Visual accuracy for AIVlog episodes

How to make a Veo 3.1 episode look like the *real* place, not a generic set.
Apply these in order — escalate only when the cheaper rung falls short.

## The ladder (cheapest first)

### Rung 1 — Enrich the prompt (free; do this always)
~70% of the accuracy gain, zero extra steps or cost. In each prompt's location
clause, name **specific real detail**, not generic descriptors:
- **Materials**: "red sandstone outer walls, white marble palace pavilions" beats "a palace".
- **Named architecture**: "the Lahori Gate", "cusped (scalloped) Mughal arches",
  "pietra dura (parchin kari) floral inlay", "the Nahr-i-Bihisht water channel".
- **Named objects**: "the Peacock Throne (Takht-i-Taus), gold legs, jewelled canopy,
  two enamelled peacocks".
- **Documented inscriptions/features**: "an engraved Persian couplet along the wall".

Rule of thumb: if a detail has a proper noun or a known material, use it.

### Rung 2 — Generate an accurate seed frame (nano-banana → image-to-video)
When prompting alone won't nail a hero shot (e.g. the throne reveal), generate a
still with the `nano-banana` skill from a detailed accuracy prompt, then feed it as
the **first frame** via `generate_videos(image=...)`. The clip stays faithful to it.
Use for 1–2 key beats, not every clip. (Verify seed-frame + character reference
images coexist on the Developer-API key before relying on both — see caveat below.)

### Rung 3 — Real public-domain reference images
Only when accurate photos/paintings exist AND rungs 1–2 fall short. Source from:
- **Wikimedia Commons** (Red Fort, Diwan-i-Khas photos — CC/public domain)
- **British Library** (Mughal-era paintings, prints — many public domain)
- **The Met / Smithsonian / Rijksmuseum Open Access** (Mughal miniatures)
Feed as a `reference_images` entry. **Costs a face slot** (max 3 total), so your
narrator's face drifts more — a real tradeoff. Prefer rung 2.

## Decisions per episode (the policy)
- **Accurate references DON'T exist** (e.g. the Peacock Throne, dismantled 1739 —
  only paintings survive) → enrich the prompt from the painted/written record. Rung 1.
- **Accurate references DO exist AND prompting isn't getting there** → escalate to a
  seed frame (rung 2), or public-domain refs (rung 3) if needed.

## Known Veo failure modes for historical scenes
- **Gibberish text** on signs/inscriptions — keep camera moving; don't linger on text.
  Named real inscriptions (e.g. the Diwan-i-Khas couplet) render better than generic signs.
- **Anachronisms** creep in (later architecture, wrong dress) — pin the year and
  materials explicitly in every clip.
- **Scale drift** — state relative scale ("towering", "raised on a low marble plinth").

## Two prompting lessons that repeat (verified on GCC ep1)
1. **Veo defaults to a wide-eyed, manic "excited YouTuber" face.** Vague direction
   ("lively", "reacting naturally") does NOT override it. What works: firm, negative-
   constrained wording in NARRATOR — "calm, composed, dry, relaxed eyes at NORMAL
   openness, faint knowing half-smile, deadpan; NOT wide-eyed, NOT bug-eyed, NOT
   shocked, NOT grinning, NOT an excited YouTuber; eyebrows relaxed and low." This
   flipped the look reliably.
2. **Reference photos beat prompt text for clothing.** If the refs show a t-shirt,
   prompting "wearing a robe" flickers/loses. Keep the narrator's wardrobe consistent
   with the reference images, OR give the series its own refs shot in the target
   costume. Don't script a wardrobe change against t-shirt refs.

## VERIFIED (2026-07-05): seed frame and face refs are MUTUALLY EXCLUSIVE
Tested live on the Developer-API key:
- `image=` seed frame ALONE (image-to-video) → **works**.
- `image=` seed + `reference_images` (face) TOGETHER → **400 "Unsupported video
  generation request"**. It's one OR the other, not both.

Consequence for the ladder:
- **Rung 2 (seed frame) gives you accurate architecture but NO face-locking.** Use it
  ONLY for shots where your face isn't the subject — establishing/wide shots, a hall
  before you step in, B-roll.
- **Any selfie clip where your face must match → reference_images only (Rung 1
  prompt enrichment).** You cannot have both a seeded location and your locked face
  in the same clip.
- Practical pattern: a seed-framed *establishing* clip (accurate hall, no clear face)
  can precede a face-ref *selfie* clip in the same location — the viewer reads them
  as the same place.

## Ep-01 (Red Fort 1648) status
Rung 1 applied throughout. Peacock Throne = no photo exists (dismantled 1739), so
prompt-enriched from the painted record — correct call, no seed frame needed.
