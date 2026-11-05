"""Interior design language, round 2: the diagram sets the page, the instructions annotate it.
Four pages built from the verified content of pages 14, 18, 23 and 35."""
import math, random
INK, INK2, INK3 = "#1f1e1b", "#4f4b44", "#8a857b"
T1, T2, T3, T4 = "#2f6fde", "#22995a", "#e0a92a", "#e2661d"
SIG = "#6b4dff"
MONO = 'class="mono"'; DISP = 'class="disp"'

# ----------------------------------------------------------------------------- page 14: the envelope
def envelope_big():
    """ATK / DEC / SUS / REL at page scale. The curve is the loudness of one note; the four stages are
    colour fields the reader can point at; the knob positions sit under each stage; the two instructions
    (raise ATK, raise REL) are drawn as 'before → after' ghosts on the same curve."""
    W, H = 352, 172
    x0, x1, x2, x3, x4 = 26, 122, 174, 250, 332     # stage boundaries
    base, top, sus = 112, 24, 50
    o = []
    # stage fields
    tones = ("#dcd7f7", "#e6e2d8", "#f3efe4", "#e6e2d8")      # stage fields: tonal, not track colours
    for (a, b, col, name, word) in ((x0, x1, tones[0], "ATK", "fade in"), (x1, x2, tones[1], "DEC", "settle"),
                                     (x2, x3, tones[2], "SUS", "held level"), (x3, x4, tones[3], "REL", "fade out")):
        o.append(f'<rect x="{a}" y="18" width="{b-a}" height="{base-18}" fill="{col}" opacity=".85"/>')
        o.append(f'<text x="{a+6}" y="{base+16}" {DISP} font-size="15" font-weight="600" fill="{INK}">{name}</text>')
        o.append(f'<text x="{a+6}" y="{base+27}" font-size="7" fill="{INK2}">{word}</text>')
    # the key: pressed from x0, released at x3
    o.append(f'<rect x="{x0}" y="{base+36}" width="{x3-x0}" height="7" rx="3.5" fill="{INK}"/>')
    o.append(f'<text x="{x0}" y="{base+54}" {MONO} font-size="6.4" fill="{INK3}">key down</text>')
    o.append(f'<text x="{x3}" y="{base+54}" {MONO} font-size="6.4" fill="{INK3}" text-anchor="middle">key released</text>')
    o.append(f'<line x1="{x3}" y1="24" x2="{x3}" y2="{base+36}" stroke="{INK}" stroke-width=".6" stroke-dasharray="2 2"/>')
    # ghost: the preset's short envelope (quick attack, short release)
    g = f"M{x0},{base} L{x0+10},{top+6} L{x1-30},{sus} L{x3},{sus} L{x3+16},{base}"
    o.append(f'<path d="{g}" fill="none" stroke="{INK3}" stroke-width="1.2" stroke-dasharray="3 2.4"/>')
    o.append(f'<text x="{x0+22}" y="{top-6}" font-size="6.6" fill="{INK3}">before: the preset as it comes (dashed)</text>')
    # the shaped note (after steps 1 and 2)
    d = f"M{x0},{base} C{x0+40},{base} {x1-30},{top} {x1},{top} L{x2},{sus} L{x3},{sus} C{x3+40},{sus} {x4-20},{base} {x4},{base}"
    o.append(f'<path d="{d} L{x4},{base} L{x0},{base}Z" fill="{INK}" opacity=".06"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<text x="{x4+2}" y="{sus-4}" font-size="6.6" font-weight="600" fill="{INK}" text-anchor="end">after: a pad (solid)</text>')
    # loudness axis
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x4}" y2="{base}" stroke="{INK}" stroke-width=".7"/>')
    o.append(f'<text x="{x0-4}" y="{top+3}" {MONO} font-size="6" fill="{INK3}" text-anchor="end">loud</text>')
    o.append(f'<text x="{x0-4}" y="{base+2}" {MONO} font-size="6" fill="{INK3}" text-anchor="end">silent</text>')
    # the two moves, numbered on the curve
    def num(x, y, n, col):
        o.append(f'<circle cx="{x}" cy="{y}" r="7.5" fill="{col}"/>')
        o.append(f'<text x="{x}" y="{y+3.8}" {DISP} font-size="10" font-weight="600" fill="#fff" text-anchor="middle">{n}</text>')
    num(x0+56, 74, 1, SIG); num(x3+44, 84, 2, INK)
    return f'<svg viewBox="0 0 {W} {H}" width="100%">' + "\n".join(o) + '</svg>'

def filter_dial():
    """the one-knob filter: a wide arc from low-pass (left) through off (centre) to high-pass (right)"""
    W, H = 352, 126
    cx, cy, r = 176, 100, 92
    o = []
    o.append('<defs><linearGradient id="fg" x1="0" x2="1"><stop offset="0" stop-color="#1f1e1b"/><stop offset=".5" stop-color="#bdb6a8"/><stop offset="1" stop-color="#f7f5ef"/></linearGradient></defs>')
    o.append(f'<path d="M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}" fill="none" stroke="url(#fg)" stroke-width="13" stroke-linecap="round"/>')
    # a spectrum under the arc: lows on the left, highs on the right
    n = 26
    for i in range(n):
        x = cx - 70 + i * (140 / (n - 1)); hgt = 6 + 20 * math.sin((i + .5) / n * math.pi)
        o.append(f'<rect x="{x-2:.1f}" y="{cy-4-hgt:.1f}" width="4" height="{hgt:.1f}" rx="1" fill="{T1}" opacity="{0.3+0.6*(i/(n-1)):.2f}"/>')
    o.append(f'<text x="{cx-70}" y="{cy+10}" {MONO} font-size="5.6" fill="{INK3}">lows</text>')
    o.append(f'<text x="{cx+70}" y="{cy+10}" {MONO} font-size="5.6" fill="{INK3}" text-anchor="end">highs</text>')
    # labels at the arc's ends, outside it
    o.append(f'<text x="{cx-r+2}" y="{cy+18}" {DISP} font-size="11" font-weight="600" fill="{INK}" text-anchor="middle">low-pass</text>')
    o.append(f'<text x="{cx-r+2}" y="{cy+26}" font-size="6.2" fill="{INK2}" text-anchor="middle">turn left · dark, distant</text>')
    o.append(f'<text x="{cx+r-2}" y="{cy+18}" {DISP} font-size="11" font-weight="600" fill="{INK}" text-anchor="middle">high-pass</text>')
    o.append(f'<text x="{cx+r-2}" y="{cy+26}" font-size="6.2" fill="{INK2}" text-anchor="middle">turn right · thin, a whisper</text>')
    o.append(f'<text x="{cx}" y="{cy-r-11}" {MONO} font-size="6.6" fill="{INK3}" text-anchor="middle">centre: off</text>')
    # the knob, drawn at centre on the arc
    o.append(f'<circle cx="{cx}" cy="{cy-r}" r="9" fill="{INK}"/><line x1="{cx}" y1="{cy-r-7}" x2="{cx}" y2="{cy-r-2}" stroke="#f2f0ea" stroke-width="1.8" stroke-linecap="round"/>')
    o.append(f'<text x="{cx}" y="{cy+26}" {MONO} font-size="6.2" fill="{INK}" text-anchor="middle">FX + KNOB 4</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible">' + "\n".join(o) + '</svg>'

# ----------------------------------------------------------------------------- page 18: weather
def weather_panel(kind, w=160, h=150, seed=1):
    """abstract portraits of the six TEXTURE sources, each built from the sound's own behaviour"""
    rng = random.Random(seed)
    o = []
    k = w / 160.0   # size factor relative to the design size
    if kind == "RAIN":      # falling streaks, a few droplets landing
        for _ in range(int(260 * k * k) + 40):
            x = rng.random() * w; y = rng.random() * h; L = (4 + rng.random() * 10) * k * 1.6
            o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-0.5*k:.1f}" y2="{y+L:.1f}" stroke="{T1}" stroke-width="{0.5+0.4*k:.2f}" opacity="{0.35+0.55*rng.random():.2f}"/>')
        for _ in range(6):
            x = rng.random() * w; y = h - 3*k - rng.random() * 8*k; r = (3 + rng.random() * 6) * k
            o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r*.35:.1f}" fill="none" stroke="{T1}" stroke-width=".5" opacity=".7"/>')
    elif kind == "VINYL":   # grooves, hiss as dust, three crackles
        R = max(w, h) * 0.78; step = 2.6
        for i in range(int(R / step)):
            r = 3 + i * step
            o.append(f'<circle cx="{w/2}" cy="{h*0.55}" r="{r:.1f}" fill="none" stroke="{INK}" stroke-width=".5" opacity="{0.28 if i%2 else 0.48}"/>')
        for _ in range(120):
            a = rng.random() * math.tau; r = 4 + rng.random() * R
            o.append(f'<circle cx="{w/2+r*math.cos(a):.1f}" cy="{h*0.55+r*math.sin(a):.1f}" r="{0.3+rng.random()*.5:.2f}" fill="{T4}" opacity=".8"/>')
        for a in (0.4, 2.3, 4.9):
            r = R * 0.45 + rng.random() * R * 0.3
            o.append(f'<line x1="{w/2+r*math.cos(a):.1f}" y1="{h*0.55+r*math.sin(a):.1f}" x2="{w/2+(r+3.5)*math.cos(a):.1f}" y2="{h*0.55+(r+3.5)*math.sin(a):.1f}" stroke="{T4}" stroke-width="1.6" stroke-linecap="round"/>')
    elif kind == "TAPE":    # a dark hiss band that drifts
        for j in range(7):
            pts = " ".join(f"{x},{h*0.5 + 0.1*h*math.sin(x/w*math.tau*0.9 + j*0.5) + (j-3)*h*0.07:.1f}" for x in range(0, int(w)+1, 2))
            o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="{(3-abs(j-3)*0.5)*k*1.4:.2f}" opacity="{0.16+0.1*(3-abs(j-3))}"/>')
        for _ in range(220):
            x = rng.random() * w; y = h*0.5 + rng.gauss(0, h*0.17)
            o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width=".8" height=".8" fill="{INK}" opacity=".6"/>')
    elif kind == "WIND":    # resonant gusts: long swept strokes
        for j in range(14):
            y0 = h*0.1 + j * (h*0.8/14); amp = (0.035 + 0.06 * math.sin(j / 14 * math.pi)) * h
            pts = " ".join(f"{x},{y0 + amp*math.sin(x/w*math.tau*1.3 + j*.7):.1f}" for x in range(0, int(w)+1, 2))
            o.append(f'<polyline points="{pts}" fill="none" stroke="{T2}" stroke-width="{(0.5+1.1*math.sin(j/14*math.pi)):.2f}" opacity="{0.4+0.55*math.sin(j/14*math.pi):.2f}" stroke-linecap="round"/>')
    elif kind == "RADIO":   # bursts of static between silences
        x = 0
        while x < w:
            burst = rng.random() < 0.5; L = (3 + rng.random() * 9)
            if burst:
                for _ in range(int(L * 9)):
                    o.append(f'<rect x="{x+rng.random()*L:.1f}" y="{rng.random()*h:.1f}" width=".8" height="{0.8+rng.random()*2.4:.1f}" fill="{T3}" opacity="{0.35+0.6*rng.random():.2f}"/>')
            x += L + 1.5
        o.append(f'<line x1="0" y1="{h/2}" x2="{w}" y2="{h/2}" stroke="{T3}" stroke-width=".5" opacity=".5"/>')
    elif kind == "ROOM":    # room tone: a faint, even field with a soft floor
        for _ in range(700):
            x = rng.random() * w; y = rng.random() * h
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r=".5" fill="{INK}" opacity="{0.12+0.22*rng.random():.2f}"/>')
        o.append(f'<rect x="0" y="{h*0.78}" width="{w}" height="{h*0.22}" fill="{INK}" opacity=".07"/>')
    return "\n".join(o)

def weather_strip():
    """six portraits in a row, each labelled with its SRC name as the FM-1 shows it"""
    names = [("RAIN", "a bed and droplets"), ("VINYL", "hiss, rumble, crackle"), ("TAPE", "dark hiss, drifting"),
             ("WIND", "resonant gusts"), ("RADIO", "bursts of static"), ("ROOM", "room tone")]
    W = 352; pw = 54; gap = (W - 6 * pw) / 5; ph = 44
    o = []
    for i, (nm, desc) in enumerate(names):
        x = i * (pw + gap)
        o.append(f'<clipPath id="wc{i}"><rect x="0" y="0" width="{pw}" height="{ph}" rx="5"/></clipPath>')
        o.append(f'<g transform="translate({x:.1f},0)"><rect x="0" y="0" width="{pw}" height="{ph}" rx="5" fill="#fbfaf7"/>'
                 f'<g clip-path="url(#wc{i})">{weather_panel(nm, pw, ph, seed=i+3)}</g></g>')
        o.append(f'<text x="{x+pw/2:.1f}" y="{ph+10}" {MONO} font-size="6.8" font-weight="600" fill="{INK}" text-anchor="middle">{nm}</text>')
        o.append(f'<text x="{x+pw/2:.1f}" y="{ph+17.5}" font-size="5.4" fill="{INK3}" text-anchor="middle">{desc}</text>')
    return f'<svg viewBox="0 0 {W} {ph+22}" width="100%">' + "\n".join(o) + '</svg>'

def weather_hero():
    """the page's main image: rain, large, with the loop's four tracks sitting inside it as quiet bars"""
    W, H = 352, 70
    rng = random.Random(21)
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="7" fill="#1f1e1b"/>']
    for _ in range(620):
        x = rng.random() * W; y = rng.random() * H; L = 5 + rng.random() * 14
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-1.6:.1f}" y2="{y+L:.1f}" stroke="#9db8ee" stroke-width=".7" opacity="{0.15+0.45*rng.random():.2f}"/>')
    # the loop's four tracks, as four quiet bars under the rain
    for i, col in enumerate((T1, T2, T3, T4)):
        y = 20 + i * 11
        o.append(f'<rect x="40" y="{y}" width="{200 + 40*math.sin(i)}" height="6" rx="3" fill="{col}" opacity=".85"/>')
    o.append(f'<text x="40" y="22" {MONO} font-size="7" fill="#c9c2b4">your loop</text>')
    # the texture breathing: MOVE, as a slow envelope along the bottom
    pts = " ".join(f"{x},{H-10 - 8*(0.5+0.5*math.sin(x/W*math.tau*1.0 - 1.2)):.1f}" for x in range(20, W-20, 4))
    o.append(f'<polyline points="{pts}" fill="none" stroke="#9db8ee" stroke-width="1.4" opacity=".9"/>')
    o.append(f'<text x="{W-22}" y="{H-21}" {MONO} font-size="6.4" fill="#9db8ee" text-anchor="end">MOVE · one breath per RATE</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%">' + "\n".join(o) + '</svg>'

def dust_meter():
    """DUST, 0 to 100: sample rate, bits, and a closing low-pass drawn as what happens to a clean wave"""
    W, H = 352, 60
    o = []
    for i, (amt, label) in enumerate(((0, "clean"), (35, "a little warmth"), (70, "old sampler"), (100, "a worn record"))):
        x0 = 10 + i * 86; w = 70
        steps = 40 - int(amt / 100 * 32)
        pts = []
        for s in range(steps + 1):
            x = x0 + w * s / steps
            y = 26 + 14 * math.sin(s / steps * math.tau * 1.5)
            q = 1 + amt / 100 * 6
            y = round(y / q) * q
            pts.append(f"{x:.1f},{y:.1f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>')
        o.append(f'<text x="{x0}" y="54" {MONO} font-size="6.6" fill="{INK}">DUST {amt}</text>')
        o.append(f'<text x="{x0+w}" y="54" font-size="6.2" fill="{INK3}" text-anchor="end">{label}</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%">' + "\n".join(o) + '</svg>'

# ----------------------------------------------------------------------------- page 23: the pattern
def pattern_hero():
    """the 16-step pattern at page scale: lanes with the FM-1's own key number, beat counts above,
    the count words ('1 e & a') under the steps, hit levels as fill, the kick on the 'and' called out,
    and the three fingers that play it."""
    W, H = 352, 222
    L = 70; cw = 16.8; gw = 6.5                 # left margin, cell width, gap between beats
    xs = [L + (i // 4) * (4 * cw + gw) + (i % 4) * cw for i in range(16)]
    lanes = [("Hat", 5, {1, 3, 5, 7, 9, 11, 13, 15}, {3, 7, 11, 15}, 58),
             ("Snare", 3, {5, 13}, set(), 102),
             ("Kick", 1, {1, 11}, set(), 146)]
    o = []
    # beat numbers, large
    for b in range(4):
        x = xs[b * 4]
        o.append(f'<text x="{x}" y="34" {DISP} font-size="26" font-weight="600" fill="{INK}">{b+1}</text>')
        # the count under each beat: "1 e & a"
    counts = ["", "e", "&", "a"]
    for i, x in enumerate(xs):
        c = str(i // 4 + 1) if i % 4 == 0 else counts[i % 4]
        o.append(f'<text x="{x+cw/2-1:.1f}" y="{lanes[-1][4]+36}" {MONO} font-size="7.4" fill="{INK if i%4==0 else INK3}" text-anchor="middle">{c}</text>')
    o.append(f'<text x="{L}" y="{lanes[-1][4]+50}" font-size="6.8" fill="{INK3}">count aloud: the numbers are the beats, the hats fall on every number and every "&amp;".</text>')
    o.append(f'<text x="{L}" y="{lanes[-1][4]+59}" font-size="6.8" fill="{INK3}">One bar of 16 steps, repeated; Lesson 8 stretches this to LENGTH 64, four bars in a row.</text>')
    # lanes
    for name, key, hits, ghosts, y in lanes:
        o.append(f'<text x="0" y="{y+14}" {DISP} font-size="14" font-weight="600" fill="{INK}">{name}</text>')
        o.append(f'<rect x="0" y="{y+19}" width="26" height="10" rx="2" fill="#fff" stroke="#bdb6a8" stroke-width=".5"/>')
        o.append(f'<text x="13" y="{y+26.4}" {MONO} font-size="6.2" fill="#1a1a1e" text-anchor="middle">key {key}</text>')
        for i, x in enumerate(xs, 1):
            if i in hits and i in ghosts:
                o.append(f'<rect x="{x+1:.1f}" y="{y+1}" width="{cw-4:.1f}" height="30" rx="4" fill="#f8dccb" stroke="{T4}" stroke-width="1.2"/>')
            elif i in hits:
                o.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-2:.1f}" height="32" rx="4.5" fill="{T4}"/>')
            else:
                o.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-2:.1f}" height="32" rx="4.5" fill="#e3dfd4"/>')
    # beat separators
    for b in range(1, 4):
        x = xs[b * 4] - gw / 2 - 1
        o.append(f'<line x1="{x:.1f}" y1="48" x2="{x:.1f}" y2="{lanes[-1][4]+32}" stroke="{INK3}" stroke-width=".5" stroke-dasharray="1.6 2"/>')
    # annotation: the kick on the "and" after 3
    x11 = xs[10] + cw / 2 - 1; yk = lanes[-1][4]
    o.append(f'<path d="M{x11:.1f},{yk-6} C{x11:.1f},{yk-30} {x11+40:.1f},{yk-30} {x11+58:.1f},{yk-40}" fill="none" stroke="{INK}" stroke-width=".8"/>')
    o.append(f'<circle cx="{x11:.1f}" cy="{yk-6}" r="1.6" fill="{INK}"/>')
    o.append(f'<text x="{x11+61:.1f}" y="{yk-42}" font-size="7.4" font-weight="600" fill="{INK}">the one surprise:</text>')
    o.append(f'<text x="{x11+61:.1f}" y="{yk-33}" font-size="7" fill="{INK2}">a kick on the "&amp;" after 3</text>')
    # annotation: ghosts
    xg = xs[2] + cw / 2 - 1; yh = lanes[0][4]
    o.append(f'<path d="M{xg:.1f},{yh-4} C{xg:.1f},{yh-18} {xg+30:.1f},{yh-18} {xg+44:.1f},{yh-16}" fill="none" stroke="{INK}" stroke-width=".8"/>')
    o.append(f'<text x="{xg+47:.1f}" y="{yh-14}" font-size="7" fill="{INK2}">outlined = ghost: hold <tspan font-weight="600" fill="{INK}">OCT−</tspan> as you play it</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible">' + "\n".join(o) + '</svg>'

def four_bars():
    """the counted take: four bars of the same pattern as a filmstrip, with the count-in bar before it"""
    W, H = 352, 58
    o = []
    bw = 62; x = 0
    o.append(f'<rect x="{x}" y="10" width="{bw}" height="26" rx="4" fill="none" stroke="{INK3}" stroke-width=".8" stroke-dasharray="2.4 2"/>')
    o.append(f'<text x="{x+bw/2}" y="26" {DISP} font-size="9" font-weight="600" fill="{INK3}" text-anchor="middle">4 · 3 · 2 · 1</text>')
    o.append(f'<text x="{x+bw/2}" y="47" font-size="6.6" fill="{INK3}" text-anchor="middle">count-in, not recorded</text>')
    for b in range(4):
        x = 76 + b * (bw + 7)
        o.append(f'<rect x="{x}" y="10" width="{bw}" height="26" rx="4" fill="{T4}" opacity="{0.9 if b%2==0 else 0.7}"/>')
        o.append(f'<text x="{x+bw/2}" y="26" {DISP} font-size="9" font-weight="600" fill="#fff" text-anchor="middle">bar {b+1}</text>')
        for i in range(16):
            o.append(f'<rect x="{x+4+i*3.4:.1f}" y="30" width="2.2" height="3" fill="#fff" opacity="{0.9 if i in (0,2,4,6,8,10,12,14) else 0.35}"/>')
    o.append(f'<text x="{76}" y="47" font-size="6.6" fill="{INK2}">REC at the end of the count-in · the same pattern four times · REC again when bar 4 ends</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%">' + "\n".join(o) + '</svg>'

# ----------------------------------------------------------------------------- page 35: the web editor
def signal_map():
    """FM-1 ↔ USB ↔ browser editor, and the audio path into GarageBand, as one map"""
    W, H = 352, 184
    o = []
    # FM-1 (left), simplified from the verified top view
    o.append(f'<rect x="8" y="46" width="112" height="68" rx="7" fill="#3a3a3d" stroke="#1e1e20" stroke-width=".8"/>')
    o.append(f'<rect x="38" y="52" width="26" height="26" rx="3" fill="#0c0c0e"/>')
    for i, c in enumerate((T1, T2, T3, T4)):
        o.append(f'<circle cx="{44+i*6}" cy="73" r="1.8" fill="none" stroke="{c}" stroke-width=".9"/>')
    for i in range(4):
        o.append(f'<circle cx="{76+i*11}" cy="57" r="3" fill="#202023"/>')
    for r in range(2):
        for c in range(6):
            o.append(f'<rect x="{70+c*8.2}" y="{64+r*7}" width="6.6" height="5.4" rx="1" fill="#1c1c1e"/>')
    for i in range(16):
        o.append(f'<rect x="{13+i*6.6}" y="92" width="4.6" height="16" rx="2.3" fill="#1c1c1e"/>')
    for i, present in enumerate((1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0)):
        if present: o.append(f'<rect x="{16+i*6.6}" y="82" width="4.6" height="9" rx="2.3" fill="#1c1c1e"/>')
    o.append(f'<text x="64" y="128" {DISP} font-size="11" font-weight="600" fill="{INK}" text-anchor="middle">FM-1</text>')
    o.append(f'<text x="64" y="137" font-size="6.6" fill="{INK2}" text-anchor="middle">running SLOOP</text>')
    # the one cable
    o.append(f'<path d="M120,80 C150,80 150,80 180,80" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<rect x="118" y="75" width="8" height="10" rx="1.5" fill="{INK}"/><rect x="176" y="75" width="8" height="10" rx="1.5" fill="{INK}"/>')
    o.append(f'<text x="150" y="70" {MONO} font-size="6.4" font-weight="600" fill="{INK}" text-anchor="middle">USB-C</text>')
    o.append(f'<text x="150" y="93" font-size="6" fill="{INK2}" text-anchor="middle">one data cable,</text>')
    o.append(f'<text x="150" y="100" font-size="6" fill="{INK2}" text-anchor="middle">three jobs</text>')
    # the Mac (right): browser editor on top, GarageBand below
    o.append(f'<rect x="184" y="14" width="160" height="92" rx="6" fill="#fbfaf7" stroke="{INK}" stroke-width=".9"/>')
    o.append(f'<rect x="184" y="14" width="160" height="12" rx="6" fill="{INK}"/><rect x="184" y="20" width="160" height="6" fill="{INK}"/>')
    o.append(f'<text x="192" y="22.6" {MONO} font-size="5.6" fill="#f2f0ea">isod89.github.io/sloop-fm1/webapp/editor · Chrome or Edge</text>')
    # sidebar
    for i, (nm, hot) in enumerate((("LIVE", 0), ("Sound", 1), ("Sequencer", 0), ("Library", 0), ("Song &amp; sections", 1), ("Settings", 0))):
        y = 36 + i * 11
        o.append(f'<rect x="190" y="{y-7}" width="46" height="9.5" rx="2" fill="{"#e6e2d8" if hot else "none"}"/>')
        o.append(f'<text x="193" y="{y}" {MONO} font-size="5.6" fill="{INK if hot else INK3}">{nm}</text>')
    # editor body: four coloured parameter cards + a Backup button
    for i, c in enumerate((T1, T2, T3, T4)):
        o.append(f'<rect x="{244+i*23}" y="31" width="20" height="18" rx="2.5" fill="{c}" opacity=".9"/>')
    o.append(f'<text x="244" y="60" font-size="5.8" fill="{INK2}">every knob of the selected track, live</text>')
    o.append(f'<rect x="244" y="68" width="60" height="12" rx="2.5" fill="{SIG}"/><text x="274" y="76.2" {MONO} font-size="5.8" font-weight="600" fill="#fff" text-anchor="middle">Save a backup</text>')
    o.append(f'<text x="308" y="76" font-size="5.4" fill="{INK3}">one file, the whole FM-1</text>')
    o.append(f'<text x="264" y="98" {DISP} font-size="9.5" font-weight="600" fill="{INK}" text-anchor="middle">the web editor</text>')
    # GarageBand
    o.append(f'<rect x="184" y="124" width="160" height="56" rx="6" fill="#fbfaf7" stroke="{INK}" stroke-width=".9"/>')
    o.append(f'<text x="192" y="136" {DISP} font-size="9.5" font-weight="600" fill="{INK}">GarageBand</text>')
    o.append(f'<text x="192" y="146" font-size="6.2" fill="{INK2}">Input Device: <tspan font-weight="600" fill="{INK}">Felucca</tspan> (that is the FM-1)</text>')
    o.append(f'<rect x="192" y="152" width="144" height="18" rx="2.5" fill="#e6e2d8"/>')
    pts = " ".join(f"{x},{161 + 6*math.sin(x/8)*math.sin(x/37):.1f}" for x in range(196, 334, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{T4}" stroke-width="1"/>')
    o.append(f'<circle cx="198" cy="161" r="2.6" fill="#c0392b"/>')
    o.append(f'<text x="196" y="176.5" font-size="5.4" fill="{INK3}">a stereo audio track, armed: what the headphones hear</text>')
    # audio arrow: cable -> GarageBand
    o.append(f'<path d="M164,84 L164,152 L182,152" fill="none" stroke="{T4}" stroke-width="1.6" stroke-dasharray="3 2.4"/>')
    o.append(f'<path d="M178,148.5 L183,152 L178,155.5" fill="none" stroke="{T4}" stroke-width="1.4" stroke-linecap="round"/>')
    o.append(f'<text x="168" y="128" font-size="6" fill="{T4}">audio out</text>')
    # both directions on the editor link
    o.append(f'<path d="M180,40 L136,40 L136,74" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="2.4 2"/>')
    o.append(f'<text x="133" y="36" font-size="6" fill="{INK2}" text-anchor="end">MIDI and the editor, both ways</text>')
    # device-side setting
    o.append(f'<text x="8" y="158" {MONO} font-size="6.2" fill="{INK}">on the FM-1: hold HOME, AUDIO,</text>')
    o.append(f'<text x="8" y="166" {MONO} font-size="6.2" fill="{INK}">USB AUDIO = FULL</text>')
    o.append(f'<text x="8" y="175" font-size="5.8" fill="{INK3}">a fixed, healthy level, whatever MASTER does</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible">' + "\n".join(o) + '</svg>'
