#!/usr/bin/env python3
"""SLOOP, Gently. One canonical manuscript (book/content.html + the verified page compositions assembled by
book/build.py), restyled and re-composed for the approved Concept D system, in two editions:
  A4 (explicit art-directed pages) and iPad mini 7 (measured, repaginated into 128.5 × 195.6 mm page boxes).
Usage: python3 build_editions.py [a4|ipad|all]"""
import os, re, sys, subprocess, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "..", "book"); CON = os.path.join(HERE, "..", "concepts")
sys.path[:0] = [BOOK, CON]
import pages2; pages2.S_IPAD = 1.3     # iPad diagram lettering, before the manuscript is assembled
import build as B                      # the manuscript, assembled (cream system); we restyle below
import common as C                     # fm1 drawing helpers, textures
import weather as W
import art, illus

OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
P = lambda *a: os.path.join(HERE, *a)
NIGHT, CARD, LIME, INK, INK2, INK3 = "#0e0e10", "#19191c", "#d4ff3a", "#ede8dc", "#d4cfc3", "#b9b5aa"

# ------------------------------------------------------------------ palette: cream drawings → night
CMAP = {  # order matters: longer / more specific first
    "#1f1e1b": INK, "#4f4b44": INK2, "#8a857b": INK3, "#5a554d": INK2, "#5b5852": INK2, "#3d3933": INK2, "#4a4842": INK2,
    "#e6e2d8": "#232327", "#fbfaf7": CARD, "#e3dfd4": "#2c2c31", "#f2f0ea": NIGHT, "#f4f1ea": NIGHT, "#f2efe8": NIGHT, "#efece4": INK,
    "#6b4dff": LIME, "#dcd7f7": "#262a14", "#e9e5ff": "#1d2111", "#f3efe4": "#1f1f23", "#f7f5ef": "#1f1f23",
    "#bdb6a8": "#5a5750", "#c9c2b4": "#8c8880", "#d9d4c8": "#2f2f35", "#cfc8bb": "#2f2f35",
    "#9db8ee": "#22304a", "#dfe8fa": "#1b2a48", "#f8dccb": "#3a2616", "#6b4423": "#f3c9a8", "#fbeadd": "#3a2616",
    "#3d5a80": "#9fb7e6", "#8a8378": INK3, "#a8c4f2": "#9fb7e6", "#8e8e93": "#b8b8be", "#1c1a16": NIGHT, "#8e897f": INK3, "#a9a39a": INK3, "#c8c2b4": INK2,
}
STAR = '<svg class="gl" viewBox="0 0 12 12" aria-label="☆" style="width:.9em;height:.9em;vertical-align:-.08em"><path d="M6,.9 L7.5,4.4 L11.3,4.7 L8.4,7.2 L9.3,10.9 L6,8.9 L2.7,10.9 L3.6,7.2 L.7,4.7 L4.5,4.4Z" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/></svg>'
def darken(html):
    for a, b in CMAP.items(): html = html.replace(a, b).replace(a.upper(), b)
    # fonts: the dark system has two families; nothing falls back
    html = html.replace("font-family:'IBM Plex Mono'; font-size:.9em;", "font-weight:600; letter-spacing:.02em; font-size:.92em;").replace('font-family="Inter"', 'font-family="Albert Sans"')
    html = html.replace("font-family:'IBM Plex Mono';font-weight:500;font-size:7pt;", "font-weight:600;letter-spacing:.1em;text-transform:uppercase;font-size:7pt;")
    # glyphs the Latin subsets lack
    parts = re.split(r"(<svg\b.*?</svg>)", html, flags=re.S)
    for k, part in enumerate(parts):
        if not part.startswith("<svg"):
            parts[k] = part.replace("☆", STAR).replace("½", "<span style=\"white-space:nowrap\">1/2</span>")
    html = "".join(parts)
    # white text on what used to be ink chips becomes night; white key tops stay light but warm
    html = re.sub(r'(<text\b[^>]*?)fill="#fff"', r'\1fill="#0e0e10"', html)
    html = re.sub(r'(<text\b[^>]*?)fill="#f2f0ea"', r'\1fill="#0e0e10"', html)
    html = html.replace('fill="#fff"', 'fill="#e6e1d5"').replace('fill="#ffffff"', 'fill="#e6e1d5"')
    html = re.sub(r'rx="([0-9.]+)" fill="#1c1c1e"', r'rx="\1" fill="#3b3b44" stroke="#8c8880" stroke-width=".5"', html)
    # the filter arc: dark at the low-pass end, light at the high-pass end, on a dark page
    html = html.replace('<stop offset="0" stop-color="#ede8dc"/><stop offset=".5" stop-color="#5a5750"/><stop offset="1" stop-color="#1f1f23"/>',
                        '<stop offset="0" stop-color="#3a3a42"/><stop offset=".5" stop-color="#8c8880"/><stop offset="1" stop-color="#ede8dc"/>')
    # white keys in the chord drawings keep dark lettering (text sitting on a light key)
    html = re.sub(r'(<rect x="[0-9.]+" y="[0-9.]+" width="[0-9.]+" height="(?:54|60)" rx="[45]" fill="#e6e1d5"[^>]*/>\s*<text [^>]*?)fill="#aaa69c"', r'\1fill="#55524b"', html)
    html = re.sub(r'(<rect x="[0-9.]+" y="[0-9.]+" width="[0-9.]+" height="(?:54|60)" rx="[45]" fill="#e6e1d5"[^>]*/>\s*<text [^>]*>[^<]*</text>\s*<text [^>]*?)fill="#ede8dc"', r'\1fill="#1a1a1e"', html)
    html = re.sub(r'(<rect x="[0-9.]+" y="[0-9.]+" width="[0-9.]+" height="(?:54|60)" rx="[45]" fill="#e6e1d5"[^>]*/>\s*<text [^>]*>[^<]*</text>\s*<text [^>]*>[^<]*</text>\s*<text [^>]*?)fill="#aaa69c"', r'\1fill="#55524b"', html)
    return html

# ------------------------------------------------------------------ pieces in the night design language
def rain_word(word_a, word_b, rain_img, size=68, x2=50):
    return f"""<svg class="word" viewBox="0 0 210 104" preserveAspectRatio="xMidYMid slice">
  <defs><pattern id="rp" patternUnits="userSpaceOnUse" x="0" y="0" width="210" height="104"><image href="{rain_img}" x="0" y="-20" width="210" height="150" preserveAspectRatio="xMidYMid slice"/></pattern></defs>
  <g font-family="Big Shoulders" font-weight="900" font-size="{size}" letter-spacing="-.5">
    <text style="font-family:'Big Shoulders'" x="17" y="58" fill="url(#rp)">{word_a}</text><text style="font-family:'Big Shoulders'" x="17" y="58" fill="none" stroke="{INK}" stroke-width=".3" opacity=".65">{word_a}</text>
    <text style="font-family:'Big Shoulders'" x="{x2}" y="101" fill="url(#rp)">{word_b}</text><text style="font-family:'Big Shoulders'" x="{x2}" y="101" fill="none" stroke="{INK}" stroke-width=".3" opacity=".65">{word_b}</text>
  </g></svg>"""

def hero_glo(shot):
    hw = C.fm1(viewbox="78 246 844 508", highlight=("GLO",), screen_img=shot, glow=LIME, body="#2a2a2f", label_font="Albert Sans")
    over = f"""<svg viewBox="78 246 844 508" style="position:absolute;left:0;width:176mm;bottom:0;overflow:visible">
      <circle cx="828" cy="398" r="3.2" fill="{LIME}"/>
      <path d="M828,398 L828,372 L706,372" fill="none" stroke="{LIME}" stroke-width="1.4"/>
      <text x="700" y="376" font-family="Albert Sans" font-weight="600" font-size="12" fill="{LIME}" text-anchor="end">GLO<tspan font-weight="300" fill="{INK}" font-size="10.5"> · tap it until the TEXTURE page shows</tspan></text>
    </svg>"""
    return f'<div class="hero">{hw}{over}</div>'

# hardware coordinates (from the photo-traced drawing)
BTN = {"FX": (542, 398), "SEL": (595, 398), "ENV": (647, 398), "LFO": (699, 398), "EDIT": (752, 398), "GLO": (805, 398),
       "HOME": (542, 451), "SAVE": (595, 451), "ARP": (647, 451), "SEQ": (699, 451), "PLAY": (752, 451), "REC": (805, 451)}
KNOB = {"KNOB1": (553, 327), "KNOB2": (648, 327), "KNOB3": (742, 327), "KNOB4": (838, 327),
        "MASTER": (147, 326), "SELECT": (232, 326), "PRESETS": (147, 413), "ALGORITHM": (232, 413)}
OCT = {"OCT-": (135, 468), "OCT+": (197, 468)}

def hw_tagged(tags, viewbox, shot=None, label="On the FM-1", width=None):
    """A charcoal panel: the FM-1 crop with numbered lime tags beside the controls a lesson uses, and a key.
    tags: list of (control, text). Tags never cover the control; they sit outside it, with a short tick."""
    hw = C.fm1(viewbox=viewbox, highlight=tuple(t for t, _ in tags if t in BTN or t.startswith("KNOB")), screen_img=shot, glow=LIME, body="#2a2a2f", label_font="Albert Sans")
    hw = hw.replace('width="100%"', 'width="100%" style="display:block;border-radius:2mm"')
    vb = [float(v) for v in viewbox.split()]
    o = []
    for i, (ctl, _) in enumerate(tags, 1):
        if ctl in BTN:
            x, y = BTN[ctl]; cx, cy = x + 23, y + 22
            # the tag sits beside the button, never on a neighbour: left column → left, right column → right,
            # middle columns → above (top row) or below (bottom row)
            if x <= 542 and x - 14 - 11 >= vb[0] - 6: tx, ty, sx, sy = x - 14, cy, x, cy
            elif x >= 805: tx, ty, sx, sy = x + 46 + 14, cy, x + 46, cy
            elif y <= 398: tx, ty, sx, sy = cx, y - 14, cx, y
            else: tx, ty, sx, sy = cx, y + 44 + 14, cx, y + 44
            o.append(f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{LIME}" stroke-width="2"/>')
            o.append(f'<circle cx="{tx}" cy="{ty}" r="11" fill="{LIME}"/><text x="{tx}" y="{ty+4.5}" font-family="Albert Sans" font-weight="600" font-size="13" fill="{NIGHT}" text-anchor="middle">{i}</text>')
            o.append(f'<rect x="{x-6}" y="{y-6}" width="58" height="56" rx="12" fill="none" stroke="{LIME}" stroke-width="1.2" opacity=".7"/>')
        elif ctl in KNOB:
            x, y = KNOB[ctl]
            o.append(f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{LIME}" stroke-width="2.5"/>')
            o.append(f'<line x1="{x+18}" y1="{y-18}" x2="{x+22}" y2="{y-22}" stroke="{LIME}" stroke-width="2"/>')
            o.append(f'<circle cx="{x+30}" cy="{y-30}" r="11" fill="{LIME}"/><text x="{x+30}" y="{y-25.5}" font-family="Albert Sans" font-weight="600" font-size="13" fill="{NIGHT}" text-anchor="middle">{i}</text>')
        elif ctl in OCT:
            x, y = OCT[ctl]
            o.append(f'<rect x="{x-5}" y="{y-5}" width="66" height="41" rx="8" fill="none" stroke="{LIME}" stroke-width="1.6"/>')
            o.append(f'<line x1="{x+28}" y1="{y-5}" x2="{x+28}" y2="{y-16}" stroke="{LIME}" stroke-width="2"/>')
            o.append(f'<circle cx="{x+28}" cy="{y-27}" r="11" fill="{LIME}"/><text x="{x+28}" y="{y-22.5}" font-family="Albert Sans" font-weight="600" font-size="13" fill="{NIGHT}" text-anchor="middle">{i}</text>')
    over = f'<svg viewBox="{viewbox}" style="position:absolute;inset:0;width:100%;height:100%;overflow:visible">{"".join(o)}</svg>'
    key = "".join(f'<div><span class="t">{i}</span><span>{t}</span></div>' for i, (_, t) in enumerate(tags, 1))
    style = f' style="width:{width}"' if width else ""
    return f'<div class="hwpanel"{style}><div class="lab">{label}</div><div style="position:relative">{hw}{over}</div><div class="key">{key}</div></div>'

def screen_callouts(shot):
    return f"""<div class="knoblabels" style="display:grid;grid-template-columns:repeat(4,1fr);text-align:center;font-size:.86em;line-height:1.3;color:var(--ink-2);margin-bottom:1mm">
      <div><b>KNOB1</b><br>SRC</div><div><b>KNOB2</b><br>LEVEL</div><div><b>KNOB3</b><br>TONE</div><div><b>KNOB4</b><br>MOVE</div></div>
    <div style="position:relative;padding-top:9mm">
      <img src="{shot}" alt="The TEXTURE page, VINYL source" style="width:100%;display:block;border-radius:2mm;box-shadow:0 0 0 .4mm #232327;image-rendering:pixelated">
      <svg viewBox="0 0 500 80" style="display:block;width:100%;position:absolute;left:0;top:0;overflow:visible">
        <g stroke="{LIME}" stroke-width="3" fill="{LIME}">
          <line x1="70" y1="0" x2="70" y2="150"/><line x1="190" y1="0" x2="190" y2="150"/><line x1="310" y1="0" x2="310" y2="150"/><line x1="430" y1="0" x2="430" y2="150"/>
          <circle cx="70" cy="150" r="7"/><circle cx="190" cy="150" r="7"/><circle cx="310" cy="150" r="7"/><circle cx="430" cy="150" r="7"/>
        </g></svg></div>"""

def weather_icons():
    import concept_d2 as D2
    return D2.weather_icons().replace('class="weathers"', 'class="weathers" style="display:grid;grid-template-columns:repeat(6,1fr);column-gap:3mm"')

WEATHER_CSS = """
.weathers .t{font-weight:600;font-size:.88em;letter-spacing:.04em;margin-top:1.4mm;color:var(--ink);} .weathers .d{font-size:.8em;color:var(--ink-2);line-height:1.3;}
.weathers svg{display:block;width:100%;background:var(--card);border-radius:1.4mm;} .weathers .on svg{box-shadow:inset 0 0 0 .45mm var(--signal);}
.knoblabels b{color:var(--ink);}
"""

# ------------------------------------------------------------------ the Weather lesson, as approved (word page + reading page)
def weather_pages():
    raw = B.split_sections(B.raw)
    l4 = [s for s in raw if 'id="l4"' in s][0]
    shot = C.img_uri("texture-page.png")
    rain = C.texture_image("rain", 1400, 1000, seed=7, tint=(52, 60, 80), fg=(242, 238, 226))
    steps = re.search(r'<ol class="steps">.*?</ol>', l4, flags=re.S).group(0)
    hear = re.search(r'<div class="hear">.*?</div></div>', l4, flags=re.S).group(0)
    tryb = re.search(r'<div class="try">.*?</p></div>', l4, flags=re.S).group(0)
    mess = re.search(r'<div class="mess">.*?</p></div>', l4, flags=re.S).group(0)
    cap = re.search(r'<figcaption>(.*?)</figcaption>', l4, flags=re.S).group(1)
    k = W.KICKER
    tags = [("GLO", "<b>GLO</b>, tapped repeatedly until the TEXTURE page shows (step 1)"), ("FX", "<b>FX</b>, held (step 4)"), ("KNOB2", "<b>KNOB2</b>, turned while FX is held: DUST (step 4)")]
    word = (f'<section class="page wordpage trk0" id="l4" data-part="Part 1 · Atmosphere">\n{rain_word("WEA", "THER", rain)}'
            f'<div class="kick kicker" style="margin:0;color:var(--signal)"><span class="chno" style="font-size:1.4em;color:var(--signal)">{k[0]}</span><span>{k[1]} · {k[2]}</span></div>'
            f'<div class="title">{W.TITLE_B}</div><p class="lead">{W.LEAD}</p>'
            f'<div class="start"><div class="label">{W.START_LABEL}</div><ul><li>{W.START[0]}</li></ul></div>'
            f'{hero_glo(shot)}\n</section>\n')
    a4_read = (f'<h2 style="margin:0 0 .9em;font-size:1.15em;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--ink-3)">Weather · the TEXTURE page</h2>'
            f'<div class="row" style="grid-template-columns:4fr 2fr;gap:6mm"><div style="font-size:1.08em">{steps}'
            f'<div class="label" style="margin:3mm 0 2mm">The six weathers, as step 2 lists them</div>{weather_icons()}{hear}</div>'
            f'<div>{screen_callouts(shot)}<p class="note" style="margin-top:2.5mm;font-size:.88em">{cap}</p>{hw_tagged(tags, "526 280 354 228", shot)}</div></div>'
            f'<div class="row c-1-1" style="margin-top:2mm">{tryb}{mess}</div>')
    ihead = '<div class="ihead"><span>Weather · the TEXTURE page</span><span>GLO · 7 of 8</span></div>'
    ipad_read = (f'<div class="iscreen">{ihead}{steps}</div>'
                 f'<div class="iscreen">{ihead}<div class="label" style="margin:0 0 3mm">The six weathers, as step 2 lists them</div><div class="weathers-big">{weather_icons()}</div></div>'
                 f'<div class="iscreen">{ihead}<div style="width:66%;margin:0 auto 2mm">{screen_callouts(shot)}</div><p class="note" style="margin:0 0 5mm;font-size:.92em">{cap}</p>{hear}</div>'
                 f'<div class="iscreen">{ihead}{hw_tagged(tags, "526 280 354 228", shot)}{tryb}{mess}</div>')
    read = (f'<section class="page r2 trk0" data-part="Part 1 · Atmosphere" data-head="GLO · page 7 of 8">\n'
            f'<div class="a4-only">{a4_read}</div><div class="ipad-only ipad-weather">{ipad_read}</div>\n</section>\n')
    return word, read

# ------------------------------------------------------------------ cover and part openers
def cover():
    f = art.field(210, 150, 7, 5400)
    return ('<section class="page cover" id="cover">\n'
            f'<svg class="field" {f[4:f.index(">")]}>{f.split(">",1)[1]}'
            '<div class="title">SLOOP,<br>GENTLY</div>'
            '<div class="sub">Atmospheres first, drums later.<br>A slow, friendly tour of the M&#8209;VAVE FM&#8209;1<br>running the SLOOP groovebox firmware.</div>'
            '<div class="meta">A beginner\'s handbook · written for SLOOP <b>2.8.4</b> · beta firmware · November 2026</div>\n</section>\n')

# ------------------------------------------------------------------ assemble
def order_dark():
    order = []
    word, read = weather_pages()
    for s in B.order:
        if s == "CONTENTS": order.append(s); continue
        if 'class="page cover"' in s[:60]: order.append(cover()); continue
        if 'id="l4"' in s[:300]:
            order.append(word); order.append(read); continue
        order.append(s)
    return order


# ------------------------------------------------------------------ L10: what is saved where (redrawn; sections are tonal, never track colours)
def saved_where(S=1.0):
    W, H = 352, 118
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    T = lambda x, y, t, sz=5.6, w=400, fill=INK2, anchor="middle", extra="": f'<text x="{x}" y="{y}" font-size="{sz*S:.1f}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>'
    # backup envelope
    o.append(f'<rect x="1" y="1" width="{W-2}" height="92" rx="5" fill="none" stroke="{LIME}" stroke-width=".9" stroke-dasharray="3 2.4"/>')
    o.append(T(6, 106, "WEB-EDITOR BACKUP: one file holds all of this, plus your user presets, samples, kits and settings (favourites are not included)", 5.6, 600, LIME, "start"))
    # working loop
    o.append(f'<rect x="12" y="18" width="98" height="52" rx="4" fill="{CARD}" stroke="{INK3}" stroke-width=".6"/>')
    o.append(T(61, 36, "WORKING LOOP", 7.6, 600, INK)); o.append(T(61, 47, "what you hear in loop mode", 5.6)); o.append(T(61, 56, "kept by autosave", 5.6))
    # sections
    cols = ["#e6e1d5", "#a8a49a", "#6e6a62", "#43434a"]; fg = ["#1a1a1e", "#1a1a1e", "#f2efe8", "#f2efe8"]
    for i, (n, c) in enumerate(zip("ABCD", cols)):
        x = 160 + (i % 2) * 30; y = 20 + (i // 2) * 26
        o.append(f'<rect x="{x}" y="{y}" width="26" height="20" rx="3" fill="{c}"/>')
        o.append(T(x + 13, y + 14, n, 8.6, 700, fg[i]))
    o.append(T(188, 80, "four saved sections", 5.6))
    # arrows loop ↔ sections
    o.append(f'<path d="M112,38 L154,38" stroke="{INK3}" stroke-width=".9"/><path d="M150,35 L155,38 L150,41" fill="none" stroke="{INK3}" stroke-width=".9"/>')
    o.append(f'<path d="M154,52 L112,52" stroke="{INK3}" stroke-width=".9"/><path d="M116,49 L111,52 L116,55" fill="none" stroke="{INK3}" stroke-width=".9"/>')
    o.append(T(133, 27, "SAVE + key 5–8", 5, 600, INK)); o.append(T(133, 33.5, "save into a section", 4.8, 400, INK2))
    o.append(T(133, 61, "SAVE + key 1–4", 5, 600, INK)); o.append(T(133, 68, "load a section", 4.8, 400, INK2))
    # song
    o.append(f'<rect x="250" y="18" width="90" height="52" rx="4" fill="{CARD}" stroke="{INK3}" stroke-width=".6"/>')
    o.append(T(295, 36, "SONG", 7.6, 600, INK)); o.append(T(295, 47, "A–D in order,", 5.6)); o.append(T(295, 56, "up to 16 steps", 5.6))
    o.append(f'<path d="M222,44 L246,44" stroke="{INK3}" stroke-width=".9"/><path d="M242,41 L247,44 L242,47" fill="none" stroke="{INK3}" stroke-width=".9"/>')
    o.append("</svg>")
    return "".join(o)

def fill_strip_dark(S=1.0):
    """L9: four bars as two rows; the F (fill-only) step on page 1, dashed last steps of pages 2-4, the held fill across a round."""
    from illus import wrap
    W = 352; o = []
    bw = 170; g = 12; T4 = "#e2661d"; sw = (bw - 6) / 16
    for b in range(4):
        x = (b % 2) * (bw + g); y0 = 10 + (b // 2) * 50
        o.append(f'<rect x="{x}" y="{y0+12}" width="{bw}" height="30" rx="5" fill="{T4}" opacity="{.9 if b%2==0 else .72}"/>')
        o.append(f'<text x="{x+2}" y="{y0+7}" font-size="{6.4*S:.1f}" font-weight="600" fill="{INK}">bar {b+1}</text>')
        o.append(f'<text x="{x+bw}" y="{y0+7}" font-size="{5.8*S:.1f}" fill="{INK3}" text-anchor="end">page {b+1}</text>')
        for i in range(16):
            sx = x + 3 + i * sw; last = i == 15
            if b == 0 and last:
                o.append(f'<rect x="{sx+.6:.1f}" y="{y0+15}" width="{sw-1.6:.1f}" height="24" rx="2" fill="{LIME}"/>')
                o.append(f'<text x="{sx+sw/2:.1f}" y="{y0+31}" font-size="{8*S:.1f}" font-weight="700" fill="{NIGHT}" text-anchor="middle">F</text>')
            elif last:
                o.append(f'<rect x="{sx+.6:.1f}" y="{y0+15}" width="{sw-1.6:.1f}" height="24" rx="2" fill="none" stroke="{LIME}" stroke-width="1" stroke-dasharray="2 1.4"/>')
            else:
                o.append(f'<rect x="{sx+.8:.1f}" y="{y0+21}" width="{sw-2:.1f}" height="12" rx="1.5" fill="#0e0e10" opacity="{.5 if i%2==0 else .2}"/>')
    # the held fill spans the whole round: a bar under both rows
    o.append(f'<rect x="0" y="115" width="{W}" height="14" rx="7" fill="{LIME}"/>')
    o.append(f'<text x="{W/2:.1f}" y="124.5" font-size="{min(6.2*S, 9.6):.1f}" font-weight="600" fill="{NIGHT}" text-anchor="middle">GLO + key 9, held through one full round (all four bars)</text>')
    y = 144
    for ln in wrap("F = a FILL ONLY step: the crash on step 16 of bar 1 plays only while a fill is on, so it rings once per round, when the playhead crosses it with key 9 held. The condition belongs to the whole step, every sound in it, which is why the crash sits on an empty step.", int(118/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.2*S:.1f}" fill="{INK2}">{ln}</text>'); y += 7.6 * S
    for ln in wrap("dashed: the last step of pages 2, 3 and 4, where the same mark makes a crash greet every fill bar (GLO + key 10).", int(118/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.2*S:.1f}" fill="{INK3}">{ln}</text>'); y += 7.6 * S
    return f'<svg viewBox="0 0 {W} {int(y-1)}" width="100%">' + "".join(o) + "</svg>"

def ID_fill():
    import ipad_draw; return ipad_draw.fill_strip()

def fix_pages(order):
    """page-level adjustments for the dark system (measures, densities, merges); the text is untouched"""
    out = []
    for s in order:
        if s == "CONTENTS": out.append(s); continue
        head = s[:400]
        def dense(x): return x.replace('class="page', 'class="page dense', 1) if 'dense' not in x[:120] else x
        if 'id="ch1"' in head: s = dense(s).replace('<figure style="margin:3mm 0 1mm;">', '<figure style="margin:2mm auto 1mm;width:150mm;">', 1)
        if 'If things go wrong: the complete recovery kit' in s:
            s = dense(s)
            s = re.sub(r'<figure style="margin:1mm auto 2mm;width:126mm;">.*?</figure>\s*', '', s, count=1, flags=re.S)   # the map restated the four headed paragraphs below it
        if 'Tap, hold, and the seven layers' in s: s = dense(s)
        if 'Let the sound hold itself' in s: s = dense(s)
        if 'id="l2"' in head: s = s.replace('width:142mm', 'width:134mm')
        if 'id="l5"' in head: s = dense(s).replace('margin:0 0 2mm;width:162mm;', 'margin:0 0 2mm;width:148mm;')
        if 'A pattern to copy' in s: s = s.replace('width:148mm', 'width:130mm').replace('width:150mm', 'width:138mm')
        if 'id="l8"' in head: s = dense(s).replace('margin:2mm auto 3mm;width:150mm;', 'margin:2mm auto 3mm;width:132mm;')
        if 'The knobs while FX is held' in s and 'Fills: a one' in s:
            s = dense(s)
            s = re.sub(r'<figure style="margin:3mm 0 2mm;">.*?</figure>', '', s, count=1, flags=re.S)
            fig = '<figure style="margin:5mm 0 2mm;"><div class="a4-only">' + fill_strip_dark(1.9) + '</div><div class="ipad-only">' + ID_fill() + '</div></figure>'
            s = s.replace('</div><div><h2 style="margin-top:0;">Fills', fig + '</div><div><h2 style="margin-top:0;">Fills', 1)
        if 'id="l10"' in head: s = dense(s).replace('<figure style="margin:0 0 3mm;">', '<figure style="margin:0 auto 3mm;width:128mm;">')
        if 'id="links"' in head: s = dense(s)
        if 'Lesson nine · continued' in head or 'Lesson seven · continued' in head or 'Lesson eight · continued' in head:
            s = re.sub(r' id="l[0-9]+"', '', s, count=1)
            s = s.replace('<section class="page', '<section class="page cont', 1)
        if 'Chapter fourteen · continued' in head:
            s = s.replace(' id="ch14"', '', 1)
            panel = hw_tagged([("HOME", "<b>HOME</b>, held: the settings menu, where AUDIO · USB AUDIO is set to FULL (step 1)"),
                               ("PLAY", "<b>PLAY</b>, pressed once GarageBand's track is armed and recording (step 4)")],
                              "520 262 406 258", label="On the FM-1, for this page")
            s = s.replace("</section>", f'<div class="row c-1-1" style="margin-top:4mm;align-items:start"><div style="max-width:84mm">{panel}</div><div></div></div>\n</section>')
        if 'id="ch3"' in head and 'hw-ipad' in s:
            m = re.search(r'<div class="hw-ipad ipad-only"><div class="hw-rot">(<svg viewBox="70 236 860 618".*?</svg>)</div></div>', s, flags=re.S)
            hw = m.group(1)
            REF = 520.0      # every enlargement shares one scale (520 drawing units = the full column width plus the bleed)
            NUM = {}
            def enlarge_labels(sv):
                # on the enlargements the smallest printed labels go up a step, and the screen note sets in three lines
                sv = re.sub(r'font-size="(?:9\.5|10\.5)" font-weight="500" fill="#(8e8e93|b8b8be)"', r'font-size="13.5" font-weight="500" fill="#\1"', sv)   # stock OP legends
                sv = sv.replace('font-size="11.5" font-weight="700" fill="#a8c4f2"', 'font-size="12.5" font-weight="700" fill="#a8c4f2"')     # black-key names
                sv = sv.replace('font-size="12" font-weight="700" fill="#e8e8e8"', 'font-size="12.5" font-weight="700" fill="#e8e8e8"')     # button labels
                sv = sv.replace('font-size="11" font-weight="700" fill="#e8e8e8"', 'font-size="11.5" font-weight="700" fill="#e8e8e8"')     # PLAY / STOP
                sv = re.sub(r'font-size="(?:11|12)" fill="#(8a8378|b9b5aa)"', r'font-size="13" fill="#\1"', sv)                                 # note names
                sv = re.sub(r'<text x="396" y="386"[^>]*>SLOOP draws its pages here;</text>\s*<text x="396" y="398"[^>]*>the four dials match KNOB1\u20134</text>',
                            '<g font-family="Albert Sans" font-size="12.5" fill="#a8c4f2" text-anchor="middle">'
                            '<text x="396" y="385">SLOOP draws its</text><text x="396" y="398.5">pages here; the four</text>'
                            '<text x="396" y="412">dials match KNOB1\u20134</text></g>', sv)
                return sv
            def crop(n, vb, cap, brk=False):
                w = float(vb.split()[2])
                sv = re.sub(r'viewBox="[^"]+"', f'viewBox="{vb}"', hw, 1).replace('style="margin:1mm 0 0;"', '')
                sv = enlarge_labels(sv)
                sv = re.sub(r'<rect x="(?:86|318|642)" y="817"[^>]*/>|<text x="[0-9.]+" y="832"[^>]*>.*?</text>', '', sv, flags=re.S)   # the drawing's own legend row (shown in HTML above)
                return (f'<figure class="hwcrop enl{" brk" if brk else ""}" style="--w:{100*w/REF:.1f}%">{sv}'
                        f'<figcaption><span class="leg">{n}</span>{cap}</figcaption></figure>')
            # the overview: the drawing without its lettering (too small to read on this screen), the four enlarged areas outlined and numbered
            regions = [(1, 76, 244, 436, 268, 104, 272), (2, 512, 244, 412, 268, 540, 272),
                       (3, 76, 514, 380.3, 290, 100, 778), (4, 450, 514, 474, 290, 474, 778)]
            ov = re.sub(r'<text\b[^>]*>.*?</text>', '', hw, flags=re.S)
            ov = re.sub(r'viewBox="[^"]+"', 'viewBox="70 236 860 568"', ov, 1).replace('style="margin:1mm 0 0;"', '')
            marks = ''.join(f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="12" fill="none" stroke="#d4ff3a" stroke-width="2.6"/>'
                            f'<circle cx="{tx}" cy="{ty}" r="18" fill="#d4ff3a"/><text x="{tx}" y="{ty+7.5}" font-family="Albert Sans" font-weight="700" font-size="22" fill="#0e0e10" text-anchor="middle">{n}</text>'
                            for n, x, y, w, h, tx, ty in regions)
            ov = ov.replace('</svg>', marks + '</svg>')
            legend = ('<div class="hwlegend"><span><kbd>FX</kbd> printed on the FM&#8209;1</span>'
                      '<span><kbd style="color:#9fb7e6">F#3</kbd> SLOOP names and key numbers, in blue</span>'
                      '<span><kbd style="color:#b8b8be;font-weight:500">OP1</kbd> stock legends, unused by SLOOP</span></div>')
            # every crop falls in a real gap: the top panel splits between the screen (ends x 496) and the button block (starts x 528);
            # the keyboard splits in the E-F gap (key 7 ends x 449.4, key 8 starts x 456.8), so no key or label is cut
            maps = ('<div class="ipad-only hw-maps">'
                    + f'<figure class="hwcrop overview">{ov}<figcaption>The whole panel, traced from a photograph. The four numbered areas are enlarged on the next pages, all at the same scale, with every label.</figcaption></figure>'
                    + legend
                    + crop(1, "76 244 436 268", "Top panel, left: MASTER, SELECT, PRESETS, ALGORITHM, OCT\u2212, OCT+ and the screen")
                    + crop(2, "512 244 412 268", "Top panel, right: KNOB1\u20134 and the twelve function buttons")
                    + crop(3, "76 514 380.3 290", "Keys 1\u20137, F3 to E4, with their black keys", brk=True)
                    + crop(4, "450 514 474 290", "Keys 8\u201316, F4 to G5, with their black keys")
                    + '</div>')
            s = s.replace(m.group(0), "")
            k = s.index('</p>', s.index('Traced from a photograph')) + 4
            s = s[:k] + maps + s[k:]
            s = s.replace('<section class="page', '<section class="page hwfirst', 1)
        if 'What is actually saved where' in s:
            s = re.sub(r'<svg viewBox="0 0 176 46" width="100%" style="margin:1mm 0 2mm;">.*?</svg>', lambda m: '<figure style="margin:1mm auto 2mm;width:150mm">' + saved_where() + '</figure>', s, flags=re.S)
        # L9 third page: the controls this lesson uses, drawn on the FM-1
        if 'Everything a punch-in does, and nothing it keeps' in s:
            panel = hw_tagged([("FX", "<b>FX</b>, held: the keys become 27 punch-in effects; KNOB1–4 become FILTER, DUST, DUCK and the track filter"),
                               ("GLO", "<b>GLO</b>, held: key 9 fills for as long as you hold it, key 10 for the whole next bar"),
                               ("SEQ", "<b>SEQ</b>, held: the step grid, where a step's FILL condition is set with OCT−/OCT+")],
                              "520 262 406 258", label="The controls this lesson lives on")
            s = s.replace("</section>", f'<div style="max-width:100mm;margin-top:2mm">{panel}</div>\n</section>')
        out.append(s)
    for i, s2 in enumerate(out):
        if 'Sharing track 2: a step holds four notes' in s2:
            s2 = s2.replace('<h2 style="margin-top:0;">Sharing track 2: a step holds four notes</h2>', '')
            s2 = s2.replace('margin:1mm auto 1.5mm;width:136mm;', 'margin:0 auto 2mm;width:126mm;')
            # the try-this card moves into the right column, under the GarageBand translation, so the figure can breathe
            m2 = re.search(r'<div class="mess">.*?</p></div>', s2, flags=re.S); tr = m2.group(0); s2 = s2.replace(tr, '')
            gb_end = s2.index('</div>', s2.index('<div class="gb">', s2.index('Mixing: the GLO layer'))) 
            # close of the gb's inner <p></div>: find the gb block end (two closing divs after label)
            k = s2.index('<div class="gb">', s2.index('Mixing: the GLO layer')); depth = 0; i2 = k
            while True:
                mm = re.compile(r'<div\b|</div>').search(s2, i2)
                depth += 1 if mm.group(0) != '</div>' else -1; i2 = mm.end()
                if depth == 0: break
            s2 = s2[:i2] + tr.replace('<div class="mess">', '<div class="mess" style="margin-top:3mm">') + s2[i2:]
            s2 = s2.replace('<figure class="shot"', '<figure class="shot" style="max-width:44mm;margin:0 auto .6em"', 1)
            out[i] = s2
    return out

ORDER = fix_pages(order_dark())

def pages_by_id_a4():
    d = {}
    for n, s in enumerate(ORDER, 1):
        m = re.search(r'id="([a-z0-9]+)"', (s if s != "CONTENTS" else '')[:200])
        if m: d[m.group(1)] = n
    return d

def css(edition):
    base = open(P("theme.css"), encoding="utf-8").read() + WEATHER_CSS + "\n" + open(P(f"{edition}-theme.css"), encoding="utf-8").read()
    return B.inline_fonts(base)

def assemble_a4(pages_by_id):
    out = []; cur = {"trk": "trk0", "lbl": "SLOOP, Gently", "glob": ""}
    for n, s in enumerate(ORDER, 1):
        if s == "CONTENTS": s = B.contents(pages_by_id)
        out.append(B.chrome(s, n, cur))
    body = B.SYMBOLS + "\n".join(out)
    body = darken(body)
    html = ('<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>SLOOP, Gently · A4 edition (SLOOP 2.8.4)</title>'
            f'<style>{css("a4")}</style></head><body class="ed-a4">\n{body}\n</body></html>')
    html = B.inline_imgs(html)
    html = B.resolve_xrefs(html, pages_by_id)
    return B.glyph_pass(html)


# ------------------------------------------------------------------ iPad redraws of the three wide drum-lesson drawings
T4 = "#e2661d"
def pattern_hero_ipad(S=1.4):
    """the 16-step pattern as two rows of two beats, lettering sized for the small screen"""
    from illus import wrap
    W = 352; o = []
    cw = 20; gw = 10; L = 54
    lanes = [("Hat", 5, {1, 3, 5, 7, 9, 11, 13, 15}, {3, 7, 11, 15}), ("Snare", 3, {5, 13}, set()), ("Kick", 1, {1, 11}, set())]
    counts = ["", "e", "&amp;", "a"]
    def row(beats, y0):
        xs = {}
        for bi, b in enumerate(beats):
            for k in range(4):
                i = (b - 1) * 4 + k + 1
                xs[i] = L + bi * (4 * cw + gw) + k * cw
            o.append(f'<text x="{xs[(b-1)*4+1]}" y="{y0+22}" font-family="Big Shoulders" font-weight="900" font-size="{22*S:.0f}" fill="{INK}">{b}</text>')
        for li, (name, key, hits, ghosts) in enumerate(lanes):
            y = y0 + 32 + li * 36
            o.append(f'<text x="0" y="{y+13}" font-size="{8.6*S:.1f}" font-weight="600" fill="{INK}">{name}</text>')
            o.append(f'<text x="0" y="{y+24}" font-size="{6*S:.1f}" fill="{INK3}">key {key}</text>')
            for i, x in xs.items():
                if i in hits and i in ghosts:
                    o.append(f'<rect x="{x+1:.1f}" y="{y+1}" width="{cw-4:.1f}" height="26" rx="4" fill="#3a2616" stroke="{T4}" stroke-width="1.2"/>')
                elif i in hits:
                    o.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-2:.1f}" height="28" rx="4.5" fill="{T4}"/>')
                else:
                    o.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-2:.1f}" height="28" rx="4.5" fill="#2c2c31"/>')
        yc = y0 + 32 + 3 * 36 + 8
        for i, x in xs.items():
            c = str((i - 1) // 4 + 1) if (i - 1) % 4 == 0 else counts[(i - 1) % 4]
            o.append(f'<text x="{x+cw/2-1:.1f}" y="{yc}" font-size="{7*S:.1f}" fill="{INK if (i-1)%4==0 else INK3}" text-anchor="middle">{c}</text>')
        return xs, yc
    xs1, yc1 = row((1, 2), 0)
    xs2, yc2 = row((3, 4), yc1 + 14)
    # the two notes become a legend, so nothing sits on the grid
    x11 = xs2[11] + cw / 2 - 1; yk = yc1 + 14 + 32 + 2 * 36
    o.append(f'<circle cx="{x11:.1f}" cy="{yk-3}" r="1.8" fill="{INK}"/>')
    y = yc2 + 16
    o.append(f'<rect x="1" y="{y-7}" width="{cw-4}" height="9" rx="2.5" fill="#3a2616" stroke="{T4}" stroke-width="1"/>')
    o.append(f'<text x="{cw+2}" y="{y:.1f}" font-size="{6.6*S:.1f}" fill="{INK2}">outlined = ghost: hold <tspan font-weight="600" fill="{INK}">OCT−</tspan> as you play it</text>'); y += 10 * S
    o.append(f'<circle cx="{cw/2-1}" cy="{y-3}" r="1.8" fill="{INK}"/>')
    o.append(f'<text x="{cw+2}" y="{y:.1f}" font-size="{6.6*S:.1f}" fill="{INK2}"><tspan font-weight="600" fill="{INK}">the one surprise:</tspan> a kick on the "&amp;" after 3 (the marked step)</text>'); y += 10 * S
    for ln in wrap('count aloud: the numbers are the beats, the hats fall on every number and every "&amp;". One bar of 16 steps, which the loop repeats; Lesson 8 stretches the same idea to LENGTH 64, four bars in a row.', int(96/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.4*S:.1f}" fill="{INK3}">{ln}</text>'); y += 8 * S
    return f'<svg viewBox="0 0 {W} {int(y)}" width="100%">' + "".join(o) + "</svg>"

def counted_take_ipad(S=1.4):
    """REC arms · PLAY starts the count-in · recording begins by itself · four bars · REC ends it, as a vertical timeline"""
    W = 352; o = []
    rows = [("REC", "arm: set the dials", INK, True), ("PLAY", "the count-in starts", INK, True),
            ("4 · 3 · 2 · 1", "one bar of clicks, not recorded", None, False),
            ("bars 1–4", "recording begins by itself; the pattern above, four times, counting 1 2 3 4 with the click", T4, False),
            ("REC", "finish; the loop plays on", INK, True)]
    y = 4
    for lab, txt, col, key in rows:
        if col is None:
            o.append(f'<rect x="0" y="{y}" width="78" height="20" rx="4" fill="none" stroke="{INK3}" stroke-width="1" stroke-dasharray="3 2.4"/>')
            o.append(f'<text x="39" y="{y+14}" font-size="{8*S:.1f}" font-weight="600" fill="{INK3}" text-anchor="middle">{lab}</text>')
        elif key:
            o.append(f'<rect x="0" y="{y}" width="78" height="20" rx="4" fill="#2a2a30" stroke="#5a5750" stroke-width=".8"/>')
            o.append(f'<text x="39" y="{y+13.5}" font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">{lab}</text>')
        else:
            o.append(f'<rect x="0" y="{y}" width="78" height="20" rx="4" fill="{T4}"/>')
            o.append(f'<text x="39" y="{y+13.5}" font-size="{7.6*S:.1f}" font-weight="600" fill="#fff" text-anchor="middle">{lab}</text>')
        from illus import wrap
        ty = y + 9
        for ln in wrap(txt, int(66/S)):
            o.append(f'<text x="88" y="{ty:.1f}" font-size="{6.8*S:.1f}" fill="{INK2}">{ln}</text>'); ty += 8.4 * S
        step = max(30, ty - y + 4)
        if lab != "REC" or y < 10:
            o.append(f'<line x1="39" y1="{y+20}" x2="39" y2="{y+step}" stroke="{INK3}" stroke-width=".8"/>')
        y += step
    o.append(f'<text x="0" y="{y+6}" font-size="{6.4*S:.1f}" fill="{INK3}">Changed your mind during the count-in? REC cancels it.</text>')
    return f'<svg viewBox="0 0 {W} {int(y+12)}" width="100%">' + "".join(o) + "</svg>"

def drum_dynamics_ipad(S=1.3):
    from illus import wrap, pill
    W = 352; o = []
    o.append(f'<text x="0" y="12" font-size="{9*S:.1f}" font-weight="600" fill="{INK}">Three weights from two buttons</text>')
    hits = [("OCT− held", "ghost", 18, .32, True), ("plain tap", "normal", 32, .78, False), ("OCT+ held", "hard", 46, 1.0, False)]
    base = 74
    for i, (how, name, h, op, outline) in enumerate(hits):
        x = 10 + i * 60
        o.append(f'<rect x="{x}" y="{base-h}" width="30" height="{h}" rx="5" fill="{T4}" opacity="{op}"/>')
        if outline: o.append(f'<rect x="{x+.6}" y="{base-h+.6}" width="28.8" height="{h-1.2}" rx="4.5" fill="none" stroke="{T4}" stroke-width="1.2"/>')
        o.append(f'<text x="{x+15}" y="{base+13}" font-size="{7.6*S:.1f}" font-weight="600" fill="{INK}" text-anchor="middle">{name}</text>')
        o.append(f'<text x="{x+15}" y="{base+23}" font-size="{6*S:.1f}" fill="{INK3}" text-anchor="middle">{how}</text>')
    y = base + 36
    for ln in wrap("The keys cannot feel how hard you press: these two buttons are your touch, and they record exactly as played.", int(96/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 8.2 * S
    y += 10
    o.append(f'<text x="0" y="{y}" font-size="{9*S:.1f}" font-weight="600" fill="{INK}">One pattern, thirty-seven kits</text>'); y += 8
    kits = ["AMBIENT", "LO-FI", "JAZZ", "BOOMBAP", "DUST"]; kx = 0
    for k, kit in enumerate(kits):
        w = pill(o, kx, y, kit, fill=(INK if k == 1 else "#2a2a30"), fg=(NIGHT if k == 1 else INK), S=S); kx += w + 4
    y += 9.5 * S + 6
    o.append(f'<text x="0" y="{y}" font-size="{6*S:.1f}" fill="{INK3}">PRESETS on track 4 walks the kits</text>'); y += 8
    lanes = [("hat", [0, 2, 4, 6, 8, 10, 12, 14], .55), ("snare", [4, 12], .85), ("kick", [0, 10], 1.0)]
    sw = (W - 40) / 16
    for li, (name, steps, op) in enumerate(lanes):
        y0 = y + li * 14
        o.append(f'<text x="0" y="{y0+9}" font-size="{6*S:.1f}" fill="{INK3}">{name}</text>')
        for st in range(16):
            on = st in steps
            o.append(f'<rect x="{40+st*sw+.8:.1f}" y="{y0}" width="{sw-1.6:.1f}" height="11" rx="2.5" fill="{T4 if on else "#2c2c31"}" opacity="{op if on else 1}"/>')
    y += 3 * 14 + 10
    for ln in wrap("Changing kit never changes a recorded pattern; the sequencer keeps the hits, the kit supplies the sounds, so you can swap kits under a beat forever.", int(96/S)):
        o.append(f'<text x="0" y="{y:.1f}" font-size="{6.6*S:.1f}" fill="{INK2}">{ln}</text>'); y += 8.2 * S
    return f'<svg viewBox="0 0 {W} {int(y)}" width="100%">' + "".join(o) + "</svg>"

def ipad_redraws(html):
    """swap the ipad-only siblings of the wide drawings for tall redraws; wrap raw strips into a4/ipad pairs"""
    import interior, illus, ipad_draw as ID
    def swap(html, a4_svg, new_svg):
        a4_dark = darken(a4_svg)
        i = html.find(a4_dark)
        if i < 0: return html, False
        # the ipad sibling follows: <div class="ipad-only">…</div>
        j = html.find('<div class="ipad-only">', i); k = html.find('</div>', j)
        return html[:j] + '<div class="ipad-only">' + new_svg + html[k:], True
    html, ok1 = swap(html, interior.pattern_hero(), pattern_hero_ipad())
    html, ok2 = swap(html, illus.counted_take(), counted_take_ipad())
    html, ok3 = swap(html, illus.drum_dynamics(S=1.0), drum_dynamics_ipad())
    oks = [ok1, ok2, ok3]
    for a4fn, newsvg in ((illus.install_flow, ID.install_flow()), (illus.section_timeline, ID.section_timeline()),
                         (illus.editor_map, ID.editor_map()), (illus.audio_path, ID.audio_path()), (illus.step_pages, ID.step_pages()),
                         (illus.tracks_loop, ID.tracks_loop()), (illus.overdub_stack, ID.overdub_stack()), (illus.soundbank_ribbon, ID.soundbank_ribbon()), (illus.chord_keys, ID.chord_keys()), (illus.chordplus_keys, ID.chordplus_keys()), (illus.four_note_step, ID.four_note_step()), (illus.punch_timeline, ID.punch_timeline())):
        html, ok = swap(html, a4fn(S=1.0), newsvg); oks.append(ok)
    # raw strips (one drawing for both editions in the manuscript): give them an iPad sibling
    def pair(html, start_marker, newsvg):
        i = html.find(start_marker)
        if i < 0: return html, False
        j = html.find("</svg>", i) + 6
        return html[:i] + '<div class="a4-only">' + html[i:j] + '</div><div class="ipad-only">' + newsvg + '</div>' + html[j:], True
    html, ok = pair(html, darken(saved_where()), ID.saved_where()); oks.append(ok)
    # the filter dial sits in an a4/ipad pair made by ipadify (font-scaled copy); replace the ipad copy
    fd = darken(interior.filter_dial())
    i = html.find(fd)
    if i > 0:
        j = html.find('<div class="ipad-only">', i); k = html.find('</div>', j)
        html = html[:j] + '<div class="ipad-only">' + ID.filter_dial() + html[k:]; oks.append(True)
    else: oks.append(False)
    i = html.find("solid = the step"); j = html.rfind('<svg viewBox="0 0 352 70"', 0, i)
    if j > 0:
        html, ok = pair(html, html[j:j+40], ID.slow_music()); oks.append(ok)
    i = html.find("The loop closes, your playing snaps gently into it"); j = html.find('<svg viewBox="0 0 176 30"', i)
    if j > 0:
        html, ok = pair(html, html[j:j+40], ID.free_take()); oks.append(ok)
    import diagrams
    i = html.find('<svg viewBox="0 0 352 90" width="100%">' + darken(diagrams.poly_wide())[:60])
    if i > 0:
        html, ok = pair(html, html[i:i+60], ID.poly_wide()); oks.append(ok)
    print("ipad redraws:", oks)
    return html

def mark_long_asides(html):
    """asides longer than about a third of a screen may continue on the next screen; short ones stay whole"""
    def f(m):
        txt = re.sub(r"<[^>]+>", "", m.group(0))
        return m.group(0).replace('<div class="aside"', '<div class="aside long"', 1) if len(txt) > 650 else m.group(0)
    html = re.sub(r'<div class="aside"[^>]*>.*?</p>\s*</div>', f, html, flags=re.S)
    def g(m):
        txt = re.sub(r"<[^>]+>", "", m.group(0)); cls = m.group(1)
        return m.group(0).replace(f'<div class="{cls}"', f'<div class="{cls} long"', 1) if len(txt) > 650 else m.group(0)
    # translation / caution boxes: the box ends at the first closing div after its last paragraph or list
    return re.sub(r'<div class="(gb|careful)"[^>]*>(?:(?!<div class="(?:gb|careful|mess|try|hear|aside)).)*?</(?:p|ol|ul)>\s*</div>', g, html, flags=re.S)

def label_floor(html, units=8.0):
    """raise any label in an iPad drawing below `units` (per 352 of width) to that size: about 7.1 pt on the iPad mini's screen"""
    def fix(m):
        vbw = float(m.group(2))
        if not (150 <= vbw <= 400): return m.group(0)
        floor = units * vbw / 352
        return re.sub(r'font-size="([0-9.]+)"', lambda f: f'font-size="{max(float(f.group(1)), floor):.2f}"', m.group(0))
    return re.sub(r'(<div class="ipad-only">\s*<svg viewBox="0 0 ([0-9.]+) [0-9.]+".*?</svg>)', fix, html, flags=re.S)

def ipad_moves(html):
    """iPad-only placement: L5's chord-keys figure after the 'Three words' paragraph (A4 keeps it after the start box)"""
    i = html.find('id="l5"'); j = html.find('<figure style="margin:0 0 2mm;width:148mm;">', i)
    k = html.find('</figure>', j) + len('</figure>')
    h3 = html.find('Three words, then the keys do the theory', k)
    if j < 0 or h3 < 0 or j - i > 4000: return html
    fig = html[j:k]
    html = html[:j] + html[k:]
    h3 = html.find('Three words, then the keys do the theory', i)
    pend = html.find('</p>', h3) + 4
    html = html[:pend] + html[pend:]
    # place it inside the steps, after step 3 ("Make wrong notes impossible") and before step 4, where CHORD goes on
    ol = html.find('<ol class="steps">', h3)
    lis = [m.start() for m in re.finditer(r'<li>', html[ol:ol + 9000])]
    if len(lis) >= 4:
        cut = ol + lis[3]
        html = (html[:cut] + '</ol>\n' + fig.replace('margin:0 0 2mm;', 'margin:2mm 0 4mm;') + '\n<ol class="steps" start="4">' + html[cut:])
    # lessons never end on a lone "made a mess?" box: its closing companion travels with it (order unchanged)
    def block_end(h, start):
        """end index of the <div> that opens at start"""
        depth = 0; i = start
        while True:
            m = re.compile(r'<div\b|</div>').search(h, i)
            depth += 1 if m.group(0) != '</div>' else -1; i = m.end()
            if depth == 0: return i
    # L2: "A word you now own" (last block of the row) joins "made a mess?"
    a = html.find('<div class="aside"><div class="label">A word you now own')
    if a > 0:
        ae = block_end(html, a); aside = html[a:ae]
        html = html[:a] + html[ae:]
        m0 = html.find('<div class="mess">', a); me = block_end(html, m0)
        html = html[:m0] + '<div class="keep">' + aside + html[m0:me] + '</div>' + html[me:]
    # L3: "try this" and "made a mess?" together
    u = html.find('Undo the pass you just made')
    if u > 0:
        t0 = html.rfind('<div class="try">', 0, u); m0 = html.find('<div class="mess">', u); me = block_end(html, m0)
        html = html[:t0] + '<div class="keep">' + html[t0:me] + '</div>' + html[me:]
    # L8: the closing row (try, parked note, made a mess?) stays whole
    st = html.find('A step you just set')
    if st > 0:
        r0 = html.rfind('<div class="row"', 0, st)
        html = html[:r0] + '<div class="row keep"' + html[r0 + len('<div class="row"'):]
    return html

def assemble_ipad(pages_by_id):
    out = []
    for s in ORDER:
        if s == "CONTENTS": s = B.contents(pages_by_id)
        out.append(s)
    body = B.SYMBOLS + "\n".join(out)
    body = ipad_moves(mark_long_asides(label_floor(ipad_redraws(darken(body)))))
    # iPad only: the stacked PLAY / STOP legend on every hardware drawing a step larger (it is the smallest printed label)
    body = re.sub(r'font-size="11(?:\.5)?" font-weight="700" fill="#e8e8e8" text-anchor="middle">(PLAY|STOP)<', r'font-size="13" font-weight="700" fill="#e8e8e8" text-anchor="middle">\1<', body)
    body = re.sub(r'font-size="12(?:\.5)?" font-weight="700" fill="#e8e8e8" text-anchor="middle">([A-Z+\u2212]{2,6})<', r'font-size="13.5" font-weight="700" fill="#e8e8e8" text-anchor="middle">\1<', body)   # button legends
    html = ('<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>SLOOP, Gently · iPad mini edition (SLOOP 2.8.4)</title>'
            f'<style>{css("ipad")}</style></head><body class="ed-ipad">\n{body}\n</body></html>')
    html = B.inline_imgs(html)
    html = B.resolve_xrefs(html, pages_by_id)
    return B.glyph_pass(html)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "a4"
    if which in ("a4", "all"):
        html = assemble_a4(pages_by_id_a4())
        open(P("out", "SLOOP-Gently-A4.html"), "w", encoding="utf-8").write(html)
        print("A4 pages:", len(ORDER))
        B.render(P("out", "SLOOP-Gently-A4.html"), P("out", "SLOOP-Gently-A4.pdf")); print("A4 rendered")
    if which in ("ipad", "all"):
        html = assemble_ipad({})
        open(P("out", "SLOOP-Gently-iPad-Mini.html"), "w", encoding="utf-8").write(html)
        B.render(P("out", "SLOOP-Gently-iPad-Mini.html"), P("out", "SLOOP-Gently-iPad-Mini.pdf")); print("iPad pass 1")
        ap = B.anchor_pages(P("out", "SLOOP-Gently-iPad-Mini.pdf"))
        html = assemble_ipad(ap)
        open(P("out", "SLOOP-Gently-iPad-Mini.html"), "w", encoding="utf-8").write(html)
        B.render(P("out", "SLOOP-Gently-iPad-Mini.html"), P("out", "SLOOP-Gently-iPad-Mini.pdf")); print("iPad pass 2; anchors:", len(ap))
