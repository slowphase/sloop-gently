"""Instructional diagrams (data-driven SVG) shared by both editions."""
INK, INK3, PAPER = "#1f1e1b", "#8a857b", "#f2f0ea"
T1, T2, T3, T4 = "#2f6fde", "#22995a", "#e0a92a", "#e2661d"
EMPTY = "#e3dfd4"

# ---------- page 20: 16-step pattern ----------
def cells():
    o = []
    hat = {1, 3, 5, 7, 9, 11, 13, 15}; hat_ghost = {3, 7, 11, 15}
    lanes = [(24, hat, hat_ghost), (48, {5, 13}, set()), (72, {1, 11}, set())]
    xs = [50 + g * 75.5 + j * 17.5 for g in range(4) for j in range(4)]
    for y, hits, ghosts in lanes:
        for i, x in enumerate(xs, 1):
            if i in hits and i in ghosts:
                o.append(f'<rect x="{x+.6:.1f}" y="{y+.6}" width="13.8" height="16.8" rx="3.4" fill="#f8dccb" stroke="{T4}" stroke-width="1.2"/>')
            elif i in hits:
                o.append(f'<rect x="{x:.1f}" y="{y}" width="15" height="18" rx="4" fill="{T4}"/>')
            else:
                o.append(f'<rect x="{x:.1f}" y="{y}" width="15" height="18" rx="4" fill="{EMPTY}"/>')
    for i, x in enumerate(xs, 1):
        o.append(f'<text x="{x+7.5:.1f}" y="101" class="mono" font-size="6.2" fill="{INK3}" text-anchor="middle">{i}</text>')
    # annotate the kick on step 11
    x11 = xs[10] + 7.5
    o.append(f'<path d="M{x11:.1f},106 L{x11:.1f},110" stroke="{INK}" stroke-width=".7"/>')
    o.append(f'<text x="{x11:.1f}" y="118" font-size="7" fill="{INK}" text-anchor="middle">kick on the "and" after 3</text>')
    return "\n      ".join(o)

# ---------- page 20: the armed screen's dials ----------
def dials():
    o = []
    spec = [("KNOB 1", "MODE", "tempo", T1, True), ("KNOB 2", "LENGTH", "4 bars", T2, False),
            ("KNOB 3", "START", "count", T3, False), ("KNOB 4", "QUANT", "on", T4, False)]
    for i, (k, p, v, c, opt) in enumerate(spec):
        cx = 25 + i * 50
        dash = ' stroke-dasharray="3 2.4"' if opt else ""
        o.append(f'<circle cx="{cx}" cy="22" r="14" fill="none" stroke="{c}" stroke-width="3"{dash}/>')
        o.append(f'<circle cx="{cx}" cy="22" r="9.5" fill="{INK if not opt else "#5b5852"}"/>')
        o.append(f'<line x1="{cx}" y1="15" x2="{cx+4}" y2="19" stroke="{PAPER}" stroke-width="1.8" stroke-linecap="round"/>')
        o.append(f'<text x="{cx}" y="49" class="mono" font-size="6.6" fill="{INK3}" text-anchor="middle">{k}</text>')
        o.append(f'<text x="{cx}" y="61" class="disp" font-size="10" font-weight="600" fill="{INK}" text-anchor="middle">{p}</text>')
        w = 7 + len(v) * 5.2
        o.append(f'<rect x="{cx-w/2:.1f}" y="66" width="{w:.1f}" height="11" rx="2" fill="#e6e2d8"/>')
        o.append(f'<text x="{cx}" y="74" class="mono" font-size="7.4" font-weight="500" fill="{INK}" text-anchor="middle">{v}</text>')
    o.append(f'<text x="25" y="89" class="mono" font-size="5.8" fill="{INK3}" text-anchor="middle">empty loop only</text>')
    return "\n          ".join(o)

# ---------- page 25: two timescales ----------
def timescale():
    o = ['<defs><linearGradient id="g-rel2" x1="0" x2="1"><stop offset="0" stop-color="#2f6fde"/>'
         '<stop offset="1" stop-color="#2f6fde" stop-opacity="0"/></linearGradient></defs>']
    X0, BW = 70, 70
    for b in range(4):
        o.append(f'<text x="{X0+b*BW+2}" y="8" class="mono" font-size="6.4" fill="{INK3}">bar {b+1}</text>')
    for b in range(5):
        o.append(f'<line x1="{X0+b*BW}" y1="11" x2="{X0+b*BW}" y2="63" stroke="{INK3}" stroke-width=".5" stroke-dasharray="1.6 1.6"/>')
    # lane labels
    o.append(f'<rect x="0" y="15" width="13" height="11" rx="2" fill="{T1}"/><text x="6.5" y="23" class="mono" font-size="7" font-weight="600" fill="#fff" text-anchor="middle">1</text>')
    o.append(f'<text x="17" y="21" class="mono" font-size="6.2" fill="{INK}">DIV 1BAR</text><text x="17" y="30" class="mono" font-size="6.2" fill="{INK}">LENGTH 4</text>')
    o.append(f'<rect x="0" y="47" width="13" height="11" rx="2" fill="{T4}"/><text x="6.5" y="55" class="mono" font-size="7" font-weight="600" fill="#fff" text-anchor="middle">4</text>')
    o.append(f'<text x="17" y="55" class="mono" font-size="6.2" fill="{INK}">DIV 1/16</text>')
    for i, key in enumerate((5, 10, 8, 9)):
        x = X0 + i * BW + 2
        o.append(f'<rect x="{x}" y="14" width="50" height="21" rx="3.5" fill="{T1}"/>')
        o.append(f'<rect x="{x+48}" y="14" width="17" height="21" fill="url(#g-rel2)"/>')
        o.append(f'<text x="{x+5}" y="23" class="mono" font-size="7" font-weight="600" fill="#fff">step {i+1}</text>')
        o.append(f'<text x="{x+5}" y="31.5" font-size="6.4" fill="#dfe8fa">chord of key {key}</text>')
    for k in range(64):
        x = X0 + k * BW / 16 + 1
        tall = k % 4 == 0
        h = 13 if tall else 8
        o.append(f'<rect x="{x:.2f}" y="{60-h}" width="2.2" height="{h}" rx="1" fill="{T4}" opacity="{1 if tall else .55}"/>')
    o.append(f'<text x="{X0}" y="68.5" class="mono" font-size="5.6" fill="{INK3}">solid = the step\'s GATE · fade = the pad\'s release · ticks = track 4\'s steps</text>')
    return "\n      ".join(o)

# ---------- page 25: polymeter 3 against 4 ----------
def poly():
    o = []
    X0, W = 26, 14
    o.append(f'<text x="0" y="17" class="mono" font-size="6.4" fill="{INK}">drums</text>')
    o.append(f'<text x="0" y="35" class="mono" font-size="6.4" fill="{INK}">chords</text>')
    for s in range(3):
        o.append(f'<rect x="{X0+s*4*W+.6}" y="10" width="{4*W-1.2}" height="10" rx="2.5" fill="{T4}" opacity="{1 if s%2==0 else .55}"/>')
        o.append(f'<text x="{X0+s*4*W+4}" y="17.4" class="mono" font-size="5.8" fill="#fff">4 bars</text>')
    for s in range(4):
        o.append(f'<rect x="{X0+s*3*W+.6}" y="28" width="{3*W-1.2}" height="10" rx="2.5" fill="{T1}" opacity="{1 if s%2==0 else .55}"/>')
        o.append(f'<text x="{X0+s*3*W+4}" y="35.4" class="mono" font-size="5.8" fill="#fff">3 bars</text>')
    xe = X0 + 12 * W
    o.append(f'<line x1="{xe}" y1="5" x2="{xe}" y2="43" stroke="{INK}" stroke-width="1" stroke-dasharray="2 1.6"/>')
    o.append(f'<text x="{xe}" y="53" font-size="6.8" fill="{INK}" text-anchor="end">bar 13: together again</text>')
    o.append(f'<text x="{X0}" y="53" class="mono" font-size="5.8" fill="{INK3}">bar 1</text>')
    return "\n      ".join(o)



def poly_wide():
    """three-bar chord bed against four-bar drums, realigning at bar 13 (352 x 90)"""
    o = []
    X0, W = 44, 24.5          # 12 bars across 294 units
    o.append(f'<text x="0" y="24" class="disp" font-size="10" font-weight="600" fill="{INK}">Drums</text>')
    o.append(f'<text x="0" y="33" class="mono" font-size="6.2" fill="{INK3}">LENGTH 64</text>')
    o.append(f'<text x="0" y="40" class="mono" font-size="6.2" fill="{INK3}">DIV 1/16</text>')
    o.append(f'<text x="0" y="58" class="disp" font-size="10" font-weight="600" fill="{INK}">Chords</text>')
    o.append(f'<text x="0" y="67" class="mono" font-size="6.2" fill="{INK3}">LENGTH 3</text>')
    o.append(f'<text x="0" y="74" class="mono" font-size="6.2" fill="{INK3}">DIV 1BAR</text>')
    for b in range(13):
        x = X0 + b * W
        o.append(f'<line x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="74" stroke="{INK3}" stroke-width=".45" stroke-dasharray="1.4 1.8"/>')
    for b in range(12):
        o.append(f'<text x="{X0 + b*W + W/2:.1f}" y="7" class="mono" font-size="6" fill="{INK3}" text-anchor="middle">{b+1}</text>')
    for s in range(3):
        x = X0 + s * 4 * W
        o.append(f'<rect x="{x+1}" y="15" width="{4*W-2}" height="20" rx="4" fill="{T4}" opacity="{1 if s%2==0 else .62}"/>')
        o.append(f'<text x="{x+6}" y="28" class="mono" font-size="7" font-weight="600" fill="#fff">4 bars · the beat</text>')
    for s in range(4):
        x = X0 + s * 3 * W
        o.append(f'<rect x="{x+1}" y="48" width="{3*W-2}" height="20" rx="4" fill="{T1}" opacity="{1 if s%2==0 else .62}"/>')
        o.append(f'<text x="{x+6}" y="61" class="mono" font-size="7" font-weight="600" fill="#fff">3 chords</text>')
    xe = X0 + 12 * W
    o.append(f'<line x1="{xe}" y1="6" x2="{xe}" y2="80" stroke="{INK}" stroke-width="1.1"/>')
    o.append(f'<text x="{xe-3}" y="86" font-size="7.2" fill="{INK}" text-anchor="end">bar 13: the two land together again</text>')
    o.append(f'<text x="{X0}" y="86" font-size="7.2" fill="{INK3}">bar 1: together</text>')
    return "\n      ".join(o)


def drum_keys_tall():
    """the 16 drum sounds in four rows of four (for the narrow iPad page). Same data as the A4 strip."""
    names = ["KICK","KICK 2","SNARE","CLAP","HAT","OPEN HAT","PEDAL","RIM","SNARE 2","LOW TOM","HI TOM","CRASH","RIDE","SHAKER","CONGA","COWBELL"]
    o = []
    for i, nm in enumerate(names):
        r, c = divmod(i, 4)
        x = c * 44 + 1; y = r * 13 + 1
        lean = (i + 1) in (1, 5)
        fill = T4 if lean else "#f8dccb"
        o.append(f'<rect x="{x}" y="{y}" width="42" height="11" rx="2" fill="{fill}" stroke="{T4}" stroke-width=".5"/>')
        o.append(f'<text x="{x+21}" y="{y+7.6}" class="mono" font-size="4.6" font-weight="600" fill="{"#fff" if lean else "#6b4423"}" text-anchor="middle">{i+1} {nm}</text>')
    return "\n      ".join(o)
