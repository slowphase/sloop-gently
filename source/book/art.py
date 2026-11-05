"""Original SVG artwork for SLOOP, Gently.
One motif, used sparingly: the loop, drawn as grain. Dots whose density and size follow a slow
wave, coloured by SLOOP's four tracks. Nothing is filtered or rasterised; the halftone is real dots,
so it prints cleanly and the PDF stays vector."""
import math, random

T = ["#2f6fde", "#22995a", "#e0a92a", "#e2661d"]

def _col(u, rng, spread=0.18):
    """colour by position u in 0..1 across the four tracks, with a soft random bleed at the borders"""
    u = min(max(u + rng.uniform(-spread, spread), 0), 0.999)
    return T[int(u * 4)]

def field(w=210, h=150, seed=7, n=5200, base_y=0.62, amp=0.22, dark=True):
    """cover: a wide granular wave. Dot size peaks on the crest; density fades with distance."""
    rng = random.Random(seed)
    o = [f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">']
    for _ in range(n):
        x = rng.random()
        yc = base_y + amp * (0.55 * math.sin(x * 6.0 + 0.4) + 0.3 * math.sin(x * 13.1 + 2.0) + 0.15 * math.sin(x * 29.0))
        d = rng.gauss(0, 0.085)
        y = yc + d
        if not (0.02 < y < 0.98):
            continue
        near = math.exp(-(d * d) / (2 * 0.03 ** 2))
        r = 0.22 + 1.15 * near * (0.6 + 0.4 * rng.random())
        op = 0.35 + 0.65 * near
        o.append(f'<circle cx="{x*w:.1f}" cy="{y*h:.1f}" r="{r:.2f}" fill="{_col(x, rng)}" opacity="{op:.2f}"/>')
    o.append("</svg>")
    return "\n".join(o)

def ring(size=120, seed=3, n=1400, stroke=False, playhead=True):
    """the loop: a ring of grain, one track colour per quarter, a little thicker where the beat lands"""
    rng = random.Random(seed)
    c = size / 2; R = size * 0.36
    o = [f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">']
    for _ in range(n):
        a = rng.random() * math.tau
        beat = 0.5 + 0.5 * math.cos(a * 4)          # four beats round the loop
        d = rng.gauss(0, size * (0.018 + 0.03 * beat))
        x = c + (R + d) * math.cos(a); y = c + (R + d) * math.sin(a)
        r = 0.25 + 0.9 * beat * rng.random() + 0.2
        col = T[int(((a + math.pi / 4) % math.tau) / math.tau * 4)]
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*size/120:.2f}" fill="{col}" opacity="{0.45+0.55*rng.random():.2f}"/>')
    # the playhead: one bright gap
    if playhead:
        o.append(f'<circle cx="{c + R*math.cos(-math.pi/2):.1f}" cy="{c + R*math.sin(-math.pi/2):.1f}" r="{size*0.022:.2f}" fill="#f2efe8"/>')
    o.append("</svg>")
    return "\n".join(o)

def ring_small(size=16, seed=5):
    return ring(size, seed, n=260)

def cloud(w=210, h=120, seed=11, n=4200):
    """atmosphere: a slow granular cloud, dense in the middle, thinning to nothing"""
    rng = random.Random(seed)
    o = [f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">']
    for _ in range(n):
        x = rng.gauss(0.5, 0.22); y = rng.gauss(0.55, 0.2)
        if not (0 < x < 1 and 0.02 < y < 0.98):
            continue
        dist = math.hypot((x - 0.5) / 0.26, (y - 0.55) / 0.22)
        near = math.exp(-dist * dist / 2)
        r = 0.2 + 1.6 * near * rng.random()
        o.append(f'<circle cx="{x*w:.1f}" cy="{y*h:.1f}" r="{r:.2f}" fill="{_col(x, rng, .3)}" opacity="{0.25+0.7*near:.2f}"/>')
    o.append("</svg>")
    return "\n".join(o)

def pulse(w=210, h=110, seed=2):
    """rhythm: sixteen columns of grain, pulsing where the pattern lands (kick 1 & 11, snare 5 & 13, hats on odd steps)"""
    rng = random.Random(seed)
    kick = {1, 11}; snare = {5, 13}; hat = {1, 3, 5, 7, 9, 11, 13, 15}
    o = [f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">']
    cw = w / 16
    for s in range(1, 17):
        energy = 0.18 + (0.6 if s in kick else 0) + (0.45 if s in snare else 0) + (0.2 if s in hat else 0)
        col = T[3] if s in kick else (T[0] if s in snare else (T[2] if s in hat else T[1]))
        for _ in range(int(220 * energy)):
            x = (s - 1 + rng.random()) * cw
            y = h * (1 - rng.random() ** 1.6 * energy * 0.95)
            r = 0.2 + 0.9 * rng.random() * energy
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" opacity="{0.35+0.6*rng.random():.2f}"/>')
    o.append("</svg>")
    return "\n".join(o)

def ribbons(w=210, h=120, seed=4):
    """performing: four long waves, each a track, crossing and uncrossing like hands on the keys"""
    rng = random.Random(seed)
    o = [f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">']
    for k, col in enumerate(T):
        pts = []
        for i in range(0, 211, 3):
            x = i; u = i / 210
            y = h * (0.5 + 0.28 * math.sin(u * 5.2 + k * 1.4) * math.sin(u * 1.7 + k) + 0.06 * math.sin(u * 23 + k * 3))
            pts.append(f"{x},{y:.1f}")
        for j in range(26):   # a ribbon drawn as many thin passes = grain
            dy = rng.gauss(0, 2.2)
            op = 0.06 + 0.1 * rng.random()
            o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{0.5+rng.random():.2f}" opacity="{op:.2f}" transform="translate(0,{dy:.1f})"/>')
    o.append("</svg>")
    return "\n".join(o)

def wave_icon():
    """the small four-colour wave in the 'you should now be hearing' band"""
    return ('<svg viewBox="0 0 96 30" class="wave"><defs><linearGradient id="gt" x1="0" x2="1">'
            '<stop offset="0" stop-color="#5b8ff0"/><stop offset=".36" stop-color="#3fbf7c"/>'
            '<stop offset=".68" stop-color="#f0bf45"/><stop offset="1" stop-color="#f08045"/></linearGradient></defs>'
            '<path d="M2,15 C8,1 14,1 20,15 S32,29 38,15 S48,4 54,15 S62,24 68,15 S74,9 79,15 S85,19 88,15 S92,13 94,15" '
            'fill="none" stroke="url(#gt)" stroke-width="2.4" stroke-linecap="round"/></svg>')

def pad_art(engine, seed):
    """a tiny vignette per sound: the engine's character, not an icon"""
    rng = random.Random(seed)
    o = ['<svg viewBox="0 0 100 22" class="art" preserveAspectRatio="none">']
    if engine == "ANALOG":
        pts = " ".join(f"{x},{11+7*math.sin(x/100*math.tau*1.5):.1f}" for x in range(0, 101, 2))
        o.append(f'<polyline points="{pts}" fill="none" stroke="#2f6fde" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>')
    elif engine == "GRAIN":
        for _ in range(170):
            x = rng.random() * 100; y = 11 + rng.gauss(0, 4)
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{0.3+rng.random()*1.1:.2f}" fill="{rng.choice(T)}" opacity="{0.35+0.6*rng.random():.2f}"/>')
    elif engine == "VOICE":
        for k in range(5):
            pts = " ".join(f"{x},{11+(2+k*1.1)*math.sin(x/100*math.tau*(1+k*.5)+k):.1f}" for x in range(0, 101, 2))
            o.append(f'<polyline points="{pts}" fill="none" stroke="#22995a" stroke-width=".7" opacity=".55"/>')
    elif engine == "PHYS":
        o.append('<line x1="4" y1="11" x2="96" y2="11" stroke="#e0a92a" stroke-width="1.4"/>')
        for k in range(1, 9):
            x = 4 + 92 * k / 9
            o.append(f'<line x1="{x:.1f}" y1="{11-9/k:.1f}" x2="{x:.1f}" y2="{11+9/k:.1f}" stroke="#e0a92a" stroke-width=".9" opacity=".8"/>')
    else:  # NOISE
        for _ in range(130):
            x = rng.random() * 100; y = rng.random() * 22
            o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="1.4" height="1.4" fill="#e2661d" opacity="{0.2+0.6*rng.random():.2f}"/>')
    o.append("</svg>")
    return "".join(o)
