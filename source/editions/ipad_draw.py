"""Tall redraws for the iPad mini edition: the drawings that are wide strips on A4 become stacked, larger-lettered
versions for a 110 mm column. Facts are the same as the A4 drawings (which were verified against GUIDE.md v2.8.4)."""
import math
NIGHT, CARD, LIME, INK, INK2, INK3 = "#0e0e10", "#19191c", "#d4ff3a", "#ede8dc", "#d4cfc3", "#b9b5aa"
WASH, LINE = "#232327", "#2f2f35"
T1, T4 = "#2f6fde", "#e2661d"
W = 352
FLOOR = 8.0   # smallest label in drawing units: 8/352 of a ~122 mm drawing is about 7.1 pt on the iPad mini's screen

def wrap(text, maxchars):
    words = text.split(); lines = []; cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxchars: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def T(x, y, t, sz=8, w=400, fill=INK2, anchor="start", fam=None):
    sz = max(sz, FLOOR)
    f = f' font-family="{fam}"' if fam else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz:.1f}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}"{f}>{t}</text>'

def para(o, x, y, text, maxchars, sz=7.6, fill=INK2, lh=None):
    sz = max(sz, FLOOR)
    lh = lh or sz * 1.3
    for ln in wrap(text, maxchars):
        o.append(T(x, y, ln, sz, 400, fill)); y += lh
    return y

def svg(h, o): return f'<svg viewBox="0 0 {W} {int(h)}" width="100%">' + "".join(o) + "</svg>"

# ------------------------------------------------------------------ ch2: install, five steps stacked
def install_flow():
    steps = [("Chrome or Edge", "the installer page"), ("a data cable", "straight in, no hub"),
             ("INSTALL", "allow MIDI access"), ("wait for Done", "cable untouched"), ("SLOOP logo", "the FM-1 restarts")]
    o = []; y = 4; bh = 26
    for i, (a, b) in enumerate(steps):
        dark = a == "INSTALL"
        o.append(f'<rect x="30" y="{y}" width="{W-30}" height="{bh}" rx="5" fill="{INK if dark else CARD}" stroke="{INK3}" stroke-width="{0 if dark else .7}"/>')
        o.append(T(14, y + 18, str(i + 1), 18, 900, INK, "middle", "Big Shoulders"))
        o.append(T(42, y + 11.5, a, 10, 600, NIGHT if dark else INK))
        o.append(T(42, y + 21.5, b, 8, 400, "#4a4a44" if dark else INK2))
        if i < 4: o.append(f'<path d="M{W/2+15},{y+bh+1} L{W/2+15},{y+bh+5}" stroke="{INK3}" stroke-width="1"/>')
        y += bh + 6
    y = para(o, 0, y + 6, "The one rule: never unplug or switch off while an install is running.", 70, 8, INK)
    y = para(o, 0, y + 1, "Interrupted anyway? The FM-1 waits in update mode; press INSTALL again.", 70, 7.6, INK2)
    return svg(y, o)

# ------------------------------------------------------------------ L3: the free take, two bars (replaces the 176×30 strip)
def free_take():
    o = []
    o.append(T(0, 9, "bar 1 · press REC, then play", 7.6, 600, INK3))
    o.append(T(W, 9, "bar 2 · keep playing", 7.6, 600, INK3, "end"))
    bw = (W - 44) / 2
    for b in range(2):
        x = b * (bw + 6)
        o.append(f'<rect x="{x}" y="14" width="{bw}" height="30" rx="4" fill="none" stroke="{T1}" stroke-width="1.4"/>')
        for k in range(4):
            o.append(T(x + (k + .5) * bw / 4, 33, str(k + 1), 10, 600, T1, "middle"))
    o.append(f'<circle cx="{W-14}" cy="29" r="13" fill="#c0392b"/>' + T(W - 14, 32.5, "REC", 7.4, 700, "#fff", "middle"))
    o.append(T(W - 14, 56, "press on this “1”", 7.4, 600, "#e07b6f", "end"))
    o.append(T(W - 14, 65, "and the loop closes", 7.2, 400, INK2, "end"))
    return svg(72, o)

# ------------------------------------------------------------------ L8: length & division, the slow-music trick, stacked
def slow_music():
    o = []
    o.append(f'<rect x="0" y="2" width="16" height="14" rx="3" fill="{T1}"/>' + T(8, 12.5, "1", 9, 600, "#fff", "middle"))
    o.append(T(22, 9, "pad · DIV 1BAR · LENGTH 4", 8, 600, INK))
    o.append(T(22, 19, "four steps, each lasting a whole bar", 7.4, 400, INK2))
    X0, BW = 0, W / 4
    for i, key in enumerate((5, 10, 8, 9)):
        x = X0 + i * BW
        o.append(f'<rect x="{x+1}" y="26" width="{BW-14}" height="26" rx="4" fill="{T1}"/>')
        o.append(f'<rect x="{x+BW-15}" y="26" width="13" height="26" fill="{T1}" opacity=".35"/>')
        o.append(T(x + 6, 37, f"step {i+1}", 8, 600, "#fff"))
        o.append(T(x + 6, 47, f"chord of key {key}", 7, 400, "#dfe8fa"))
        o.append(T(x + 2, 62, f"bar {i+1}", 7, 400, INK3))
    o.append(f'<rect x="0" y="74" width="16" height="14" rx="3" fill="{T4}"/>' + T(8, 84.5, "4", 9, 600, "#fff", "middle"))
    o.append(T(22, 81, "drums · DIV 1/16 · LENGTH 64", 8, 600, INK))
    o.append(T(22, 91, "sixteen steps a bar, four bars, ticking underneath", 7.4, 400, INK2))
    for k in range(64):
        x = k * W / 64 + .8; tall = k % 4 == 0
        h = 16 if tall else 9
        o.append(f'<rect x="{x:.1f}" y="{116-h}" width="3.6" height="{h}" rx="1.2" fill="{T4}" opacity="{1 if tall else .55}"/>')
    y = para(o, 0, 130, "solid = the step's GATE · faded = the pad's release · ticks = track 4's steps", 64, 7.2, INK3)
    return svg(y, o)

# ------------------------------------------------------------------ L10: sections on the bar (two stacked timelines)
def section_timeline():
    cols = {"A": "#e6e1d5", "B": "#a8a49a", "C": "#6e6a62", "D": "#43434a"}
    fg = {"A": "#1a1a1e", "B": "#1a1a1e", "C": "#f2efe8", "D": "#f2efe8"}
    o = []
    y = para(o, 0, 10, "SAVE + key 1–4 while playing: the new section starts on the next bar", 58, 8.4, INK)
    bw = W / 8; y0 = y + 2
    for i, s in enumerate(["A", "A", "A", "B", "B", "B", "B", "C"]):
        o.append(f'<rect x="{i*bw}" y="{y0}" width="{bw-2}" height="24" rx="4" fill="{cols[s]}"/>')
        o.append(T(i * bw + (bw - 2) / 2, y0 + 16, s, 10, 600, fg[s], "middle"))
    px = 2 * bw + bw * .4
    o.append(f'<circle cx="{px:.1f}" cy="{y0+36}" r="3" fill="{LIME}"/><path d="M{px:.1f},{y0+36} L{px:.1f},{y0+26}" stroke="{LIME}" stroke-width="1.4"/>')
    o.append(T(px - 6, y0 + 38, "SAVE + key 2,", 7.4, 400, INK2, "end")); o.append(T(px - 6, y0 + 48, "pressed here", 7.4, 400, INK2, "end"))
    o.append(f'<path d="M{3*bw-1},{y0+24} L{3*bw-1},{y0+54}" stroke="{LIME}" stroke-width="1.4"/>')
    y = para(o, 3 * bw + 4, y0 + 58, "B begins at the next bar line, every track from its first step", 34, 7.4, INK2)
    y = para(o, 0, y + 10, "A quick chain, A B B C, tapped while SAVE stays held:", 58, 8.4, INK)
    y = para(o, 0, y, "each section plays for its own pattern length, round and round", 64, 7.4, INK2)
    y0 = y + 2
    for i, s in enumerate(["A", "B", "B", "C", "A", "B", "B", "C"]):
        o.append(f'<rect x="{i*bw}" y="{y0}" width="{bw-2}" height="24" rx="4" fill="{cols[s]}" opacity="{1 if i<4 else .45}"/>')
        o.append(T(i * bw + (bw - 2) / 2, y0 + 16, s, 10, 600, fg[s], "middle"))
    y = para(o, 0, y0 + 38, "SONG REC (SAVE + key 14) writes down which sections you played, and for how many bars", 64, 7.2, INK3)
    return svg(y, o)

# ------------------------------------------------------------------ L10: what is saved where, stacked
def saved_where():
    o = []
    o.append(f'<rect x="1" y="1" width="{W-2}" height="214" rx="6" fill="none" stroke="{LIME}" stroke-width="1" stroke-dasharray="4 3"/>')
    def box(x, y, w, h, title, lines):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{CARD}" stroke="{INK3}" stroke-width=".7"/>')
        o.append(T(x + w / 2, y + 16, title, 9.4, 600, INK, "middle"))
        yy = y + 28
        for ln in lines: o.append(T(x + w / 2, yy, ln, 7.4, 400, INK2, "middle")); yy += 10
    box(16, 14, 150, 60, "WORKING LOOP", ["what you hear in loop mode", "kept by autosave"])
    cols = ["#e6e1d5", "#a8a49a", "#6e6a62", "#43434a"]; fg = ["#1a1a1e", "#1a1a1e", "#f2efe8", "#f2efe8"]
    for i, (n, c) in enumerate(zip("ABCD", cols)):
        x = 210 + (i % 2) * 60; y = 14 + (i // 2) * 30
        o.append(f'<rect x="{x}" y="{y}" width="54" height="26" rx="4" fill="{c}"/>' + T(x + 27, y + 18, n, 12, 700, fg[i], "middle"))
    o.append(T(267, 86, "four saved sections", 7.4, 400, INK2, "middle"))
    # arrows between loop and sections
    o.append(f'<path d="M170,34 L204,34 M199,30 L205,34 L199,38" fill="none" stroke="{INK3}" stroke-width="1.1"/>')
    o.append(f'<path d="M204,58 L170,58 M175,54 L169,58 L175,62" fill="none" stroke="{INK3}" stroke-width="1.1"/>')
    o.append(T(187, 27, "SAVE + key 5–8", 6.8, 600, INK, "middle")); o.append(T(187, 69, "SAVE + key 1–4", 6.8, 600, INK, "middle"))
    o.append(T(100, 100, "save into a section (up)  ·  load a section (down)", 7.2, 400, INK2))
    # song
    box(16, 118, 320, 56, "SONG", ["sections A–D in order, up to 16 steps", "SONG REC (SAVE + key 14) writes one down as you play"])
    o.append(f'<path d="M267,76 L267,112 M263,107 L267,113 L271,107" fill="none" stroke="{INK3}" stroke-width="1.1"/>')
    y = para(o, 10, 192, "WEB-EDITOR BACKUP: one file holds all of this, plus your user presets, samples, kits and settings (favourites are not included)", 58, 7.4, LIME)
    return svg(220, o)

# ------------------------------------------------------------------ ch14: the editor map and the audio path, stacked for a tall column
def _fm1_block(o, x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#2a2a2f" stroke="#1e1e22" stroke-width="1"/>')
    o.append(f'<rect x="{x+w*.14}" y="{y+h*.12}" width="{w*.24}" height="{h*.42}" rx="3" fill="#050505"/>')
    for i in range(4): o.append(f'<circle cx="{x+w*.52+i*w*.12}" cy="{y+h*.22}" r="{h*.07}" fill="#202023" stroke="#141415"/>')
    for r in range(2):
        for i in range(6): o.append(f'<rect x="{x+w*.46+i*w*.085}" y="{y+h*.38+r*h*.16}" width="{w*.07}" height="{h*.12}" rx="2" fill="#1c1c1e"/>')
    for i in range(16): o.append(f'<rect x="{x+w*.06+i*w*.056}" y="{y+h*.68}" width="{w*.04}" height="{h*.24}" rx="2" fill="#1c1c1e"/>')

def editor_map():
    o = []
    _fm1_block(o, 70, 4, 212, 110)
    o.append(T(176, 128, "FM-1", 10, 600, INK, "middle")); o.append(T(176, 139, "running SLOOP", 7.4, 400, INK2, "middle"))
    # cable down
    o.append(f'<rect x="171" y="146" width="10" height="8" rx="1.5" fill="{INK}"/><path d="M176,154 L176,190" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><rect x="171" y="188" width="10" height="8" rx="1.5" fill="{INK}"/>')
    o.append(T(186, 166, "USB-C", 8, 600, INK)); o.append(T(186, 176, "a data cable, straight in, no hub;", 7.2, 400, INK2)); o.append(T(186, 185, "MIDI runs both ways", 7.2, 400, INK2))
    # browser
    bx, by, bw, bh = 16, 202, 320, 150
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="7" fill="{CARD}" stroke="{INK}" stroke-width="1"/>')
    o.append(f'<path d="M{bx},{by+16} H{bx+bw}" stroke="{INK}" stroke-width=".7"/>')
    for i in range(3): o.append(f'<circle cx="{bx+10+i*8}" cy="{by+8}" r="2.4" fill="{INK3}"/>')
    o.append(T(bx + 40, by + 11, "isod89.github.io/sloop-fm1/webapp/editor", 6.8, 400, INK2))
    items = ["LIVE", "Sound", "Sequencer", "Library", "Song & sections", "Settings"]
    for i, it in enumerate(items):
        yy = by + 32 + i * 18
        if it in ("Sound", "Song & sections"): o.append(f'<rect x="{bx+8}" y="{yy-11}" width="88" height="15" rx="2.5" fill="{WASH}"/>')
        o.append(T(bx + 12, yy, it, 8, 600 if it in ("Sound", "Song & sections") else 400, INK if it in ("Sound", "Song & sections") else INK2))
    o.append(f'<rect x="{bx+112}" y="{by+26}" width="196" height="20" rx="4" fill="{INK}"/>' + T(bx + 210, by + 39.5, "Connect", 8.4, 600, NIGHT, "middle"))
    for i, c in enumerate((T1, "#22995a", "#e0a92a", T4)):
        o.append(f'<rect x="{bx+112+i*48}" y="{by+58}" width="40" height="36" rx="4" fill="{c}" opacity=".85"/>')
        o.append(f'<rect x="{bx+118+i*48}" y="{by+66}" width="28" height="5" rx="2" fill="#0e0e10" opacity=".35"/>')
    o.append(T(bx + 112, by + 108, "every value is a tile you drag", 7.2, 400, INK2)); o.append(T(bx + 112, by + 118, "up or down like a knob", 7.2, 400, INK2))
    o.append(f'<rect x="{bx+112}" y="{by+124}" width="196" height="20" rx="4" fill="{LIME}"/>' + T(bx + 210, by + 137.5, "Save a backup", 8.4, 600, NIGHT, "middle"))
    o.append(T(176, by + bh + 14, "the web editor", 10, 600, INK, "middle"))
    o.append(T(176, by + bh + 25, "drawn, not a screenshot; details simplified", 7.2, 400, INK3, "middle"))
    return svg(by + bh + 32, o)

def audio_path():
    o = []
    o.append(T(0, 10, "hold HOME · AUDIO · USB AUDIO = FULL", 7.8, 600, INK))
    _fm1_block(o, 70, 18, 212, 110)
    o.append(T(176, 142, "FM-1", 10, 600, INK, "middle")); o.append(T(176, 153, "running SLOOP", 7.4, 400, INK2, "middle"))
    o.append(f'<rect x="171" y="160" width="10" height="8" rx="1.5" fill="{INK}"/><path d="M176,168 L176,206" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><rect x="171" y="204" width="10" height="8" rx="1.5" fill="{INK}"/>')
    pts = " ".join(f"{160 + 4*math.sin(y/3.2):.1f},{y}" for y in range(170, 204, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{LIME}" stroke-width="1.4"/>')
    o.append(T(150, 180, "audio, on the same cable", 7.6, 600, LIME, "end"))
    o.append(T(186, 180, "the Mac sees an input", 7.2, 400, INK2)); o.append(T(186, 190, "named Felucca", 7.2, 600, INK))
    gx, gy, gw, gh = 16, 218, 320, 118
    o.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="7" fill="{CARD}" stroke="{INK}" stroke-width="1"/>')
    o.append(f'<path d="M{gx},{gy+16} H{gx+gw}" stroke="{INK}" stroke-width=".7"/>')
    for i in range(3): o.append(f'<circle cx="{gx+10+i*8}" cy="{gy+8}" r="2.4" fill="{INK3}"/>')
    o.append(T(gx + 40, gy + 11, "GarageBand", 8, 600, INK))
    o.append(T(gx + 10, gy + 32, "Settings › Audio/MIDI › Input Device:", 7.6, 400, INK2)); o.append(T(gx + 150, gy + 32, "Felucca", 7.6, 600, INK))
    o.append(f'<rect x="{gx+10}" y="{gy+42}" width="{gw-20}" height="34" rx="4" fill="{WASH}"/>')
    o.append(f'<circle cx="{gx+22}" cy="{gy+59}" r="5" fill="#c0392b"/>')
    o.append(T(gx + 34, gy + 56, "Audio track · input 1 + 2 (stereo) · armed", 7.4, 400, INK2))
    pts = " ".join(f"{x},{gy+67 + 4*math.sin(x/5)*math.sin(x/23):.1f}" for x in range(gx + 34, gx + gw - 16, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{LIME}" stroke-width="1.2"/>')
    y = para(o, gx + 10, gy + 92, "software monitoring off: listen on the FM-1's own output; what you capture is exactly what the headphones hear", 62, 7.2, INK2)
    o.append(T(176, gy + gh + 12, "drawn, not a screenshot; menu names vary by version", 7.2, 400, INK3, "middle"))
    y = para(o, 0, gy + gh + 28, "Arm the track, press GarageBand's record button, then PLAY on the FM-1. Stop both when done.", 64, 7.6, INK)
    return svg(y + 2, o)

# ------------------------------------------------------------------ L8: 64 steps, four pages, as a 2×2 for the tall column
def step_pages():
    o = []
    pw, ph = 168, 44
    for p in range(4):
        x = (p % 2) * (pw + 16); y = 12 + (p // 2) * (ph + 26)
        o.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="5" fill="{CARD if p else WASH}" stroke="{INK if p==0 else INK3}" stroke-width="{1.2 if p==0 else .6}"/>')
        for i in range(16):
            on = p == 0 and i in (0, 2, 4, 6, 8, 10, 11, 12, 14)
            o.append(f'<rect x="{x+6+i*9.9:.1f}" y="{y+8}" width="7.2" height="28" rx="2" fill="{T4 if on else "#2c2c31"}"/>')
        o.append(T(x, y - 3, f"page {p+1}", 8.4, 600, INK))
        o.append(T(x + pw, y - 3, f"steps {p*16+1}–{p*16+16}", 7.6, 400, INK3, "end"))
        o.append(T(x + pw / 2, y + ph + 11, f"bar {p+1}", 7.6, 400, INK2, "middle"))
    y = para(o, 0, 12 + 2 * (ph + 26) + 2, "the screen shows 16 steps at a time; OCT− / OCT+ turn the page, and the keys always edit the page on screen", 62, 7.6, INK2)
    return svg(y, o)

# ------------------------------------------------------------------ ch1: four tracks, one playhead (labels above each lane)
def tracks_loop():
    T1_, T2_, T3_ = "#2f6fde", "#22995a", "#e0a92a"
    lanes = [(T1_, "1", "synth", "pads and atmospheres", [0, 4, 8, 12]),
             (T2_, "2", "synth", "chords and keys", [0, 2, 4, 6, 8, 10, 12, 14]),
             (T3_, "3", "synth", "bass or melody", [0, 6, 8, 14]),
             (T4, "4", "drum machine", "16 sounds, one per white key", [0, 2, 4, 5, 6, 8, 10, 12, 14, 15])]
    o = []; LW = 320; SP = (LW - 26) / 15; y = 6
    for col, n, kind, what, hits in lanes:
        o.append(f'<rect x="0" y="{y}" width="18" height="18" rx="4" fill="{col}"/>' + T(9, y + 13, n, 10, 600, "#fff" if n != "3" else "#1a1a1e", "middle"))
        o.append(T(24, y + 8, kind, 9, 600, INK)); o.append(T(24, y + 18, what, 7.4, 400, INK2))
        y += 24
        o.append(f'<rect x="0" y="{y}" width="{LW}" height="18" rx="9" fill="{col}" opacity=".16"/>')
        for h in hits: o.append(f'<rect x="{8+h*SP:.1f}" y="{y+4}" width="12" height="10" rx="3" fill="{col}"/>')
        y += 30
    px = 8 + 7 * SP + 6
    o.append(f'<line x1="{px:.1f}" y1="26" x2="{px:.1f}" y2="{y-6}" stroke="{INK}" stroke-width="1.4"/><path d="M{px-5:.1f},22 L{px+5:.1f},22 L{px:.1f},28Z" fill="{INK}"/>')
    o.append(f'<path d="M{LW+6},{36} C{LW+26},{36} {LW+26},{y-20} {LW+6},{y-20}" fill="none" stroke="{INK3}" stroke-width=".9" stroke-dasharray="2 2"/>')
    y = para(o, 0, y + 4, "one playhead sweeps all four loops together, round and round", 60, 8, INK2)
    return svg(y, o)

# ------------------------------------------------------------------ L2: the one-knob filter (arc, then annotations, nothing overlapping)
def filter_dial():
    o = []; cx, cy, r = 176, 142, 108
    o.append(f'<defs><linearGradient id="fgi" x1="0" x2="1"><stop offset="0" stop-color="#3a3a42"/><stop offset=".5" stop-color="#8c8880"/><stop offset="1" stop-color="{INK}"/></linearGradient></defs>')
    o.append(f'<path d="M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}" fill="none" stroke="url(#fgi)" stroke-width="16" stroke-linecap="round"/>')
    n = 26
    for i in range(n):
        x = cx - 76 + i * (152 / (n - 1)); h = 8 + 26 * math.sin((i + .5) / n * math.pi)
        o.append(f'<rect x="{x-2.4:.1f}" y="{cy-8-h:.1f}" width="4.8" height="{h:.1f}" rx="1.2" fill="{T1}" opacity="{0.3+0.6*(i/(n-1)):.2f}"/>')
    o.append(T(cx - 76, cy + 4, "lows", 7.4, 600, INK3)); o.append(T(cx + 76, cy + 4, "highs", 7.4, 600, INK3, "end"))
    o.append(f'<circle cx="{cx}" cy="{cy-r}" r="11" fill="{INK}"/><line x1="{cx}" y1="{cy-r-8}" x2="{cx}" y2="{cy-r-2}" stroke="{NIGHT}" stroke-width="2.2" stroke-linecap="round"/>')
    o.append(T(cx, cy - r - 18, "centre: off", 8, 600, INK3, "middle"))
    o.append(T(cx, cy + 4, "FX + KNOB 4", 8, 600, INK, "middle"))
    yb = cy + 26
    o.append(T(0, yb, "low-pass", 13, 600, INK)); o.append(T(0, yb + 12, "turn left: dark, distant", 7.6, 400, INK2))
    o.append(T(W, yb, "high-pass", 13, 600, INK, "end")); o.append(T(W, yb + 12, "turn right: thin, a whisper", 7.6, 400, INK2, "end"))
    return svg(yb + 20, o)

# ------------------------------------------------------------------ L3: overdub passes, labels above each lane
def overdub_stack():
    rows = [("pass 1", "the free take: your chords", [(0, 60), (62, 60), (124, 60), (186, 60)], 1.0),
            ("pass 2", "REC while it plays: more notes on top", [(30, 10), (92, 10), (154, 10), (216, 10), (236, 10)], .75),
            ("pass 3", "and again, whenever you like", [(10, 6), (70, 6), (134, 6), (194, 6)], .5)]
    o = []; y = 4; LW = W; k = LW / 250
    for name, what, notes, op in rows:
        o.append(T(0, y + 9, name, 10, 600, INK)); o.append(T(52, y + 9, what, 7.6, 400, INK2))
        y += 14
        o.append(f'<rect x="0" y="{y}" width="{LW}" height="22" rx="5" fill="{T1}" opacity=".12"/>')
        for s, l in notes: o.append(f'<rect x="{2+s*k:.1f}" y="{y+5}" width="{l*k:.1f}" height="12" rx="3" fill="{T1}" opacity="{op}"/>')
        y += 32
    o.append(f'<line x1="0" y1="18" x2="0" y2="{y-8}" stroke="{INK}" stroke-width=".7"/><line x1="{LW}" y1="18" x2="{LW}" y2="{y-8}" stroke="{INK}" stroke-width=".7"/>')
    y = para(o, 0, y + 4, "one loop, the same length every time; every pass joins what is already there", 62, 7.8, INK2)
    return svg(y, o)

# ------------------------------------------------------------------ L8: two clocks, labels above the rows
def poly_wide():
    o = []; X0 = 0; Wb = W / 12
    for b in range(12): o.append(T(X0 + b * Wb + Wb / 2, 8, str(b + 1), 7, 400, INK3, "middle"))
    for b in range(13): o.append(f'<line x1="{X0+b*Wb:.1f}" y1="11" x2="{X0+b*Wb:.1f}" y2="104" stroke="{INK3}" stroke-width=".45" stroke-dasharray="1.4 1.8"/>')
    o.append(T(0, 22, "Drums", 12, 600, INK)); o.append(T(46, 22, "LENGTH 64 · DIV 1/16 · four bars of sixteen steps", 7.4, 400, INK2))
    for s_ in range(3):
        x = X0 + s_ * 4 * Wb
        o.append(f'<rect x="{x+1}" y="27" width="{4*Wb-2}" height="22" rx="4" fill="{T4}" opacity="{1 if s_%2==0 else .62}"/>')
        o.append(T(x + 6, 41, "4 bars · the beat", 7.6, 600, "#fff"))
    o.append(T(0, 66, "Chords", 12, 600, INK)); o.append(T(50, 66, "LENGTH 3 · DIV 1BAR · three steps of one bar", 7.4, 400, INK2))
    for s_ in range(4):
        x = X0 + s_ * 3 * Wb
        o.append(f'<rect x="{x+1}" y="71" width="{3*Wb-2}" height="22" rx="4" fill="{T1}" opacity="{1 if s_%2==0 else .62}"/>')
        o.append(T(x + 6, 85, "3 chords", 7.6, 600, "#fff"))
    o.append(f'<line x1="{W}" y1="11" x2="{W}" y2="110" stroke="{INK}" stroke-width="1.2"/>')
    o.append(T(0, 106, "bar 1: together", 7.6, 400, INK2)); o.append(T(W - 4, 106, "bar 13: the two land together again", 7.6, 400, INK, "end"))
    return svg(112, o)

# ------------------------------------------------------------------ L10: what is saved where, strictly vertical
def saved_where():
    o = []
    def box(y, h, title, lines, x=36, w=280):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{CARD}" stroke="{INK3}" stroke-width=".7"/>')
        o.append(T(x + w / 2, y + 16, title, 9.6, 600, INK, "middle"))
        yy = y + 28
        for ln in lines: o.append(T(x + w / 2, yy, ln, 7.4, 400, INK2, "middle")); yy += 10
    o.append(f'<rect x="1" y="1" width="{W-2}" height="300" rx="6" fill="none" stroke="{LIME}" stroke-width="1" stroke-dasharray="4 3"/>')
    box(14, 50, "WORKING LOOP", ["what you hear in loop mode", "kept by autosave"])
    # down arrow: save; up arrow: load, each with its own label column
    o.append(f'<path d="M130,66 L130,112 M125,106 L130,113 L135,106" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(124, 86, "SAVE + key 5–8", 7.4, 600, INK, "end")); o.append(T(124, 96, "save into a section", 7, 400, INK2, "end"))
    o.append(f'<path d="M222,112 L222,66 M217,72 L222,65 L227,72" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(228, 86, "SAVE + key 1–4", 7.4, 600, INK)); o.append(T(228, 96, "load a section", 7, 400, INK2))
    cols = ["#e6e1d5", "#a8a49a", "#6e6a62", "#43434a"]; fg = ["#1a1a1e", "#1a1a1e", "#f2efe8", "#f2efe8"]
    for i, (n, c) in enumerate(zip("ABCD", cols)):
        x = 36 + i * 72
        o.append(f'<rect x="{x}" y="116" width="64" height="30" rx="4" fill="{c}"/>' + T(x + 32, 136, n, 13, 700, fg[i], "middle"))
    o.append(T(176, 160, "four saved sections, each a complete snapshot", 7.6, 400, INK2, "middle"))
    o.append(f'<path d="M176,166 L176,194 M171,188 L176,195 L181,188" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(184, 178, "SONG REC (SAVE + key 14) writes down", 7, 400, INK2)); o.append(T(184, 187, "which sections you play, and for how long", 7, 400, INK2))
    box(198, 50, "SONG", ["sections A–D in order, up to 16 steps", "played back with SAVE + key 13"])
    y = para(o, 10, 272, "WEB-EDITOR BACKUP: one file holds all of this, plus your user presets, samples, kits and settings (favourites are not included)", 58, 7.4, LIME)
    return svg(306, o)

# ------------------------------------------------------------------ L1: the sound bank, as a stacked list (the kinds in PRESETS order)
def soundbank_ribbon():
    kinds = [("favourites", 10, LIME), ("bass", 22, INK), ("keys", 12, INK), ("organ", 10, INK), ("pad", 25, T1),
             ("lead", 17, INK), ("pluck & bell", 36, INK), ("stab", 12, INK), ("FX", 15, INK), ("your 32 user presets", 24, INK3)]
    o = []; y = para(o, 0, 10, "PRESETS, turned to the right, walks the 153 sounds by kind", 56, 9, INK)
    total = sum(k[1] for k in kinds); x = 0; y0 = y + 2
    for name, wgt, col in kinds:
        w = W * wgt / total
        o.append(f'<rect x="{x:.1f}" y="{y0}" width="{w-1.5:.1f}" height="16" rx="3" fill="{col}" opacity="{.95 if col in (T1,LIME) else .18 if col==INK else .4}"/>')
        x += w
    o.append(f'<path d="M0,{y0+24} L{W-8},{y0+24} M{W-13},{y0+20} L{W-7},{y0+24} L{W-13},{y0+28}" fill="none" stroke="{INK3}" stroke-width="1"/>')
    yy = y0 + 40
    for name, wgt, col in kinds:
        o.append(f'<rect x="0" y="{yy-9}" width="12" height="12" rx="2.5" fill="{col}" opacity="{.95 if col in (T1,LIME) else .4 if col!=INK3 else .6}"/>')
        o.append(T(18, yy, name, 8.4, 600 if col in (T1, LIME) else 400, INK if col != T1 else "#7fb0ff"))
        yy += 14
    yy = para(o, 0, yy + 4, "your favourites come first, then the factory sounds kind by kind, then your own presets; the kind shows next to the name on screen", 62, 7.6, INK2)
    yy = para(o, 0, yy + 1, "keep going until the pads arrive, and stop on WARM PAD", 62, 7.8, "#7fb0ff")
    return svg(yy, o)

# ------------------------------------------------------------------ L5: CHORD on the white keys, two rows of eight
def chord_keys():
    T2_ = "#22995a"; degrees = ["IV", "V", "VI", "VII", "I", "II", "III", "IV", "V", "VI", "VII", "I", "II", "III", "IV", "V"]
    o = []; y = para(o, 0, 10, "With CHORD on, the white keys walk the scale from key 5 (C4)", 54, 9, INK)
    y = para(o, 0, y, "one finger, one chord: key 5 is the home chord (I); each key up is the next chord along, the keys below carry on downwards.", 64, 7.6, INK2)
    kw = W / 8; blk = (0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14)
    for row in range(2):
        K = y + 4 + row * 84
        for c in range(8):
            i = row * 8 + c; x = c * kw; home = i in (4, 11)
            o.append(f'<rect x="{x:.1f}" y="{K}" width="{kw-3:.1f}" height="62" rx="5" fill="#e6e1d5" stroke="{T2_ if home else "#5a5750"}" stroke-width="{2 if home else .6}"/>')
            o.append(T(x + (kw - 3) / 2, K + 13, str(i + 1), 7.4, 400, "#55524b", "middle"))
            o.append(T(x + (kw - 3) / 2, K + 40, degrees[i], 15, 600, T2_ if home else "#1a1a1e", "middle"))
            o.append(T(x + (kw - 3) / 2, K + 54, "chord", 6.6, 400, "#55524b", "middle"))
            if i in blk and c < 7: o.append(f'<rect x="{x+kw-9:.1f}" y="{K}" width="12" height="30" rx="3" fill="#1c1c1e" opacity=".85"/>')
        if row == 0: o.append(T(4 * kw + (kw - 3) / 2, K + 74, "home", 8, 600, T2_, "middle"))
        else: o.append(T(3 * kw + (kw - 3) / 2, K + 74, "home, an octave up", 8, 600, T2_, "middle"))
    y = y + 4 + 2 * 84 + 2
    y = para(o, 0, y, "Black keys fall silent here; CHORD+ (next page) gives them a new job.", 64, 7.6, INK3)
    y = para(o, 0, y + 1, "The lesson's journey, key 5 › 10 › 8 › 9, is I › VI › IV › V: the four chords under a thousand gentle songs.", 64, 7.6, INK2)
    return svg(y, o)

def chordplus_keys():
    fn = [("F#", "major / minor"), ("G#", "adds the 7th"), ("A#", "sus4"), ("C#", "adds the 9th"), ("D#", "an inversion")]
    o = []; y = para(o, 0, 10, "CHORD+: hold a black key and the chord under your finger changes", 52, 9, INK)
    for k, v in fn:
        o.append(f'<rect x="0" y="{y-9}" width="24" height="13" rx="2.5" fill="#1c1c1e" stroke="#5a5750" stroke-width=".6"/>' + T(12, y + .5, k, 7.6, 600, INK, "middle"))
        o.append(T(32, y, v, 8.4, 400, INK)); y += 17
    y = para(o, 0, y + 2, "both octaves of black keys work, and you can hold several at once", 64, 7.6, INK3)
    return svg(y, o)

# ------------------------------------------------------------------ L7: a step holds four notes (stacked)
def four_note_step():
    T2_ = "#22995a"; EMPTY_ = "#2c2c31"
    cases = [("a TRIAD chord on the step", [T2_, T2_, T2_, None], "three notes used, one spare"),
             ("a melody note on the same step", [T2_, T2_, T2_, "M"], "four notes: the step is full"),
             ("one more note arrives", [T2_, T2_, "M", "M"], "the oldest held note gives way")]
    o = []; y = 4
    for title, slots, note in cases:
        o.append(T(0, y + 9, title, 9, 600, INK))
        for k, c in enumerate(slots):
            x = k * 34
            if c == "M": o.append(f'<rect x="{x}" y="{y+14}" width="30" height="30" rx="5" fill="{T2_}" opacity=".38"/><rect x="{x+.8}" y="{y+14.8}" width="28.4" height="28.4" rx="4.4" fill="none" stroke="{T2_}" stroke-width="1.4"/>')
            else: o.append(f'<rect x="{x}" y="{y+14}" width="30" height="30" rx="5" fill="{c or EMPTY_}" stroke="{INK3 if c is None else "none"}" stroke-width=".8" stroke-dasharray="3 2"/>')
        o.append(T(150, y + 32, note, 8, 400, INK2))
        y += 54
    o.append(f'<rect x="0" y="{y}" width="14" height="10" rx="2.5" fill="{T2_}"/>' + T(20, y + 8, "chord notes (track 2's Rhodes)", 7.8, 400, INK2))
    y += 16
    o.append(f'<rect x="0" y="{y}" width="14" height="10" rx="2.5" fill="{T2_}" opacity=".38"/><rect x="0.6" y="{y+.6}" width="12.8" height="8.8" rx="2" fill="none" stroke="{T2_}" stroke-width="1.1"/>' + T(20, y + 8, "melody notes: the same track, the same Rhodes, an octave up", 7.8, 400, INK2))
    y = para(o, 0, y + 22, "so: place melody notes mostly between the chord hits, where every slot is free", 64, 7.6, INK3)
    return svg(y, o)

# ------------------------------------------------------------------ L9: a punch-in lasts as long as the finger (tall)
def punch_timeline():
    o = []; X0, X1 = 60, W
    for b in range(5):
        x = X0 + b * (X1 - X0) / 4
        o.append(f'<line x1="{x:.1f}" y1="8" x2="{x:.1f}" y2="96" stroke="{INK3}" stroke-width=".5" stroke-dasharray="1.6 1.8"/>')
        if b < 4: o.append(T(x + 3, 7, f"bar {b+1}", 6.8, 400, INK3))
    fx0, fx1 = X0 + 66, X0 + 186
    o.append(T(0, 30, "FX + a key", 9, 600, INK)); o.append(T(0, 74, "the effect", 9, 600, INK))
    o.append(f'<rect x="{fx0}" y="20" width="{fx1-fx0}" height="14" rx="7" fill="{INK}"/>' + T((fx0 + fx1) / 2, 30, "held", 7.4, 600, NIGHT, "middle"))
    o.append(f'<path d="M{X0},84 L{fx0+4},84 L{fx0+10},58 L{fx1-6},58 L{fx1+10},84 L{X1},84" fill="none" stroke="{LIME}" stroke-width="2.2" stroke-linejoin="round"/>')
    o.append(T(fx0 + 10, 52, "starts on the grid", 7, 600, LIME)); o.append(T(fx1 + 14, 76, "lets go cleanly", 7, 600, LIME))
    y = para(o, 0, 112, "exactly as long as your finger; never recorded.", 64, 7.8, INK2)
    y = para(o, 0, y, "The fade setting (FX held, then SELECT) softens the edges: 0 instant, 15 about a third of a second.", 64, 7.6, INK2)
    return svg(y, o)

# ------------------------------------------------------------------ L9: the fill strip, four bars stacked
def fill_strip():
    o = []; bw = W; sw = (bw - 6) / 16; y0 = 6
    for b in range(4):
        y = y0 + b * 38
        o.append(f'<rect x="0" y="{y+10}" width="{bw}" height="24" rx="5" fill="{T4}" opacity="{.9 if b%2==0 else .72}"/>')
        o.append(T(2, y + 7, f"bar {b+1}", 7.6, 600, INK)); o.append(T(bw, y + 7, f"page {b+1}", 7, 400, INK3, "end"))
        for i in range(16):
            sx = 3 + i * sw; last = i == 15
            if b == 0 and last:
                o.append(f'<rect x="{sx+.8:.1f}" y="{y+12}" width="{sw-1.8:.1f}" height="20" rx="2.5" fill="{LIME}"/>' + T(sx + sw / 2, y + 26, "F", 9, 700, NIGHT, "middle"))
            elif last:
                o.append(f'<rect x="{sx+.8:.1f}" y="{y+12}" width="{sw-1.8:.1f}" height="20" rx="2.5" fill="none" stroke="{LIME}" stroke-width="1.2" stroke-dasharray="2.4 1.6"/>')
            else:
                o.append(f'<rect x="{sx+1:.1f}" y="{y+17}" width="{sw-2.2:.1f}" height="10" rx="1.8" fill="{NIGHT}" opacity="{.5 if i%2==0 else .2}"/>')
    y = y0 + 4 * 38 + 2
    o.append(f'<rect x="0" y="{y}" width="{W}" height="16" rx="8" fill="{LIME}"/>' + T(W / 2, y + 11, "GLO + key 9, held through one full round (all four bars)", 7.6, 600, NIGHT, "middle"))
    y = para(o, 0, y + 30, "F = a FILL ONLY step: the crash on step 16 of bar 1 plays only while a fill is on, so it rings once per round, when the playhead crosses it with key 9 held. The condition belongs to the whole step, every sound in it, which is why the crash sits on an empty step.", 64, 7.4, INK2)
    y = para(o, 0, y + 1, "dashed: the last step of pages 2, 3 and 4, where the same mark makes a crash greet every fill bar (GLO + key 10).", 64, 7.4, INK3)
    return svg(y, o)

# ------------------------------------------------------------------ final polish: the saving model, compact (same facts, ~50 units shorter)
def saved_where():
    o = []
    def box(y, h, title, lines, x=36, w=280):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{CARD}" stroke="{INK3}" stroke-width=".7"/>')
        o.append(T(x + w / 2, y + 15, title, 9.6, 600, INK, "middle"))
        yy = y + 27
        for ln in lines: o.append(T(x + w / 2, yy, ln, 8, 400, INK2, "middle")); yy += 10
    box(12, 38, "WORKING LOOP", ["what you hear in loop mode · kept by autosave"])
    o.append(f'<path d="M130,52 L130,88 M125,82 L130,89 L135,82" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(124, 67, "SAVE + key 5–8", 8, 600, INK, "end")); o.append(T(124, 77, "save into a section", 8, 400, INK2, "end"))
    o.append(f'<path d="M222,89 L222,53 M217,59 L222,52 L227,59" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(228, 67, "SAVE + key 1–4", 8, 600, INK)); o.append(T(228, 77, "load a section", 8, 400, INK2))
    cols = ["#e6e1d5", "#a8a49a", "#6e6a62", "#43434a"]; fg = ["#1a1a1e", "#1a1a1e", "#f2efe8", "#f2efe8"]
    for i, (n, c) in enumerate(zip("ABCD", cols)):
        x = 36 + i * 72
        o.append(f'<rect x="{x}" y="92" width="64" height="28" rx="4" fill="{c}"/>' + T(x + 32, 111, n, 13, 700, fg[i], "middle"))
    o.append(T(176, 133, "four saved sections, each a complete snapshot", 8, 400, INK2, "middle"))
    o.append(f'<path d="M176,139 L176,163 M171,157 L176,164 L181,157" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    o.append(T(184, 149, "SONG REC (SAVE + key 14) writes down", 8, 400, INK2)); o.append(T(184, 159, "which sections you play, and for how long", 8, 400, INK2))
    box(167, 48, "SONG", ["sections A–D in order, up to 16 steps", "SAVE + key 13: song mode, where PLAY performs it"])
    y = para(o, 12, 231, "WEB-EDITOR BACKUP: one file holds all of this, plus your user presets, samples, kits and settings (favourites are not included)", 64, 8, LIME)
    H = int(y + 2)
    o.insert(0, f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="6" fill="none" stroke="{LIME}" stroke-width="1" stroke-dasharray="4 3"/>')
    return svg(H, o)

# ------------------------------------------------------------------ final polish: the editor map, compact (labels beside the device instead of under it)
def editor_map():
    o = []
    _fm1_block(o, 80, 4, 160, 80)
    o.append(T(252, 36, "FM-1", 10, 600, INK)); o.append(T(252, 48, "running SLOOP", 8, 400, INK2))
    o.append(f'<rect x="155" y="86" width="10" height="8" rx="1.5" fill="{INK}"/><path d="M160,94 L160,114" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><rect x="155" y="112" width="10" height="8" rx="1.5" fill="{INK}"/>')
    o.append(T(172, 99, "USB-C: a data cable, straight in, no hub;", 8, 600, INK)); o.append(T(172, 110, "MIDI runs both ways", 8, 400, INK2))
    bx, by, bw, bh = 16, 124, 320, 140
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="7" fill="{CARD}" stroke="{INK}" stroke-width="1"/>')
    o.append(f'<path d="M{bx},{by+16} H{bx+bw}" stroke="{INK}" stroke-width=".7"/>')
    for i in range(3): o.append(f'<circle cx="{bx+10+i*8}" cy="{by+8}" r="2.4" fill="{INK3}"/>')
    o.append(T(bx + 40, by + 11, "isod89.github.io/sloop-fm1/webapp/editor", 8, 400, INK2))
    items = ["LIVE", "Sound", "Sequencer", "Library", "Song & sections", "Settings"]
    for i, it in enumerate(items):
        yy = by + 32 + i * 17
        hi = it in ("Sound", "Song & sections")
        if hi: o.append(f'<rect x="{bx+8}" y="{yy-11}" width="90" height="15" rx="2.5" fill="{WASH}"/>')
        o.append(T(bx + 12, yy, it, 8, 600 if hi else 400, INK if hi else INK2))
    o.append(f'<rect x="{bx+112}" y="{by+24}" width="196" height="20" rx="4" fill="{INK}"/>' + T(bx + 210, by + 37.5, "Connect", 8.4, 600, NIGHT, "middle"))
    for i, c in enumerate((T1, "#22995a", "#e0a92a", T4)):
        o.append(f'<rect x="{bx+112+i*49}" y="{by+52}" width="43" height="30" rx="4" fill="{c}" opacity=".85"/>')
        o.append(f'<rect x="{bx+118+i*49}" y="{by+59}" width="30" height="5" rx="2" fill="#0e0e10" opacity=".35"/>')
    o.append(T(bx + 112, by + 96, "every value is a tile you drag", 8, 400, INK2)); o.append(T(bx + 112, by + 106, "up or down like a knob", 8, 400, INK2))
    o.append(f'<rect x="{bx+112}" y="{by+114}" width="196" height="20" rx="4" fill="{LIME}"/>' + T(bx + 210, by + 127.5, "Save a backup", 8.4, 600, NIGHT, "middle"))
    o.append(T(176, by + bh + 14, "the web editor", 10, 600, INK, "middle"))
    o.append(T(176, by + bh + 26, "drawn, not a screenshot; details simplified", 8, 400, INK3, "middle"))
    return svg(by + bh + 31, o)

# ------------------------------------------------------------------ final polish: the recording path, compact (labels beside the device)
def audio_path():
    o = []
    o.append(T(0, 10, "hold HOME · AUDIO · USB AUDIO = FULL", 8, 600, INK))
    _fm1_block(o, 70, 18, 180, 90)
    o.append(T(262, 56, "FM-1", 10, 600, INK)); o.append(T(262, 68, "running SLOOP", 8, 400, INK2))
    o.append(f'<rect x="155" y="110" width="10" height="8" rx="1.5" fill="{INK}"/><path d="M160,118 L160,150" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><rect x="155" y="148" width="10" height="8" rx="1.5" fill="{INK}"/>')
    pts = " ".join(f"{146 + 4*math.sin(y/3.2):.1f},{y}" for y in range(120, 148, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{LIME}" stroke-width="1.4"/>')
    o.append(T(136, 132, "audio, on the same cable", 8, 600, LIME, "end"))
    o.append(T(172, 128, "the Mac sees an input", 8, 400, INK2)); o.append(T(172, 139, "named Felucca", 8, 600, INK))
    gx, gy, gw, gh = 16, 162, 320, 112
    o.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="7" fill="{CARD}" stroke="{INK}" stroke-width="1"/>')
    o.append(f'<path d="M{gx},{gy+16} H{gx+gw}" stroke="{INK}" stroke-width=".7"/>')
    for i in range(3): o.append(f'<circle cx="{gx+10+i*8}" cy="{gy+8}" r="2.4" fill="{INK3}"/>')
    o.append(T(gx + 40, gy + 11, "GarageBand", 8, 600, INK))
    o.append(T(gx + 10, gy + 31, "Settings › Audio/MIDI › Input Device:", 8, 400, INK2)); o.append(T(gx + 160, gy + 31, "Felucca", 8, 600, INK))
    o.append(f'<rect x="{gx+10}" y="{gy+40}" width="{gw-20}" height="32" rx="4" fill="{WASH}"/>')
    o.append(f'<circle cx="{gx+22}" cy="{gy+56}" r="5" fill="#c0392b"/>')
    o.append(T(gx + 34, gy + 53, "Audio track · input 1 + 2 (stereo) · armed", 8, 400, INK2))
    pts = " ".join(f"{x},{gy+64 + 4*math.sin(x/5)*math.sin(x/23):.1f}" for x in range(gx + 34, gx + gw - 16, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{LIME}" stroke-width="1.2"/>')
    para(o, gx + 10, gy + 88, "software monitoring off: listen on the FM-1's own output; what you capture is exactly what the headphones hear", 62, 8, INK2)
    o.append(T(176, gy + gh + 13, "drawn, not a screenshot; menu names vary by version", 8, 400, INK3, "middle"))
    y = para(o, 0, gy + gh + 29, "Arm the track, press GarageBand's record button, then PLAY on the FM-1. Stop both when done.", 64, 8, INK)
    return svg(y + 2, o)
