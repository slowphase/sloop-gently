"""The Weather lesson (Lesson 4), verbatim from the verified masters (content.html, id="l4").
Shared by all three concepts. Markup is neutral: <k> button, <kn> knob, <v> on-screen value, <arrow/> for the one arrow.
Nothing here is reworded; each concept only styles and arranges it."""

KICKER = ("L4", "Lesson four", "Atmosphere")
TITLE = "Weather: textures and dust"
TITLE_A, TITLE_B = "Weather:", "textures and dust"
LEAD = ("The secret glue of ambient and lo-fi records is a quiet bed of noise underneath everything: "
        "rain, tape hiss, vinyl crackle. SLOOP generates these for you, without using up a track.")
START_LABEL = "starting from here"
START = ["Any loop playing (Lesson 3's, ideally), or even just a held pad. Any track can be selected; this lesson's settings are global."]
STEPS = [
    "Tap <k>GLO</k> repeatedly until the <v>TEXTURE</v> page shows.",
    "Turn <v>SRC</v> to <v>RAIN</v>. Bring <v>LEVEL</v> up until it sits just under the music. Try the other weathers: "
    "<v>VINYL</v> (hiss, rumble and crackle), <v>TAPE</v>, <v>WIND</v>, <v>RADIO</v>, <v>ROOM</v>.",
    "<v>TONE</v> darkens (left) or thins (right) the bed; <v>MOVE</v> makes it breathe, swelling and receding. "
    "On the next page, <b>TEXTURE 2</b>, <v>RATE</v> sets how long each breath takes, 1 to 16 bars of your tempo.",
    "One more colour: hold <k>FX</k> and turn <kn>KNOB 2</kn>, <v>DUST</v>. It runs the whole mix through an old sampler "
    "and a worn record: softly driven, fewer bits, a little hiss and crackle while the music plays. A small amount warms everything.",
]
HEAR_LABEL = "you should now be hearing"
HEAR = "Your loop sitting inside weather: rain breathing beneath it, a little dust on top. It instantly sounds like a finished record."
SHOT_CAP = ("<b>GLO <arrow/> TEXTURE.</b> A vinyl bed at 63%, darkened with TONE, breathing with MOVE. "
            "The texture is saved with your project, and each song section can carry its own.")
TRY_LABEL = "try this"
TRY = ("Set TEXTURE 2's <v>WHEN</v> to <i>PLAY</i> so the weather fades in and out with the transport: "
       "press <k>PLAY</k> to stop and the rain politely stops with the band.")
MESS_LABEL = "made a mess?"
MESS = ("Everything here is reversible by turning it off: SRC to <v>OFF</v> silences the bed entirely (and costs nothing while off), "
        "DUST back to 0 cleans the mix. Nothing in this lesson records into your loop.")

# Facts allowed on diagram labels, quoted from GUIDE.md at tag v2.8.4 (sections 9, 16, 18) and the verified screenshot.
SOURCES = [("RAIN", "a bed and droplets"), ("VINYL", "hiss, rumble, crackle"), ("TAPE", "dark hiss, drifting"),
           ("WIND", "resonant gusts"), ("RADIO", "bursts of static"), ("ROOM", "room tone")]
TEXTURE_PAGE = [("SRC", "OFF, VINYL, TAPE, RAIN, WIND, RADIO, ROOM, USR1–4"), ("LEVEL", ""), ("TONE", "LP · OFF · HP, left to right"), ("MOVE", "how much it breathes over RATE")]
TEXTURE2_PAGE = [("RATE", "1, 2, 4, 8 or 16 bars"), ("WHEN", "PLAY / ALWAYS"), ("DUCK", "OFF / ON")]
DUST_FACTS = ["FX + KNOB 2", "0–100 %", "drive into a soft clip", "a lower sample rate (down to ~11 kHz)"]
SRC_OFF = "at SRC OFF nothing runs"
PAGE_NO = "TEXTURE 7/8"   # as the screenshot shows it
