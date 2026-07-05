#!/usr/bin/env python3
"""
Bangalore 1970s selfie-vlog — Series: bangalore-1970s, Episode 01 (MG Road).

Config only. The engine lives in AIVlog/lib/veo_engine.py.
Run:
    ../../.venv/bin/python episode01.py            # test clip 1 (~$0.80)
    ../../.venv/bin/python episode01.py --all      # render all 9 (~$7.20)
    ../../.venv/bin/python episode01.py --clips 5  # re-render a drifted clip
Then:
    ../../lib/stitch.sh episode01                  # -> bangalore_ep01.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
import veo_engine

NARRATOR = (
    "The narrator is a South Asian man in his 50s, medium-brown skin, with "
    "wavy salt-and-pepper grey-and-black hair, a short grey-flecked stubble "
    "beard, and rectangular dark-rimmed glasses. He wears a modern charcoal "
    "quarter-zip and jeans, holding the camera at arm's length (selfie-vlog "
    "framing). Same face and glasses as the reference images. His expression is "
    "relaxed, warm and conversational - a natural, easy smile, NOT wide-eyed or "
    "shocked. Background signage and shop signs stay soft, blurred and out of "
    "focus (no sharp readable text)."
)

PROMPTS = [
    # 1 - Arriving
    "Selfie-vlog video, camera held at arm's length. {you} Walking onto a wide, "
    "tree-lined boulevard, Mahatma Gandhi (MG) Road, Bangalore, India, 1975, "
    "looking around amazed and talking to camera. Early morning golden light "
    "through rain trees, a low red-tiled shopping promenade, almost no traffic. "
    "Warm faded 1970s film look, subtle grain. The narrator says: \"I just woke "
    "up on MG Road in Bangalore, and somehow it's nineteen seventy-five. Look at "
    "this. No malls, no honking, just this long tree-lined boulevard and cool "
    "morning air.\" Ambient birdsong.",

    # 2 - Promenade of shops
    "Selfie-vlog, arm's-length camera. {you} Strolling along a covered red-tiled "
    "shopping promenade on 1975 MG Road, Bangalore, gesturing at small storefronts "
    "- a tailor, a watch-repair stall, a Bata shoe shop, a handicrafts emporium "
    "with painted signboards in English and Kannada. A few relaxed pedestrians in "
    "1970s clothing. Warm daylight, vintage film grain. The narrator says: \"This "
    "whole stretch is a red-tiled promenade of little shops - tailors, a watch "
    "repair, a Bata, the Cauvery emporium. And everyone's just strolling. Nobody's "
    "in a hurry.\" Gentle street ambience.",

    # 3 - Higginbothams
    "Selfie-vlog, arm's-length camera. {you} Standing in front of an old "
    "colonial-era bookstore (Higginbothams) on MG Road, Bangalore, 1975, tall "
    "shelves and stacks of books through the doorway, a couple of customers "
    "browsing unhurriedly. Warm interior glow on the pavement, vintage 70s color "
    "and grain. The narrator says: \"Here's Higginbothams. This bookshop's been on "
    "this road longer than India's been independent. People browse for an hour and "
    "buy one book. That's the pace here.\" Quiet ambient sound.",

    # 4 - Traffic
    "Selfie-vlog, arm's-length camera. {you} At the edge of MG Road, Bangalore, "
    "1975, pointing at the near-empty street as a single man cycles past, one cream "
    "Ambassador car rolls by, and a red double-decker bus passes in the background. "
    "Wide leafy road, warm afternoon light, period street signs. 70s film palette, "
    "gentle grain. The narrator says: \"And the traffic? Watch this. One gentleman "
    "on a bicycle. One cream Ambassador. A red double-decker bus. That's it - you "
    "could cross this road with your eyes closed.\" Ambient bicycle bell.",

    # 5 - Lakeview ice cream
    "Selfie-vlog, arm's-length camera. {you} Inside Lakeview Milk Bar on MG Road, "
    "Bangalore, 1975, a charming ice cream parlor, holding a scoop of ice cream and "
    "a tall thick milkshake, talking to camera with a relaxed, happy smile. Retro tiled counter, "
    "glass sundae cups, families enjoying dessert. Warm nostalgic light, 70s film "
    "grain. The narrator says: \"Okay, this is the one I came for - Lakeview Milk "
    "Bar. Fresh ice cream, a proper thick milkshake, about a rupee. This has been "
    "the coolest spot in town for decades.\" Ambient chatter and spoons on glass.",

    # 6 - Plaza Theatre
    "Selfie-vlog, arm's-length camera. {you} In front of the Plaza Theatre "
    "single-screen cinema on MG Road, Bangalore, 1975, a large hand-painted "
    "English-film poster towering above the marquee, a neat orderly queue of "
    "moviegoers in 70s clothing. Early evening light, painted signage and glowing "
    "bulbs, vintage film grain. The narrator says: \"Plaza Theatre - they're "
    "showing an English film, hand-painted board ten feet tall, a neat little queue "
    "out front. On a Saturday evening, this is where the whole city ends up.\" "
    "Ambient crowd murmur.",

    # 7 - Indian Coffee House
    "Selfie-vlog, arm's-length camera. {you} At a marble-topped table inside a "
    "bustling 1975 Indian Coffee House near MG Road, Bangalore, holding a small "
    "steel tumbler of frothy filter coffee, waiters in white uniforms and turbaned "
    "caps in the background, older men chatting animatedly. Warm interior light, "
    "nostalgic film grain. The narrator says: \"Upstairs there's the Indian Coffee "
    "House - waiters in white turbans, twenty-five-paise filter coffee, and "
    "old-timers arguing about cricket for hours. Nobody rushes them out.\" Ambient "
    "clink of steel cups.",

    # 8 - Life on the boulevard
    "Selfie-vlog, arm's-length camera. {you} Walking slowly along the tree-lined MG "
    "Road boulevard, Bangalore, 1975, gesturing at families and couples out for an "
    "unhurried evening stroll under the rain trees, warm low sunlight. Relaxed "
    "nostalgic mood, vintage 70s color and grain. The narrator says: \"And it's "
    "really the pace that gets me. Cool weather all year, everyone knows everyone, "
    "evenings spent walking this boulevard. They call it a pensioner's paradise - I "
    "finally get it.\" Ambient birdsong and soft chatter.",

    # 9 - Closing
    "Selfie-vlog, arm's-length camera. {you} Walking away down MG Road at golden "
    "sunset, holding an ice cream, glancing back at the camera with a wistful smile "
    "and talking to camera. 1975 Bangalore, warm low sun through the rain trees, "
    "the red-tiled promenade and a cinema marquee softly glowing behind. Nostalgic "
    "70s film look, soft grain, gentle lens flare. The narrator says: \"No tech "
    "parks, no start-ups, no traffic jams. Just MG Road, an ice cream, and all the "
    "time in the world. This is Bangalore before it became Bangalore - and I don't "
    "want to go back.\" Ambient birdsong, distant temple bell.",
]

SLUG = "episode01"

# Title / end card text for this episode.
CARD_TITLE = "MG Road"
CARD_SUBTITLE = "Bangalore, 1975"
CARD_END1 = "Bangalore before it"
CARD_END2 = "became Bangalore"

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
