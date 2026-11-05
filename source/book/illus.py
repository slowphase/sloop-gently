"""Explanatory diagrams for the illustrated edition. Every drawing restates a verified sentence of the book.
S = label scale (1.0 for A4, larger for the iPad edition). Track colours appear only where they mean a track."""
import math
INK, INK2, INK3 = "#1f1e1b", "#4f4b44", "#8a857b"
T1, T2, T3, T4 = "#2f6fde", "#22995a", "#e0a92a", "#e2661d"
SIG = "#6b4dff"; WASH = "#e6e2d8"; CARD = "#fbfaf7"; EMPTY = "#e3dfd4"
MONO = 'class="mono"'; DISP = 'class="disp"'

def svg(w, h, body, extra=""):
    return f'<svg viewBox="0 0 {w} {h}" width="100%" {extra}>' + "\n".join(body) + "</svg>"

def wrap(text, maxchars):
    """greedy word wrap by character budget (labels are short; Inter ~0.5em/char, Plex Mono ~0.6em/char)"""
    words = text.split(); lines = []; cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxchars:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def pill(o, x, y, text, fill=INK, fg="#f2f0ea", S=1.0, w=None):
    fsz = 6.2 * S; w = w or (len(text) * fsz * 0.62 + 6 * S)
    o.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{9.5*S:.1f}" rx="{2.2*S}" fill="{fill}"/>')
    o.append(f'<text x="{x+w/2:.1f}" y="{y+6.8*S:.1f}" {MONO} font-size="{fsz:.1f}" font-weight="600" fill="{fg}" text-anchor="middle">{text}</text>')
    return w

# ------------------------------------------------------------------ ch1: four tracks, one playhead
def tracks_loop(S=1.0):
    W, H = 352, 118
    o = []
    lanes = [(T1, "1", "synth", "pads and atmospheres", [0, 4, 8, 12]),
             (T2, "2", "synth", "chords and keys", [0, 2, 4, 6, 8, 10, 12, 14]),
             (T3, "3", "synth", "bass or melody", [0, 6, 8, 14]),
             (T4, "4", "drum machine", "16 sounds, one per white key", [0, 2, 4, 5, 6, 8, 10, 12, 14, 15])]
    X0 = 100 if S <= 1.05 else 128
    LW = 322 - X0; SP = (LW - 21) / 15
    for i, (col, n, kind, what, hits) in enumerate(lanes):
        y = 14 + i * 24
        o.append(f'<rect x="{X0}" y="{y}" width="{LW}" height="16" rx="8" fill="{col}" opacity=".16"/>')
        for h in hits:
            o.append(f'<rect x="{X0+6+h*SP:.1f}" y="{y+4}" width="9" height="8" rx="3" fill="{col}"/>')
        o.append(f'<rect x="0" y="{y+1}" width="14" height="14" rx="3" fill="{col}"/>')
        o.append(f'<text x="7" y="{y+11}" {MONO} font-size="{7.5*S:.1f}" font-weight="600" fill="{"#fff" if i!=2 else INK}" text-anchor="middle">{n}</text>')
        o.append(f'<text x="19" y="{y+8}" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}">{kind}</text>')
        o.append(f'<text x="19" y="{y+15.5}" font-size="{5.6*S:.1f}" fill="{INK3}">{what}</text>')
    # the one playhead
    px = X0 + 6 + 7 * SP
    o.append(f'<line x1="{px:.1f}" y1="8" x2="{px:.1f}" y2="108" stroke="{INK}" stroke-width="1.2"/>')
    o.append(f'<path d="M{px-4:.1f},4 L{px+4:.1f},4 L{px:.1f},9Z" fill="{INK}"/>')
    o.append(f'<text x="{px+5:.1f}" y="114" font-size="{5.8*S:.1f}" fill="{INK2}">one playhead sweeps all four loops together</text>')
    # the loop arrow
    o.append(f'<path d="M{X0+LW+6},22 C{X0+LW+22},22 {X0+LW+22},94 {X0+LW+6},94" fill="none" stroke="{INK3}" stroke-width=".8" stroke-dasharray="2 2"/>')
    o.append(f'<text x="{X0+LW+26}" y="60" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="middle" transform="rotate(90 {X0+LW+26} 60)">round and round</text>')
    return svg(W, H, o)

# ------------------------------------------------------------------ ch2: install flow
def install_flow(S=1.0):
    steps = [("Chrome or Edge", "the installer page", CARD), ("a data cable", "straight in, no hub", CARD),
             ("INSTALL", "allow MIDI access", INK), ("wait for Done", "cable untouched", CARD), ("SLOOP logo", "the FM-1 restarts", CARD)]
    W = 352; o = []
    if S <= 1.1:
        bw = 66; gap = (W - 5 * bw) / 4; y0 = 18; bh = 40
        for i, (a_, b_, fill) in enumerate(steps):
            x = i * (bw + gap)
            o.append(f'<rect x="{x:.1f}" y="{y0}" width="{bw}" height="{bh}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="{0 if fill==INK else .7}"/>')
            fg = "#f2f0ea" if fill == INK else INK
            o.append(f'<text x="{x+bw/2:.1f}" y="{y0+18}" {DISP} font-size="{7.2*S:.1f}" font-weight="600" fill="{fg}" text-anchor="middle">{a_}</text>')
            o.append(f'<text x="{x+bw/2:.1f}" y="{y0+29}" font-size="{5.8*S:.1f}" fill="{"#c9c2b4" if fill==INK else INK2}" text-anchor="middle">{b_}</text>')
            o.append(f'<text x="{x+6:.1f}" y="12" {MONO} font-size="{6*S:.1f}" fill="{INK3}">{i+1}</text>')
            if i < 4:
                o.append(f'<path d="M{x+bw+3:.1f},38 L{x+bw+gap-3:.1f},38" stroke="{INK3}" stroke-width=".9"/><path d="M{x+bw+gap-6:.1f},35 L{x+bw+gap-3:.1f},38 L{x+bw+gap-6:.1f},41" fill="none" stroke="{INK3}" stroke-width=".9"/>')
        o.append(f'<text x="0" y="78" font-size="{6*S:.1f}" fill="{INK2}">The one rule: never unplug or switch off while an install is running.</text>')
        o.append(f'<text x="0" y="87" font-size="{6*S:.1f}" fill="{INK3}">Interrupted anyway? The FM-1 waits in update mode; press INSTALL again.</text>')
        return svg(W, 92, o)
    # stacked, for the narrow page: one row per step
    rh = 30; y = 4
    for i, (a_, b_, fill) in enumerate(steps):
        o.append(f'<rect x="22" y="{y}" width="{W-22}" height="{rh-5}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="{0 if fill==INK else .7}"/>')
        fg = "#f2f0ea" if fill == INK else INK
        o.append(f'<text x="0" y="{y+17}" {MONO} font-size="{9*S:.1f}" font-weight="600" fill="{INK3}">{i+1}</text>')
        o.append(f'<text x="32" y="{y+16}" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{fg}">{a_}</text>')
        o.append(f'<text x="{W-8}" y="{y+16}" font-size="{6.4*S:.1f}" fill="{"#c9c2b4" if fill==INK else INK2}" text-anchor="end">{b_}</text>')
        y += rh
    y += 6
    for ln in wrap("The one rule: never unplug or switch off while an install is running.", int(100/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    for ln in wrap("Interrupted anyway? The FM-1 waits in update mode; press INSTALL again.", int(100/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK3}">{ln}</text>'); y += 7.6 * S
    return svg(W, int(y), o)

# ------------------------------------------------------------------ ch2: recovery map
def recovery_flow(S=1.0):
    W = 352
    o = []
    rows = [("SLOOP will not start", "hold OCT− alone while switching on", "SLOOP USB RESCUE", "install again from the browser"),
            ("An install stopped half-way", "nothing to press on the device", "the FM-1 waits in update mode", "press INSTALL again"),
            ("A button or knob does the wrong thing", "hold OCT− + OCT+ while switching on", "HARDWARE CALIBRATION", "press each control as the screen asks"),
            ("Going back to the official firmware", "save a backup first", "M-UPGRADE + the official V16 file", "not found? the Clipper installer's return option")]
    xs = [18, 130, 242]; cw = 104
    for k, kind in enumerate(("what you do", "what the screen says", "then")):
        o.append(f'<text x="{xs[k]}" y="7" {MONO} font-size="{5.2*S:.1f}" fill="{INK3}">{kind}</text>')
    y = 12; lh = 6.4 * S
    for i, (sym, act, state, then) in enumerate(rows):
        o.append(f'<circle cx="7" cy="{y+8}" r="6" fill="{INK}"/><text x="7" y="{y+11}" {DISP} font-size="{7.5*S:.1f}" font-weight="700" fill="#fff" text-anchor="middle">!</text>')
        o.append(f'<text x="18" y="{y+11}" {DISP} font-size="{8.4*S:.1f}" font-weight="600" fill="{INK}">{sym}</text>')
        cells = [(wrap(act, int(32/S)), False), (wrap(state, int(27/S)), True), (wrap(then, int(32/S)), False)]
        nl = max(len(c[0]) for c in cells)
        ch = nl * lh + 4
        for k, (lines, see) in enumerate(cells):
            x = xs[k]
            o.append(f'<rect x="{x}" y="{y+15}" width="{cw}" height="{ch:.1f}" rx="2.5" fill="{INK if see else WASH}"/>')
            for j, ln in enumerate(lines):
                o.append(f'<text x="{x+4}" y="{y+15+4.5+lh*(j+1)-1.2:.1f}" {MONO if see else ""} font-size="{5.6*S:.1f}" font-weight="{600 if see else 400}" fill="{"#f2f0ea" if see else INK}">{ln}</text>')
            if k < 2:
                o.append(f'<path d="M{x+cw+1},{y+15+ch/2:.1f} L{x+cw+5},{y+15+ch/2:.1f}" stroke="{INK3}" stroke-width=".8"/>')
        y += 15 + ch + 5
    return svg(W, int(y - 2), o)

# ------------------------------------------------------------------ ch3: tap / hold, keys → tiles
def tiles_map(S=1.0):
    if S > 1.1: return tiles_map_stacked(S)
    W, H = 352, 126
    o = []
    # the 16 white keys
    kx = 0; kw = 10.4
    for i in range(16):
        x = kx + i * kw
        glow = i in (0, 4, 8, 12)
        o.append(f'<rect x="{x:.1f}" y="60" width="{kw-1.4:.1f}" height="44" rx="3.5" fill="{"#f7f5ef" if glow else "#fff"}" stroke="{"#8a857b" if glow else "#bdb6a8"}" stroke-width="{1.1 if glow else .5}"/>')
        o.append(f'<text x="{x+(kw-1.4)/2:.1f}" y="98" {MONO} font-size="{6*S:.1f}" fill="{INK}" text-anchor="middle">{i+1}</text>')
    o.append(f'<text x="0" y="43" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">hold a layer button,</text>')
    o.append(f'<text x="0" y="54" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">and the 16 white keys…</text>')
    for j, ln in enumerate(wrap("keys 1, 5, 9 and 13 glow dimly: the first key of each row of tiles, landmarks for your fingers", int(56/S))):
        o.append(f'<text x="0" y="{112+j*7*S:.1f}" font-size="{5.8*S:.1f}" fill="{INK3}">{ln}</text>')
    # arrow
    o.append(f'<path d="M172,82 L196,82" stroke="{INK}" stroke-width="1"/><path d="M192,78 L197,82 L192,86" fill="none" stroke="{INK}" stroke-width="1"/>')
    # the screen with 4x4 tiles
    sx, sy = 206, 24
    o.append(f'<rect x="{sx}" y="{sy}" width="146" height="94" rx="6" fill="#0c0c0e"/>')
    o.append(f'<text x="{sx+6}" y="{sy+10}" {MONO} font-size="{5.6*S:.1f}" fill="#9a958c">the screen: the keys as tiles</text>')
    tw = 32; th = 14
    for r in range(4):
        for c in range(4):
            n = r * 4 + c + 1
            x = sx + 8 + c * (tw + 3); y = sy + 16 + r * (th + 3)
            o.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="2.5" fill="{"#2a2a2e" if c else "#3a3a40"}"/>')
            o.append(f'<text x="{x+4}" y="{y+11}" {MONO} font-size="{6*S:.1f}" fill="{"#e9e4d8" if c==0 else "#9a958c"}">{n}</text>')
    o.append(f'<text x="{sx+6}" y="{sy+90}" {MONO} font-size="{5.2*S:.1f}" fill="#9a958c">rows: keys 1-4 · 5-8 · 9-12 · 13-16</text>')
    return svg(W, H, o)

def tiles_map_stacked(S=1.3):
    """iPad: keys above, screen below"""
    W = 352; o = []
    o.append(f'<text x="0" y="12" {DISP} font-size="{9*S:.1f}" font-weight="600" fill="{INK}">hold a layer button, and the 16 white keys…</text>')
    kw = 21.5
    for i in range(16):
        x = i * kw; glow = i in (0, 4, 8, 12)
        o.append(f'<rect x="{x:.1f}" y="22" width="{kw-2.4:.1f}" height="56" rx="4" fill="{"#f7f5ef" if glow else "#fff"}" stroke="{"#8a857b" if glow else "#bdb6a8"}" stroke-width="{1.2 if glow else .5}"/>')
        o.append(f'<text x="{x+(kw-2.4)/2:.1f}" y="70" {MONO} font-size="{7*S:.1f}" fill="{INK}" text-anchor="middle">{i+1}</text>')
    y = 92
    for ln in wrap("keys 1, 5, 9 and 13 glow dimly: the first key of each row of tiles, landmarks for your fingers", int(78/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.4*S:.1f}" fill="{INK3}">{ln}</text>'); y += 8 * S
    # arrow down
    o.append(f'<path d="M176,{y+2:.1f} L176,{y+16:.1f}" stroke="{INK}" stroke-width="1.2"/><path d="M171,{y+11:.1f} L176,{y+17:.1f} L181,{y+11:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    sy = y + 24; sw = 352; th = 24; tw = (sw - 16 - 9) / 4
    o.append(f'<rect x="0" y="{sy:.1f}" width="{sw}" height="{16 + 4*(th+3) + 22:.1f}" rx="7" fill="#0c0c0e"/>')
    o.append(f'<text x="8" y="{sy+12:.1f}" {MONO} font-size="{6.4*S:.1f}" fill="#9a958c">the screen: the keys as tiles</text>')
    for r in range(4):
        for c in range(4):
            n = r * 4 + c + 1; x = 8 + c * (tw + 3); yy = sy + 18 + r * (th + 3)
            o.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{tw:.1f}" height="{th}" rx="3" fill="{"#2a2a2e" if c else "#3a3a40"}"/>')
            o.append(f'<text x="{x+6:.1f}" y="{yy+16:.1f}" {MONO} font-size="{7.5*S:.1f}" fill="{"#e9e4d8" if c==0 else "#9a958c"}">{n}</text>')
    o.append(f'<text x="8" y="{sy + 18 + 4*(th+3) + 10:.1f}" {MONO} font-size="{6*S:.1f}" fill="#9a958c">rows: keys 1-4 · 5-8 · 9-12 · 13-16</text>')
    return svg(W, int(sy + 16 + 4*(th+3) + 26), o)

# ------------------------------------------------------------------ L1: the sound bank, by kind
def soundbank_ribbon(S=1.0):
    W = 352
    kinds = [("favourites", 10, SIG), ("bass", 22, INK), ("keys", 12, INK), ("organ", 10, INK), ("pad", 25, T1),
             ("lead", 17, INK), ("pluck & bell", 36, INK), ("stab", 12, INK), ("FX", 15, INK), ("your 32 user presets", 24, INK3)]
    total = sum(k[1] for k in kinds)
    o = []; x = 0
    hdr = wrap("PRESETS, turned to the right, walks the 153 sounds by kind", int(66/S))
    for j, ln in enumerate(hdr):
        o.append(f'<text x="0" y="{8 + j*9.5*S:.1f}" {DISP} font-size="{8*S:.1f}" font-weight="600" fill="{INK}">{ln}</text>')
    Y0, RH = (15 if S <= 1.1 else 8 + len(hdr) * 9.5 * S + 12), 22
    for i, (name, wgt, col) in enumerate(kinds):
        w = W * wgt / total
        o.append(f'<rect x="{x:.1f}" y="{Y0}" width="{w-1.2:.1f}" height="{RH}" rx="3" fill="{col}" opacity="{.95 if col in (T1,SIG) else .14 if col==INK else .35}"/>')
        need = len(name) * 5.6 * S * 0.62 + 4
        if need <= w:
            fg = "#fff" if col in (T1, SIG) else INK
            o.append(f'<text x="{x+w/2:.1f}" y="{Y0+14}" {MONO} font-size="{5.6*S:.1f}" font-weight="600" fill="{fg}" text-anchor="middle">{name}</text>')
        else:
            anchor = "start" if i == 0 else "end" if i == len(kinds) - 1 else "middle"
            tx = x + 1 if i == 0 else x + w - 2 if i == len(kinds) - 1 else x + w / 2
            up = (S > 1.1) and (i % 2 == 1)
            if up:
                o.append(f'<line x1="{x+w/2-0.6:.1f}" y1="{Y0}" x2="{x+w/2-0.6:.1f}" y2="{Y0-3}" stroke="{col}" stroke-width=".8"/>')
                o.append(f'<text x="{tx:.1f}" y="{Y0-5}" {MONO} font-size="{5.6*S:.1f}" font-weight="600" fill="{col if col!=INK3 else INK2}" text-anchor="{anchor}">{name}</text>')
            else:
                o.append(f'<line x1="{x+w/2-0.6:.1f}" y1="{Y0+RH}" x2="{x+w/2-0.6:.1f}" y2="{Y0+RH+4}" stroke="{col}" stroke-width=".8"/>')
                o.append(f'<text x="{tx:.1f}" y="{Y0+RH+10}" {MONO} font-size="{5.6*S:.1f}" font-weight="600" fill="{col if col!=INK3 else INK2}" text-anchor="{anchor}">{name}</text>')
        x += w
    ya = Y0 + RH + 15
    o.append(f'<path d="M0,{ya} L{W-6},{ya}" stroke="{INK3}" stroke-width=".8"/><path d="M{W-10},{ya-4} L{W-5},{ya} L{W-10},{ya+4}" fill="none" stroke="{INK3}" stroke-width=".8"/>')
    y = ya + 11
    for ln in wrap("your favourites come first, then the factory sounds kind by kind, then your own presets; the kind shows next to the name on screen", int(118/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{5.8*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.4 * S
    o.append(f'<text x="0" y="{y:.1f}" font-size="{5.8*S:.1f}" fill="{T1}">keep going until the pads arrive, and stop on WARM PAD</text>')
    return svg(W, int(y + 3), o)

# ------------------------------------------------------------------ L2: the LFO over four bars
def lfo_bars(S=1.0):
    W, H = 352, 112
    o = []
    X0, X1, base = 40, 340, 62
    for b in range(5):
        x = X0 + b * (X1 - X0) / 4
        o.append(f'<line x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="90" stroke="{INK3}" stroke-width=".5" stroke-dasharray="1.6 1.8"/>')
        if b < 4: o.append(f'<text x="{x+3:.1f}" y="{11 if S <= 1.1 else 97}" {MONO} font-size="{5.6*S:.1f}" fill="{INK3}">bar {b+1}</text>')
    o.append(f'<line x1="{X0}" y1="{base}" x2="{X1}" y2="{base}" stroke="{INK}" stroke-width=".7"/>')
    o.append(f'<text x="{X0-3}" y="{base+2}" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="end">where the</text>')
    o.append(f'<text x="{X0-3}" y="{base+9}" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="end">knob sits</text>')
    o.append(f'<text x="{X0-3}" y="22" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="end">brighter</text>')
    o.append(f'<text x="{X0-3}" y="88" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="end">darker</text>')
    # sine with FADE: amplitude ramps up over the first bar
    pts = []
    for i in range(0, 301):
        u = i / 300; x = X0 + u * (X1 - X0)
        fade = min(1, u * 4)                 # FADE: eases in over about a bar
        y = base - 34 * fade * math.sin(u * math.tau)     # SYNC 4BAR: one cycle per four bars
        pts.append(f"{x:.1f},{y:.1f}")
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    if S <= 1.1:
        o.append(f'<text x="{X0+4}" y="{base-40}" font-size="{6*S:.1f}" fill="{INK2}">FADE: the movement eases in</text>')
        o.append(f'<text x="{X1}" y="{base-40}" font-size="{6*S:.1f}" fill="{INK2}" text-anchor="end">SYNC 4BAR: one slow breath every four bars</text>')
    else:
        o.append(f'<text x="{X0+4}" y="{base-46}" font-size="{6*S:.1f}" fill="{INK2}">FADE:</text><text x="{X0+4}" y="{base-38}" font-size="{6*S:.1f}" fill="{INK2}">eases in</text>')
        o.append(f'<text x="{X1}" y="{base-46}" font-size="{6*S:.1f}" fill="{INK2}" text-anchor="end">SYNC 4BAR:</text><text x="{X1}" y="{base-38}" font-size="{6*S:.1f}" fill="{INK2}" text-anchor="end">one breath per four bars</text>')
    y = 104 if S <= 1.1 else 110
    for ln in wrap("LFO DEST set to FLT: the LFO turns the brightness for you, round and round. WAVE SIN keeps it smooth; RATE is ignored while SYNC is on.", int(100/S)):
        o.append(f'<text x="{X0}" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    return svg(W, int(y - 2), o)

# ------------------------------------------------------------------ L3: overdub passes on one loop
def overdub_stack(S=1.0):
    W = 352
    o = []
    rows = [("pass 1", "the free take: your chords", [(0, 60), (62, 60), (124, 60), (186, 60)], 1.0),
            ("pass 2", "REC while it plays: more notes on top", [(30, 10), (92, 10), (154, 10), (216, 10), (236, 10)], .75),
            ("pass 3", "and again, whenever you like", [(10, 6), (70, 6), (134, 6), (194, 6)], .5)]
    if S <= 1.1:
        X0, LW = 86, 250
        for i, (name, what, notes, op) in enumerate(rows):
            y = 10 + i * 24
            o.append(f'<text x="0" y="{y+9}" {DISP} font-size="{8*S:.1f}" font-weight="600" fill="{INK}">{name}</text>')
            o.append(f'<text x="0" y="{y+17}" font-size="{5.4*S:.1f}" fill="{INK3}">{what}</text>')
            o.append(f'<rect x="{X0}" y="{y}" width="{LW}" height="18" rx="4" fill="{T1}" opacity=".10"/>')
            for st, l in notes:
                o.append(f'<rect x="{X0+2+st:.1f}" y="{y+4}" width="{l}" height="10" rx="3" fill="{T1}" opacity="{op}"/>')
        o.append(f'<line x1="{X0}" y1="6" x2="{X0}" y2="82" stroke="{INK}" stroke-width=".6"/><line x1="{X0+LW}" y1="6" x2="{X0+LW}" y2="82" stroke="{INK}" stroke-width=".6"/>')
        y = 92
    else:
        X0, LW = 0, 352; sc = LW / 250
        y = 0
        for i, (name, what, notes, op) in enumerate(rows):
            o.append(f'<text x="0" y="{y+9:.1f}" {DISP} font-size="{8*S:.1f}" font-weight="600" fill="{INK}">{name}</text>')
            o.append(f'<text x="{W}" y="{y+9:.1f}" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="end">{what}</text>')
            o.append(f'<rect x="0" y="{y+13:.1f}" width="{LW}" height="20" rx="4" fill="{T1}" opacity=".10"/>')
            for st, l in notes:
                o.append(f'<rect x="{2+st*sc:.1f}" y="{y+17:.1f}" width="{l*sc:.1f}" height="12" rx="3" fill="{T1}" opacity="{op}"/>')
            y += 40
        o.append(f'<line x1="0.5" y1="10" x2="0.5" y2="{y-6}" stroke="{INK}" stroke-width=".6"/><line x1="{LW-.5}" y1="10" x2="{LW-.5}" y2="{y-6}" stroke="{INK}" stroke-width=".6"/>')
        y += 4
    for ln in wrap("one loop, the same length every time; every pass joins what is already there", int(118/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    return svg(W, int(y - 2), o)

# ------------------------------------------------------------------ L5: the white keys with CHORD on
def chord_keys(S=1.0):
    if S > 1.1: return chord_keys_rows(S)
    W = 352
    o = []
    kw = 21.5
    o.append(f'<text x="0" y="10" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">With CHORD on, the white keys walk the scale from key 5 (C4)</text>')
    sub = wrap("one finger, one chord: key 5 is the home chord (I); each key up is the next chord along, the keys below carry on downwards.", int(116/S))
    y = 20
    for ln in sub:
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.2 * S
    K = y + 2   # top of the keys
    degrees = ["IV", "V", "VI", "VII", "I", "II", "III", "IV", "V", "VI", "VII", "I", "II", "III", "IV", "V"]
    for i in range(16):
        x = i * kw; home = i == 4 or i == 11
        o.append(f'<rect x="{x:.1f}" y="{K:.1f}" width="{kw-1.6:.1f}" height="54" rx="4" fill="#fff" stroke="{T2 if home else "#bdb6a8"}" stroke-width="{1.4 if home else .5}"/>')
        o.append(f'<text x="{x+(kw-1.6)/2:.1f}" y="{K+14:.1f}" {MONO} font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">{i+1}</text>')
        o.append(f'<text x="{x+(kw-1.6)/2:.1f}" y="{K+36:.1f}" {DISP} font-size="{10*S:.1f}" font-weight="600" fill="{T2 if home else INK}" text-anchor="middle">{degrees[i]}</text>')
        o.append(f'<text x="{x+(kw-1.6)/2:.1f}" y="{K+48:.1f}" font-size="{5.2*S:.1f}" fill="{INK3}" text-anchor="middle">chord</text>')
    # black keys shown silent
    for i in (0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14):
        x = i * kw + kw - 0.8
        o.append(f'<rect x="{x-5:.1f}" y="{K:.1f}" width="10" height="26" rx="2.5" fill="#1c1c1e" opacity=".35"/>')
    o.append(f'<text x="{4*kw+(kw-1.6)/2:.1f}" y="{K+66:.1f}" font-size="{6.2*S:.1f}" font-weight="600" fill="{T2}" text-anchor="middle">home</text>')
    o.append(f'<text x="{11*kw+(kw-1.6)/2:.1f}" y="{K+66:.1f}" font-size="{6.2*S:.1f}" font-weight="600" fill="{T2}" text-anchor="middle">home, an octave up</text>')
    y = K + 78
    o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK3}">Black keys fall silent here; CHORD+ (next page) gives them a new job.</text>')
    y += 8 * S
    for ln in wrap("The lesson's journey, key 5 › 10 › 8 › 9, is I › VI › IV › V: the four chords under a thousand gentle songs.", int(116/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.2 * S
    return svg(W, int(y - 3), o)

def chord_keys_rows(S=1.3):
    """iPad: the 16 white keys as two rows of eight, large enough to read"""
    W = 352; o = []
    degrees = ["IV", "V", "VI", "VII", "I", "II", "III", "IV", "V", "VI", "VII", "I", "II", "III", "IV", "V"]
    o.append(f'<text x="0" y="11" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">With CHORD on, the white keys walk the scale from key 5 (C4)</text>')
    y = 22
    for ln in wrap("one finger, one chord: key 5 is the home chord (I); each key up is the next chord along, the keys below carry on downwards.", int(96/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    kw = 44; KH = 60
    blacks = (0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14)
    for row in range(2):
        K = y + 4 + row * (KH + 26)
        for j in range(8):
            i = row * 8 + j; x = j * kw; home = i in (4, 11)
            o.append(f'<rect x="{x:.1f}" y="{K:.1f}" width="{kw-2.4:.1f}" height="{KH}" rx="5" fill="#fff" stroke="{T2 if home else "#bdb6a8"}" stroke-width="{1.6 if home else .5}"/>')
            o.append(f'<text x="{x+(kw-2.4)/2:.1f}" y="{K+15:.1f}" {MONO} font-size="{6.4*S:.1f}" fill="{INK3}" text-anchor="middle">{i+1}</text>')
            o.append(f'<text x="{x+(kw-2.4)/2:.1f}" y="{K+40:.1f}" {DISP} font-size="{12*S:.1f}" font-weight="600" fill="{T2 if home else INK}" text-anchor="middle">{degrees[i]}</text>')
            o.append(f'<text x="{x+(kw-2.4)/2:.1f}" y="{K+53:.1f}" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">chord</text>')
            if i in blacks and j < 7:
                o.append(f'<rect x="{x+kw-2.4-5:.1f}" y="{K:.1f}" width="10" height="28" rx="2.5" fill="#1c1c1e" opacity=".35"/>')
            if home:
                o.append(f'<text x="{x+(kw-2.4)/2:.1f}" y="{K+KH+11:.1f}" font-size="{6.4*S:.1f}" font-weight="600" fill="{T2}" text-anchor="middle">{"home" if i == 4 else "home, an octave up"}</text>')
    y = y + 4 + 2 * (KH + 26) + 2
    o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK3}">Black keys fall silent here; CHORD+ (next page) gives them a new job.</text>'); y += 8 * S
    for ln in wrap("The lesson's journey, key 5 › 10 › 8 › 9, is I › VI › IV › V: the four chords under a thousand gentle songs.", int(96/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    return svg(W, int(y - 2), o)

def chordplus_keys(S=1.0):
    if S > 1.1: return chordplus_rows(S)
    W, H = 352, 82
    o = []
    fn = {"F#": "major / minor", "G#": "adds the 7th", "A#": "sus4", "C#": "adds the 9th", "D#": "an inversion"}
    names = ["F#", "G#", "A#", "C#", "D#", "F#", "G#", "A#", "C#", "D#", "F#"]
    slots = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14]
    kw = 21.5
    for i in range(16):
        o.append(f'<rect x="{i*kw:.1f}" y="40" width="{kw-1.6:.1f}" height="36" rx="4" fill="#fff" stroke="#bdb6a8" stroke-width=".5"/>')
    for n, i in zip(names, slots):
        x = i * kw + kw - 0.8
        o.append(f'<rect x="{x-6:.1f}" y="40" width="12" height="22" rx="2.5" fill="#1c1c1e"/>')
        o.append(f'<text x="{x:.1f}" y="55" {MONO} font-size="{5.2*S:.1f}" font-weight="600" fill="#f1efe9" text-anchor="middle">{n}</text>')
    o.append(f'<text x="0" y="10" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">CHORD+: hold a black key and the chord under your finger changes</text>')
    # legend row
    lx = 0
    for k, v in fn.items():
        o.append(f'<rect x="{lx}" y="18" width="14" height="10" rx="2" fill="#1c1c1e"/><text x="{lx+7}" y="25.2" {MONO} font-size="{5.4*S:.1f}" font-weight="600" fill="#f1efe9" text-anchor="middle">{k}</text>')
        o.append(f'<text x="{lx+17}" y="25.5" font-size="{6*S:.1f}" fill="{INK}">{v}</text>')
        lx += 70
    o.append(f'<text x="0" y="36" font-size="{5.6*S:.1f}" fill="{INK3}">both octaves of black keys work, and you can hold several at once</text>')
    return svg(W, H, o)

def chordplus_rows(S=1.3):
    W = 352; o = []
    fn = {"F#": "major / minor", "G#": "adds the 7th", "A#": "sus4", "C#": "adds the 9th", "D#": "an inversion"}
    o.append(f'<text x="0" y="11" {DISP} font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">CHORD+: hold a black key and the chord changes</text>')
    y = 24
    items = list(fn.items())
    for r in range(0, 5, 2):
        for c, (k, v) in enumerate(items[r:r+2]):
            lx = c * 176
            o.append(f'<rect x="{lx}" y="{y-9}" width="22" height="13" rx="2.5" fill="#1c1c1e"/><text x="{lx+11}" y="{y}" {MONO} font-size="{6.4*S:.1f}" font-weight="600" fill="#f2f0ea" text-anchor="middle">{k}</text>')
            o.append(f'<text x="{lx+28}" y="{y}" font-size="{6.6*S:.1f}" fill="{INK}">{v}</text>')
        y += 15
    o.append(f'<text x="0" y="{y+2:.1f}" font-size="{6*S:.1f}" fill="{INK3}">both octaves of black keys work, and you can hold several at once</text>')
    y += 12
    # one octave row (keys 1-8 then 9-16), black keys named
    names = ["F#", "G#", "A#", "C#", "D#", "F#", "G#", "A#", "C#", "D#", "F#"]
    slots = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14]
    kw = 44; KH = 44
    for row in range(2):
        K = y + row * (KH + 8)
        for j in range(8):
            o.append(f'<rect x="{j*kw:.1f}" y="{K:.1f}" width="{kw-2.4:.1f}" height="{KH}" rx="5" fill="#fff" stroke="#bdb6a8" stroke-width=".5"/>')
        for n, i in zip(names, slots):
            if i // 8 != row or i % 8 == 7: continue
            j = i % 8; x = j * kw + kw - 2.4
            o.append(f'<rect x="{x-9:.1f}" y="{K:.1f}" width="18" height="26" rx="3" fill="#1c1c1e"/>')
            o.append(f'<text x="{x:.1f}" y="{K+17:.1f}" {MONO} font-size="{6.4*S:.1f}" font-weight="600" fill="#f2f0ea" text-anchor="middle">{n}</text>')
    y += 2 * (KH + 8)
    return svg(W, int(y), o)

# ------------------------------------------------------------------ L6: two weights from two buttons; one pattern, many kits
def drum_dynamics(S=1.0):
    """left: OCT- ghost / plain / OCT+ hard. right: the same recorded pattern under different kits (PRESETS on track 4)."""
    W = 352
    o = []
    # ---- left panel
    o.append(f'<text x="0" y="10" {DISP} font-size="{8.4*S:.1f}" font-weight="600" fill="{INK}">Three weights from two buttons</text>')
    hits = [("OCT− held", "ghost", 14, .32, True), ("plain tap", "normal", 24, .78, False), ("OCT+ held", "hard", 34, 1.0, False)]
    base = 66
    for i, (how, name, h, op, outline) in enumerate(hits):
        x = 6 + i * 54
        o.append(f'<rect x="{x}" y="{base-h}" width="22" height="{h}" rx="4" fill="{T4}" opacity="{op}"/>')
        if outline: o.append(f'<rect x="{x+.6}" y="{base-h+.6}" width="20.8" height="{h-1.2}" rx="3.5" fill="none" stroke="{T4}" stroke-width="1"/>')
        o.append(f'<text x="{x+11}" y="{base+10}" {DISP} font-size="{7*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">{name}</text>')
        o.append(f'<text x="{x+11}" y="{base+18}" {MONO} font-size="{5.2*S:.1f}" fill="{INK3}" text-anchor="middle">{how}</text>')
    y = base + 30
    for ln in wrap("The keys cannot feel how hard you press: these two buttons are your touch, and they record exactly as played.", int(52/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{5.8*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.2 * S
    yl = y
    # ---- right panel
    X = 186
    o.append(f'<text x="{X}" y="10" {DISP} font-size="{8.4*S:.1f}" font-weight="600" fill="{INK}">One pattern, thirty-seven kits</text>')
    kits = ["AMBIENT", "LO-FI", "JAZZ", "BOOMBAP", "DUST"]
    kx = X
    for k, kit in enumerate(kits):
        w = pill(o, kx, 18, kit, fill=(INK if k == 1 else WASH), fg=("#f2f0ea" if k == 1 else INK), S=S)
        kx += w + 3
    o.append(f'<text x="{X}" y="{36}" {MONO} font-size="{5.2*S:.1f}" fill="{INK3}">PRESETS on track 4 walks the kits</text>')
    # the same pattern, three lanes
    lanes = [("hat", [0, 2, 4, 6, 8, 10, 12, 14], .55), ("snare", [4, 12], .85), ("kick", [0, 10], 1.0)]
    sw = (W - X) / 16
    for li, (name, steps, op) in enumerate(lanes):
        y0 = 42 + li * 11
        o.append(f'<text x="{X-3}" y="{y0+7.5}" {MONO} font-size="{5*S:.1f}" fill="{INK3}" text-anchor="end"> </text>')
        for st in range(16):
            on = st in steps
            o.append(f'<rect x="{X+st*sw+.6:.1f}" y="{y0}" width="{sw-1.2:.1f}" height="9" rx="2" fill="{T4 if on else EMPTY}" opacity="{op if on else 1}"/>')
    o.append(f'<text x="{X}" y="{42+3*11+8}" {MONO} font-size="{5*S:.1f}" fill="{INK3}">hat · snare · kick: the pattern from the next page</text>')
    y = 42 + 3 * 11 + 20
    for ln in wrap("Changing kit never changes a recorded pattern; the sequencer keeps the hits, the kit supplies the sounds, so you can swap kits under a beat forever.", int(52/S)):
        o.append(f'<text x="{X}" y="{y:.1f}" font-size="{5.8*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.2 * S
    return svg(W, int(max(y, yl)) + 2, o)


# ------------------------------------------------------------------ L7: a step holds four notes
def four_note_step(S=1.0):
    W, H = 352, 92
    o = []
    cases = [("a TRIAD chord on the step", [T2, T2, T2, None], "three notes used, one spare"),
             ("a melody note on the same step", [T2, T2, T2, "M"], "four notes: the step is full"),
             ("one more note arrives", [T2, T2, "M", "M"], "the oldest held note gives way")]
    for i, (title, slots, note) in enumerate(cases):
        x = i * 118
        o.append(f'<text x="{x}" y="10" {DISP} font-size="{7.4*S:.1f}" font-weight="600" fill="{INK}">{title}</text>')
        for k, c in enumerate(slots):
            if c == "M":
                o.append(f'<rect x="{x+k*25}" y="18" width="21" height="34" rx="4" fill="{T2}" opacity=".38"/><rect x="{x+k*25+.6}" y="18.6" width="19.8" height="32.8" rx="3.6" fill="none" stroke="{T2}" stroke-width="1.2"/>')
            else:
                o.append(f'<rect x="{x+k*25}" y="18" width="21" height="34" rx="4" fill="{c or EMPTY}" stroke="{INK3 if c is None else "none"}" stroke-width=".6" stroke-dasharray="2 1.6"/>')
        o.append(f'<text x="{x}" y="64" font-size="{5.8*S:.1f}" fill="{INK2}">{note}</text>')
    o.append(f'<rect x="0" y="74" width="10" height="7" rx="2" fill="{T2}"/><text x="14" y="80" font-size="{5.8*S:.1f}" fill="{INK2}">chord notes (track 2\'s Rhodes)</text>')
    o.append(f'<rect x="120" y="74" width="10" height="7" rx="2" fill="{T2}" opacity=".38"/><rect x="120.5" y="74.5" width="9" height="6" rx="1.6" fill="none" stroke="{T2}" stroke-width="1"/><text x="134" y="80" font-size="{5.8*S:.1f}" fill="{INK2}">melody notes: the same track, the same Rhodes, an octave up</text>')
    o.append(f'<text x="0" y="90" font-size="{5.8*S:.1f}" fill="{INK3}">so: place melody notes mostly between the chord hits, where every slot is free</text>')
    return svg(W, H, o)

# ------------------------------------------------------------------ L8: 64 steps, four pages
def step_pages(S=1.0):
    W, H = 352, 74
    o = []
    for p in range(4):
        x = p * 88
        o.append(f'<rect x="{x}" y="14" width="80" height="30" rx="4" fill="{"#fff" if p else CARD}" stroke="{INK if p==0 else "#bdb6a8"}" stroke-width="{1 if p==0 else .5}"/>')
        for i in range(16):
            o.append(f'<rect x="{x+4+i*4.7:.1f}" y="20" width="3.4" height="18" rx="1" fill="{T4 if i in (0,2,4,6,8,10,11,12,14) else EMPTY}"/>')
        o.append(f'<text x="{x}" y="10" {MONO} font-size="{6*S:.1f}" font-weight="600" fill="{INK}">page {p+1}</text>')
        o.append(f'<text x="{x+80}" y="10" {MONO} font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="end">steps {p*16+1}–{p*16+16}</text>')
        o.append(f'<text x="{x+40}" y="54" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">bar {p+1}</text>')
        if p < 3:
            o.append(f'<text x="{x+84}" y="31" {MONO} font-size="{6*S:.1f}" fill="{INK}" text-anchor="middle">›</text>')
    o.append(f'<text x="0" y="66" font-size="{6*S:.1f}" fill="{INK2}">the four-bar take, one bar per page; the screen shows 16 steps at a time,</text>')
    o.append(f'<text x="0" y="74" font-size="{6*S:.1f}" fill="{INK2}">OCT− / OCT+ turn the page, and the keys always edit the page on screen</text>')
    return svg(W, 80, o)

# ------------------------------------------------------------------ L9: a punch-in lasts as long as the finger
def punch_timeline(S=1.0):
    W, H = 352, 96
    o = []
    X0, X1 = 70, 340
    for b in range(5):
        x = X0 + b * (X1 - X0) / 4
        o.append(f'<line x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="80" stroke="{INK3}" stroke-width=".5" stroke-dasharray="1.6 1.8"/>')
    # finger on the key
    fx0, fx1 = X0 + 60, X0 + 170
    o.append(f'<text x="0" y="28" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}">FX + a key</text>')
    o.append(f'<rect x="{fx0}" y="18" width="{fx1-fx0}" height="12" rx="6" fill="{INK}"/>')
    o.append(f'<text x="{(fx0+fx1)/2:.1f}" y="26.5" {MONO} font-size="{5.6*S:.1f}" fill="#f2f0ea" text-anchor="middle">held</text>')
    # effect: on while held, with the fade setting easing in and out
    o.append(f'<text x="0" y="56" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}">the effect</text>')
    pts = [f"{X0},72"]
    for i in range(0, 271):
        x = X0 + i; u = 0
        if fx0 <= x <= fx1: u = min(1, (x - fx0) / 8, (fx1 - x) / 8)
        pts.append(f"{x:.1f},{72-26*u:.1f}")
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{SIG}" stroke-width="2.2" stroke-linejoin="round"/>')
    o.append(f'<text x="{fx0+2}" y="40" font-size="{5.6*S:.1f}" fill="{SIG}">starts on the grid</text>')
    o.append(f'<text x="{fx1+3}" y="68" font-size="{5.6*S:.1f}" fill="{SIG}">lets go cleanly</text>')
    o.append(f'<text x="{X0}" y="90" font-size="{6*S:.1f}" fill="{INK2}">exactly as long as your finger; never recorded.</text>')
    y = 98
    for ln in wrap("The fade setting (FX held, then SELECT) softens the edges: 0 instant, 15 about a third of a second.", int(112/S)):
        o.append(f'<text x="{X0}" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    return svg(W, int(y - 1), o)

def fill_strip(S=1.0):
    W, H = 352, 108
    o = []
    bw = 80; g = 8
    for b in range(4):
        x = b * (bw + g)
        o.append(f'<rect x="{x}" y="22" width="{bw}" height="22" rx="4" fill="{T4}" opacity="{.9 if b%2==0 else .7}"/>')
        o.append(f'<text x="{x+4}" y="16" {MONO} font-size="{6*S:.1f}" font-weight="600" fill="{INK}">bar {b+1}</text>')
        o.append(f'<text x="{x+bw}" y="16" {MONO} font-size="{5.4*S:.1f}" fill="{INK3}" text-anchor="end">page {b+1}</text>')
        for i in range(16):
            sx = x + 3 + i * 4.75
            last = i == 15
            if b == 0 and last:
                o.append(f'<rect x="{sx:.1f}" y="26" width="3.6" height="14" rx="1" fill="#fff"/>')
                o.append(f'<text x="{sx+1.8:.1f}" y="35.5" {MONO} font-size="4.6" font-weight="700" fill="{T4}" text-anchor="middle">F</text>')
            elif last:
                o.append(f'<rect x="{sx:.1f}" y="26" width="3.6" height="14" rx="1" fill="none" stroke="#fff" stroke-width=".7" stroke-dasharray="1.2 1"/>')
            else:
                o.append(f'<rect x="{sx:.1f}" y="29" width="3.6" height="8" rx="1" fill="#fff" opacity="{.75 if i%2==0 else .3}"/>')
    # the held fill across a full round
    o.append(f'<rect x="0" y="54" width="{4*bw+3*g}" height="9" rx="4.5" fill="{INK}"/>')
    o.append(f'<text x="{(4*bw+3*g)/2:.1f}" y="60.6" {MONO} font-size="{5.6*S:.1f}" fill="#f2f0ea" text-anchor="middle">GLO + key 9, held through one full round</text>')
    o.append(f'<path d="M{3+15*4.75+1.8:.1f},46 L{3+15*4.75+1.8:.1f},52" stroke="{INK}" stroke-width=".9"/>')
    y = 78
    for j, ln in enumerate(wrap("F = a FILL ONLY step: the crash on step 16 of bar 1 plays only while a fill is on, so it rings once per round, when the playhead crosses it with key 9 held. The condition belongs to the whole step, every sound in it, which is why the crash sits on an empty step.", int(112/S))):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.4 * S
    for ln in wrap("dashed: the last step of pages 2, 3 and 4, where the same mark makes a crash greet every fill bar (GLO + key 10).", int(112/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6*S:.1f}" fill="{INK3}">{ln}</text>'); y += 7.4 * S
    return svg(W, int(y - 1), o)

# ------------------------------------------------------------------ L10: sections on the bar
def section_timeline(S=1.0):
    W = 352
    o = []
    # sections A-D are not tracks: a tonal scale, never the track colours
    cols = {"A": "#e6e1d5", "B": "#a8a49a", "C": "#6e6a62", "D": "#43434a"}
    fg = {"A": "#1a1a1e", "B": "#1a1a1e", "C": "#f2efe8", "D": "#f2efe8"}
    o.append(f'<text x="0" y="12" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}">SAVE + key 1–4 while playing: the new section starts on the next bar</text>')
    bw = 42
    seq = ["A", "A", "A", "B", "B", "B", "B", "C"]
    for i, sname in enumerate(seq):
        o.append(f'<rect x="{i*bw}" y="18" width="{bw-2}" height="16" rx="3" fill="{cols[sname]}"/>')
        o.append(f'<text x="{i*bw+(bw-2)/2:.1f}" y="29" {MONO} font-size="{6.4*S:.1f}" font-weight="600" fill="{fg[sname]}" text-anchor="middle">{sname}</text>')
    px = 2 * bw + 14
    o.append(f'<circle cx="{px}" cy="40" r="1.8" fill="{SIG}"/><path d="M{px},40 L{px},35" stroke="{SIG}" stroke-width="1"/>')
    o.append(f'<text x="{px-5}" y="43" font-size="{5.6*S:.1f}" fill="{INK2}" text-anchor="end">SAVE + key 2, pressed here</text>')
    o.append(f'<path d="M{3*bw-1},36 L{3*bw-1},54" stroke="{SIG}" stroke-width="1"/>')
    o.append(f'<text x="{3*bw+3}" y="57" font-size="{5.6*S:.1f}" fill="{INK2}">B begins at the next bar line, every track from its first step</text>')
    o.append(f'<text x="0" y="74" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}">A quick chain, A B B C, tapped while SAVE stays held:</text>')
    o.append(f'<text x="0" y="83" font-size="{6*S:.1f}" fill="{INK2}">each section plays for its own pattern length, round and round</text>')
    chain = ["A", "B", "B", "C", "A", "B", "B", "C"]
    for i, sname in enumerate(chain):
        o.append(f'<rect x="{i*bw}" y="89" width="{bw-2}" height="16" rx="3" fill="{cols[sname]}" opacity="{1 if i<4 else .45}"/>')
        o.append(f'<text x="{i*bw+(bw-2)/2:.1f}" y="100" {MONO} font-size="{6.4*S:.1f}" font-weight="600" fill="{fg[sname]}" text-anchor="middle">{sname}</text>')
    o.append(f'<text x="0" y="116" font-size="{5.6*S:.1f}" fill="{INK3}">SONG REC (SAVE + key 14) writes down which sections you played, and for how many bars</text>')
    return svg(W, 120, o)

# ------------------------------------------------------------------ ch14: the editor map, and the audio path
def _fm1_small(o, x, y, S=1.0, label=True):
    o.append(f'<rect x="{x}" y="{y}" width="112" height="68" rx="7" fill="#3a3a3d" stroke="#1e1e20" stroke-width=".8"/>')
    o.append(f'<rect x="{x+30}" y="{y+6}" width="26" height="26" rx="3" fill="#0c0c0e"/>')
    for i, c in enumerate((T1, T2, T3, T4)):
        o.append(f'<circle cx="{x+36+i*6}" cy="{y+27}" r="1.8" fill="none" stroke="{c}" stroke-width=".9"/>')
    for i in range(4): o.append(f'<circle cx="{x+68+i*11}" cy="{y+11}" r="3" fill="#202023"/>')
    for r in range(2):
        for c in range(6): o.append(f'<rect x="{x+62+c*8.2}" y="{y+18+r*7}" width="6.6" height="5.4" rx="1" fill="#1c1c1e"/>')
    for i in range(16): o.append(f'<rect x="{x+5+i*6.6}" y="{y+46}" width="4.6" height="16" rx="2.3" fill="#1c1c1e"/>')
    for i, p in enumerate((1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0)):
        if p: o.append(f'<rect x="{x+8+i*6.6}" y="{y+36}" width="4.6" height="9" rx="2.3" fill="#1c1c1e"/>')
    if label:
        o.append(f'<text x="{x+56}" y="{y+82}" {DISP} font-size="{10*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">FM-1</text>')
        o.append(f'<text x="{x+56}" y="{y+91}" font-size="{6*S:.1f}" fill="{INK2}" text-anchor="middle">running SLOOP</text>')

def editor_map(S=1.0):
    """FM-1 ↔ one cable ↔ the browser editor. Schematic: the browser is drawn, not a screenshot."""
    W, H = 352, 150
    o = []
    _fm1_small(o, 8, 40, S)
    # cable
    o.append(f'<path d="M120,74 L196,74" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<rect x="118" y="69" width="8" height="10" rx="1.5" fill="{INK}"/><rect x="190" y="69" width="8" height="10" rx="1.5" fill="{INK}"/>')
    o.append(f'<text x="158" y="62" {MONO} font-size="{6.4*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">USB-C</text>')
    o.append(f'<text x="158" y="90" font-size="{5.8*S:.1f}" fill="{INK2}" text-anchor="middle">a data cable,</text>')
    o.append(f'<text x="158" y="98" font-size="{5.8*S:.1f}" fill="{INK2}" text-anchor="middle">straight in, no hub;</text>')
    o.append(f'<text x="158" y="106" font-size="{5.8*S:.1f}" fill="{INK2}" text-anchor="middle">MIDI runs both ways</text>')
    o.append(f'<path d="M150,108 L166,108" stroke="{INK3}" stroke-width=".8"/><path d="M153,105 L150,108 L153,111 M163,105 L166,108 L163,111" fill="none" stroke="{INK3}" stroke-width=".8"/>')
    # browser window (schematic)
    bx, by, bw, bh = 200, 14, 152, 112
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{CARD}" stroke="{INK}" stroke-width=".9"/>')
    o.append(f'<path d="M{bx},{by+12} H{bx+bw}" stroke="{INK}" stroke-width=".6"/>')
    for i in range(3): o.append(f'<circle cx="{bx+8+i*7}" cy="{by+6}" r="2" fill="{INK3}"/>')
    o.append(f'<text x="{bx+30}" y="{by+8.5}" {MONO} font-size="{5*S:.1f}" fill="{INK2}">isod89.github.io/sloop-fm1/webapp/editor</text>')
    # sidebar: the real page names
    for i, (nm, hot) in enumerate((("LIVE", 0), ("Sound", 1), ("Sequencer", 0), ("Library", 0), ("Song &amp; sections", 1), ("Settings", 0))):
        y = by + 26 + i * 12
        if hot: o.append(f'<rect x="{bx+5}" y="{y-8}" width="52" height="11" rx="2" fill="{WASH}"/>')
        o.append(f'<text x="{bx+8}" y="{y}" {MONO} font-size="{5.6*S:.1f}" fill="{INK if hot else INK3}">{nm}</text>')
    # body: knobs as tiles + a Connect button
    o.append(f'<rect x="{bx+66}" y="{by+20}" width="80" height="12" rx="3" fill="{INK}"/><text x="{bx+106}" y="{by+28.5}" {MONO} font-size="{5.8*S:.1f}" font-weight="600" fill="#f2f0ea" text-anchor="middle">Connect</text>')
    for i, c in enumerate((T1, T2, T3, T4)):
        o.append(f'<rect x="{bx+66+i*20}" y="{by+40}" width="17" height="22" rx="3" fill="{c}" opacity=".85"/>')
        o.append(f'<rect x="{bx+66+i*20+4}" y="{by+44+ (i*3)%8}" width="9" height="2.4" rx="1" fill="#fff" opacity=".9"/>')
    o.append(f'<text x="{bx+66}" y="{by+72}" font-size="{5.4*S:.1f}" fill="{INK2}">every value is a tile you drag</text>')
    o.append(f'<text x="{bx+66}" y="{by+80}" font-size="{5.4*S:.1f}" fill="{INK2}">up or down like a knob</text>')
    o.append(f'<rect x="{bx+66}" y="{by+88}" width="68" height="12" rx="3" fill="{SIG}"/><text x="{bx+100}" y="{by+96.5}" {MONO} font-size="{5.8*S:.1f}" font-weight="600" fill="#fff" text-anchor="middle">Save a backup</text>')
    o.append(f'<text x="{bx+bw/2}" y="{by+bh+12}" {DISP} font-size="{10*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">the web editor</text>')
    o.append(f'<text x="{bx+bw/2}" y="{by+bh+21}" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">drawn, not a screenshot; details simplified</text>')
    return svg(W, H, o)

def audio_path(S=1.0):
    """the recording path: FM-1 → USB audio (the input named Felucca) → a GarageBand audio track"""
    W, H = 352, 128
    o = []
    _fm1_small(o, 8, 22, S)
    # device setting callout
    o.append(f'<text x="8" y="12" {MONO} font-size="{5.8*S:.1f}" fill="{INK}">hold HOME · AUDIO · USB AUDIO = FULL</text>')
    # cable, carrying audio
    o.append(f'<path d="M120,56 L196,56" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<rect x="118" y="51" width="8" height="10" rx="1.5" fill="{INK}"/><rect x="190" y="51" width="8" height="10" rx="1.5" fill="{INK}"/>')
    pts = " ".join(f"{x},{44 + 4*math.sin(x/3.2):.1f}" for x in range(128, 190, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{SIG}" stroke-width="1.2"/>')
    o.append(f'<text x="158" y="36" {MONO} font-size="{6*S:.1f}" font-weight="600" fill="{SIG}" text-anchor="middle">audio, on the same cable</text>')
    o.append(f'<text x="158" y="74" font-size="{5.8*S:.1f}" fill="{INK2}" text-anchor="middle">the Mac sees an input</text>')
    o.append(f'<text x="158" y="83" font-size="{5.8*S:.1f}" fill="{INK2}" text-anchor="middle">named <tspan font-weight="600" fill="{INK}">Felucca</tspan></text>')
    # GarageBand window (schematic)
    gx, gy, gw, gh = 200, 14, 152, 84
    o.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="6" fill="{CARD}" stroke="{INK}" stroke-width=".9"/>')
    o.append(f'<path d="M{gx},{gy+12} H{gx+gw}" stroke="{INK}" stroke-width=".6"/>')
    for i in range(3): o.append(f'<circle cx="{gx+8+i*7}" cy="{gy+6}" r="2" fill="{INK3}"/>')
    o.append(f'<text x="{gx+30}" y="{gy+8.5}" {DISP} font-size="{6*S:.1f}" font-weight="600" fill="{INK}">GarageBand</text>')
    o.append(f'<text x="{gx+8}" y="{gy+24}" font-size="{5.6*S:.1f}" fill="{INK2}">Settings › Audio/MIDI › Input Device: <tspan font-weight="600" fill="{INK}">Felucca</tspan></text>')
    o.append(f'<rect x="{gx+8}" y="{gy+32}" width="{gw-16}" height="24" rx="3" fill="{WASH}"/>')
    o.append(f'<circle cx="{gx+16}" cy="{gy+44}" r="3.4" fill="#c0392b"/>')
    o.append(f'<text x="{gx+24}" y="{gy+40}" {MONO} font-size="{5.2*S:.1f}" fill="{INK2}">Audio track · input 1 + 2 (stereo) · armed</text>')
    pts = " ".join(f"{x},{gy+48 + 4*math.sin(x/5)*math.sin(x/23):.1f}" for x in range(gx+24, gx+gw-12, 2))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{SIG}" stroke-width="1"/>')
    o.append(f'<text x="{gx+8}" y="{gy+68}" font-size="{5.4*S:.1f}" fill="{INK2}">software monitoring off: listen on the FM-1\'s own output</text>')
    o.append(f'<text x="{gx+8}" y="{gy+77}" font-size="{5.4*S:.1f}" fill="{INK2}">what you capture is exactly what the headphones hear</text>')
    o.append(f'<text x="{gx+gw/2}" y="{gy+gh+11}" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">drawn, not a screenshot; menu names vary by version</text>')
    o.append(f'<text x="8" y="124" font-size="{6*S:.1f}" fill="{INK2}">Arm the track, press GarageBand\'s record button, then PLAY on the FM-1. Stop both when done.</text>')
    return svg(W, H, o)

# ------------------------------------------------------------------ p23: the counted take, corrected
def counted_take(S=1.0):
    """REC arms · PLAY starts the count-in · recording begins by itself · four bars · REC ends it"""
    W, H = 352, 78
    o = []
    def key(x, y, t, dark=True, w=30):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="12" rx="2.5" fill="{INK if dark else "#fff"}" stroke="{INK}" stroke-width=".7"/>')
        o.append(f'<text x="{x+w/2:.1f}" y="{y+8.4}" {MONO} font-size="{6*S:.1f}" font-weight="600" fill="{"#f2f0ea" if dark else INK}" text-anchor="middle">{t}</text>')
    # press REC (arm)
    key(0, 22, "REC"); o.append(f'<text x="0" y="44" font-size="{5.6*S:.1f}" fill="{INK2}">arm</text>')
    o.append(f'<text x="0" y="52" font-size="{5.2*S:.1f}" fill="{INK3}">set the dials</text>')
    # press PLAY
    key(40, 22, "PLAY"); o.append(f'<text x="55" y="44" font-size="{5.6*S:.1f}" fill="{INK2}" text-anchor="middle">count-in starts</text>')
    # count-in bar
    o.append(f'<rect x="78" y="20" width="56" height="16" rx="3" fill="none" stroke="{INK3}" stroke-width=".8" stroke-dasharray="2.4 2"/>')
    o.append(f'<text x="106" y="31" {DISP} font-size="{8*S:.1f}" font-weight="600" fill="{INK3}" text-anchor="middle">4 · 3 · 2 · 1</text>')
    o.append(f'<text x="106" y="44" font-size="{5.6*S:.1f}" fill="{INK3}" text-anchor="middle">one bar of clicks</text>')
    o.append(f'<text x="106" y="52" font-size="{5.2*S:.1f}" fill="{INK3}" text-anchor="middle">not recorded</text>')
    # recording begins by itself
    o.append(f'<path d="M136,28 L142,28" stroke="{T4}" stroke-width="1.6"/>')
    o.append(f'<text x="139" y="14" font-size="{5.6*S:.1f}" fill="{T4}" text-anchor="middle">recording begins by itself</text>')
    bw = 40
    for b in range(4):
        x = 144 + b * (bw + 4)
        o.append(f'<rect x="{x}" y="20" width="{bw}" height="16" rx="3" fill="{T4}" opacity="{.9 if b%2==0 else .72}"/>')
        o.append(f'<text x="{x+bw/2:.1f}" y="31" {DISP} font-size="{7.6*S:.1f}" font-weight="600" fill="#fff" text-anchor="middle">bar {b+1}</text>')
    o.append(f'<text x="{144+2*bw+4:.1f}" y="44" font-size="{5.6*S:.1f}" fill="{INK2}" text-anchor="middle">the pattern above, four times, counting 1 2 3 4 with the click</text>')
    # press REC to finish
    key(322, 22, "REC"); o.append(f'<text x="352" y="44" font-size="{5.6*S:.1f}" fill="{INK2}" text-anchor="end">finish</text>')
    o.append(f'<text x="352" y="52" font-size="{5.2*S:.1f}" fill="{INK3}" text-anchor="end">the loop plays on</text>')
    o.append(f'<text x="0" y="70" font-size="{5.8*S:.1f}" fill="{INK3}">Changed your mind during the count-in? REC cancels it.</text>')
    return svg(W, H, o)


import re as _re
def scale_fonts(svg_text, S):
    """multiply every numeric font-size in an SVG (for the iPad edition's larger lettering)"""
    return _re.sub(r'font-size="([0-9.]+)"', lambda m: f'font-size="{float(m.group(1))*S:.2f}"', svg_text)
