#!/usr/bin/env python3
"""
Grand Court Chronicles — Episode 01.  (config only; engine lives in AIVlog/lib/)

Fill in NARRATOR (match your refs photos) and the 8 PROMPTS, then from this folder:
    ../../.venv/bin/python episode01.py            # test clip 1 (~$0.80)
    ../../.venv/bin/python episode01.py --all      # render all
    ../../.venv/bin/python episode01.py --cards    # render title/end cards
    ../../lib/stitch.sh episode01                  # -> Grand Court Chronicles_episode01.mp4
Refs resolve: this folder's refs/ -> series refs/ -> global AIVlog/refs/.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
import veo_engine

SLUG = "episode01"

# NOTE: clothing is deliberately NOT here - this episode has a wardrobe change
# (modern -> Mughal period dress), so each PROMPT sets the clothing for that beat.
# NARRATOR carries only the constant face/build.
NARRATOR = (
    "The narrator is a South Asian man in his 50s, medium-brown skin, with wavy "
    "salt-and-pepper grey-and-black hair, a short grey-flecked stubble beard, and "
    "rectangular dark-rimmed glasses. Same face and glasses as the reference "
    "images. He holds the camera at arm's length (selfie-vlog framing). "
    "IMPORTANT - his expression is calm, composed and dry: relaxed eyes at a "
    "NORMAL everyday openness, a faint knowing half-smile, understated and "
    "deadpan, like a witty person telling a quiet story. He is NOT wide-eyed, NOT "
    "bug-eyed, NOT shocked, NOT surprised, NOT grinning manically, NOT an excited "
    "YouTuber. Eyebrows relaxed and low. He speaks softly and casually. "
    "Shot on a phone-style selfie camera with slight handheld shake and casual "
    "natural lighting (documentary realism, NOT polished cinematic)."
)

# One prompt per 8s clip. Structure follows the retention framework:
# 1 hook / 2 micro-quest / 3 danger-realisation / 4 wardrobe change /
# 5 modern parallel / 6 spectacle payoff / 7 incident / 8 cliffhanger outro.
# Nuances baked in: broadcast imperfection (handheld shake, confused extras
# glancing at the selfie stick), modern-slang-meets-Mughal-grit dissonance,
# specific period spatial audio, scripted continuity carrying the "guards"
# thread across clips. MODERN clothing clips 1-3, PERIOD dress clips 4-8.
PROMPTS = [
    # 1 - SENSORY SHOCK HOOK (modern clothes, mid-action)
    "Selfie-vlog, phone held at arm's length, handheld and slightly shaky. {you} "
    "wearing a modern charcoal quarter-zip and jeans, ducking low behind a massive "
    "red sandstone gateway (the Lahori Gate, massive fortified red sandstone with "
    "pointed Mughal arches) and peering around it, then flinching back from the "
    "blinding glare off freshly polished white marble pavilions inside. This "
    "is the brand-new Red Fort (Lal Qila), Delhi, 1648, the day it opens - red "
    "sandstone outer walls, gleaming white marble palace buildings within. Turbaned "
    "Mughal guards with spears and sashes stand in the sun-blasted sandstone "
    "courtyard beyond; a couple "
    "of servants glance at the camera, confused by the selfie stick. Harsh midday "
    "sun, real documentary look, slight lens flare. The narrator says, hushed, dry "
    "and amused: \"So I've let myself into Shah Jahan's brand-new Red Fort. It's "
    "sixteen forty-eight, this place opened roughly this morning, and the walls are "
    "so white I genuinely can't look at them. Somebody said 'yes, all of it, "
    "marble' and nobody stopped him.\" Ambient: echoing courtyard, distant "
    "trumpets, guards' boots on stone.",

    # 2 - MICRO-QUEST + slang/grit dissonance (modern clothes)
    "Selfie-vlog, arm's-length phone, handheld shake. {you} in the modern charcoal "
    "quarter-zip, creeping fast along a shaded arcade of cusped (scalloped) Mughal "
    "arches inside the 1648 Red Fort, Delhi, glancing over his shoulder and grinning "
    "at the camera. White marble columns with delicate pietra dura floral inlay "
    "(coloured semi-precious stone flowers), servants carrying trays hurrying past and "
    "staring at him. Warm shade, dusty light shafts, casual realistic look. The "
    "narrator says, low and wry: \"The plan, such as it is: get one look at the "
    "famous Peacock Throne before anyone asks who I am. No tickets, no queue - just "
    "me, my confidence, and roughly four hundred extremely armed men.\" Ambient: "
    "shuffling bare feet, murmured Persian voices, a peacock's distant cry.",

    # 3 - DANGER REALISATION (modern clothes throughout)
    "Selfie-vlog, arm's-length phone, handheld. {you} in the modern charcoal "
    "quarter-zip, pressed flat against a carved marble pillar in the 1648 Red Fort, "
    "Delhi, glancing warily toward two stern turbaned guards down the corridor "
    "who have started to notice him. Tense, whispered energy, dust in warm light. "
    "The narrator whispers to camera, dryly alarmed: \"So it turns out a man in a "
    "quarter-zip rather stands out at the Mughal court. And the penalty for "
    "loitering near the emperor is, and I quote, being trampled by an execution "
    "elephant. So I'm going to keep my head down - ideally attached - and try to "
    "look like I belong.\" Ambient: sharp guard's command in Persian, approaching "
    "footsteps, his own nervous breath.",

    # 4 - SLIPPING DEEPER IN (modern clothes)
    "Selfie-vlog, arm's-length phone, handheld shake. {you} in the modern charcoal "
    "quarter-zip, slipping quietly through a crowd of Mughal nobles in silk and "
    "servants inside the 1648 Red Fort, Delhi, keeping his head low and giving the "
    "camera a wry sideways glance. Warm sunlit white marble, real handheld look. "
    "The narrator says, low and amused: \"Okay - the trick, it turns out, is to "
    "walk like you own the place. Nobody questions a man striding confidently "
    "toward the emperor's hall. Terrible security, honestly. Love it for me.\" "
    "Ambient: rustling silk, a sitar tuning somewhere, courtyard chatter.",

    # 5 - MODERN PARALLEL (modern clothes)
    "Selfie-vlog, arm's-length phone, handheld. {you} in the modern charcoal "
    "quarter-zip, walking through a grand open courtyard of the 1648 Red Fort, Delhi, "
    "gesturing at a royal herald announcing news to a gathered crowd. White marble "
    "fountains, the Nahr-i-Bihisht (Stream of Paradise) water channel running "
    "through carved marble, nobles in silk listening. Bright sun, realistic "
    "documentary feel, background people occasionally glancing at the camera. The "
    "narrator says, amused: \"Now, no phones here, obviously - so that gentleman "
    "shouting himself hoarse? That's the news. The entire empire's headlines, "
    "delivered by one man with excellent lungs. Honestly, not the worst version of "
    "a feed I've seen.\" Ambient: herald's booming voice, trickling fountain water, "
    "pigeons.",

    # 6 - SPECTACLE PAYOFF - the Peacock Throne (modern clothes)
    "Selfie-vlog, arm's-length phone, handheld. "
    "{you} in the modern charcoal quarter-zip, edging into the Diwan-i-Khas (Hall of "
    "Private Audience) of the 1648 Red Fort, Delhi - a white marble hall of cusped "
    "arches, pillars covered in pietra dura floral inlay, gilded and painted "
    "ceiling, an engraved Persian couplet running along the top of the wall - and "
    "gasping at the legendary golden Peacock Throne (Takht-i-Taus) raised on gold "
    "legs under a jewelled canopy on pillars, two enamelled peacocks with "
    "outspread tails behind it, encrusted with rubies, emeralds and diamonds "
    "catching the light. Cool shadowed hall, shafts of light, awestruck realism. "
    "The narrator whispers, quietly floored: "
    "\"And there it is. The Peacock Throne. Give or take, the single most valuable "
    "thing on the planet at this exact moment - and I'm filming it on a phone, in a "
    "fleece, like some kind of tourist. Somehow that feels right.\" Ambient: "
    "hushed echoing hall, faint courtly music, his awed breath.",

    # 7 - THE INCIDENT (modern clothes, caught)
    "Selfie-vlog, arm's-length phone, very shaky, half-turned as if fleeing. {you} "
    "in the modern charcoal quarter-zip, being firmly grabbed by the sleeve and "
    "shooed away by an angry court eunuch and a spear-carrying guard in the "
    "Diwan-i-Khas of the 1648 Red Fort, Delhi, the Peacock Throne blurring behind "
    "him. Chaotic handheld motion, harsh light. The narrator, dryly panicking, to "
    "camera: \"Ah. Yes. Apparently one does not simply film the emperor's throne - "
    "noted, noted, I'm leaving. Hands off the fleece, sir, it's the only one I "
    "brought.\" Ambient: sharp angry shouting in Persian, scuffling feet, a spear "
    "butt cracking on marble.",

    # 8 - CLIFFHANGER OUTRO (period dress, fleeing)
    "Selfie-vlog, arm's-length phone, handheld and bouncing as he hurries. {you} in "
    "the modern charcoal quarter-zip, speed-walking out through a red sandstone "
    "archway of the 1648 Red Fort, Delhi, glancing back over his shoulder at "
    "pursuing guards, then giving the camera a wry look. Bright exit into harsh sun, dust, "
    "real documentary look. The narrator says, breathless but wry: \"Right, the "
    "guards and I have reached a difference of opinion, so I'll be leaving - but "
    "that? Richest court on Earth, sixteen forty-eight. Not bad for a morning's "
    "trespassing. Next time: the diamond markets of Hampi, fifteen-ten. Do "
    "subscribe - I may not survive the elephant.\" Ambient: pounding footsteps, "
    "shouting guards, a blaring Mughal war trumpet.",
]

# Title / end card text.
CARD_TITLE = "The Red Fort"
CARD_SUBTITLE = "Delhi, 1648"
CARD_END1 = "Next stop: Hampi, 1510"
CARD_END2 = "Subscribe"

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
