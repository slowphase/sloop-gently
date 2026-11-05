#!/usr/bin/env python3
"""Build SLOOP, Gently v2: one content source, two editions (A4 art-directed pages; iPad mini reflow).
Usage: python3 build.py [a4|ipad|all] [--no-render]"""
import base64, os, re, subprocess, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art, diagrams, illus, interior

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
CHROME = "google-chrome"

# ------------------------------------------------------------------ helpers
def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def inline_fonts(css):
    return re.sub(r"url\(fonts/([^)]+)\)", lambda m: f"url({data_uri(P('fonts', m.group(1)), 'font/woff2')})", css)

def inline_imgs(html):
    return re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: data_uri(P("img", m.group(1)), "image/png"), html)

def split_sections(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    parts = re.split(r'(?=<section class="page)', html)
    return [p for p in parts if p.strip().startswith('<section')]

def strip_chrome(sec):
    sec = re.sub(r'<!--.*?-->\s*', '', sec, flags=re.S).lstrip()
    sec = re.sub(r'\s*<div class="runhead">.*?</div>\s*', '\n', sec, flags=re.S)
    sec = re.sub(r'\s*<div class="folio">.*?</div>\s*', '\n', sec, flags=re.S)
    return sec

def set_classes(sec, add):
    m = re.match(r'<section class="([^"]*)"', sec)
    cls = [c for c in m.group(1).split() if c not in ("odd", "even", "nofooter") and not (c.startswith("trk") and any(a.startswith("trk") for a in add))]
    for a in add:
        if a not in cls: cls.append(a)
    return sec.replace(m.group(0), f'<section class="{" ".join(cls)}"', 1)

def close_last(s):
    i = s.rstrip().rfind("</div>")
    return s[:i] + "</section>\n"

def text_of(sec):
    return re.sub(r"<[^>]+>", " ", sec)

SYMBOLS = """<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="g-tracks" x1="0" x2="1"><stop offset="0" stop-color="#5b8ff0"/><stop offset=".36" stop-color="#3fbf7c"/><stop offset=".68" stop-color="#f0bf45"/><stop offset="1" stop-color="#f08045"/></linearGradient>
<linearGradient id="g-rel" x1="0" x2="1"><stop offset="0" stop-color="#2f6fde"/><stop offset="1" stop-color="#2f6fde" stop-opacity="0"/></linearGradient>
<symbol id="i-wave" viewBox="0 0 96 30"><path d="M2,15 C8,1 14,1 20,15 S32,29 38,15 S48,4 54,15 S62,24 68,15 S74,9 79,15 S85,19 88,15 S92,13 94,15" fill="none" stroke="url(#g-tracks)" stroke-width="2.4" stroke-linecap="round"/></symbol>
<symbol id="i-spark" viewBox="0 0 12 12"><path d="M6,0 C6.6,4 8,5.4 12,6 C8,6.6 6.6,8 6,12 C5.4,8 4,6.6 0,6 C4,5.4 5.4,4 6,0Z" fill="currentColor"/></symbol>
<symbol id="i-undo" viewBox="0 0 12 12"><path d="M3.2,4.2 H7.6 A3.1,3.1 0 0 1 7.6,10.4 H4.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M5,1.6 L2.2,4.2 L5,6.8" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-play" viewBox="0 0 12 12"><path d="M3,1.8 L10,6 L3,10.2Z" fill="currentColor"/></symbol>
</defs></svg>
"""

def adapt_proto(s):
    """prototype pages used h2.title/h3.sub; the book system uses h1/h2"""
    s = s.replace('<h2 class="title compact">', '<h1>').replace('<h2 class="title">', '<h1>')
    s = re.sub(r'<h3 class="sub"([^>]*)>(.*?)</h3>', r'<h2\1>\2</h2>', s, flags=re.S)
    s = s.replace('<span class="aside">', '<span class="aside-t">')
    s = s.replace('<svg viewBox="0 0 96 30" width="24mm" height="7.5mm"><use href="#i-wave"/></svg>', art.wave_icon())
    return s

# ------------------------------------------------------------------ content
raw = open(P("content.html"), encoding="utf-8").read()
secs = split_sections(raw)
secs = secs[1:]                                   # drop the old cover
about = secs.pop(0)                               # "A hobby, not a syllabus"
secs.pop(0)                                       # drop the old contents

def idx_of(pred):
    for i, s in enumerate(secs):
        if pred(s): return i
    raise KeyError

# prototype compositions replace their pages
def proto(name, fills):
    s = open(P(name), encoding="utf-8").read()
    for k, v in fills.items(): s = s.replace(k, v)
    return adapt_proto(strip_chrome(s))
p11 = proto("proto_p11.html", {})
p20 = proto("proto_p20.html", {"<!--CELLS-->": diagrams.cells(), "<!--DIALS-->": diagrams.dials()})
p25 = proto("proto_p25.html", {"<!--TIMESCALE-->": diagrams.timescale(), "<!--POLY-->": diagrams.poly()})
for src_html in (p11, p20, p25):
    pass
p11 = close_last(p11.replace('<div class="page odd trk1">', '<section class="page trk1" data-part="Part 1 · Atmosphere">'))
p20 = close_last(p20.replace('<div class="page even trk4">', '<section class="page trk4" data-part="Part 2 · Rhythm and low end">'))
p25 = close_last(p25.replace('<div class="page odd trk1 dense">', '<section class="page trk1" data-part="Part 2 · Rhythm and low end">'))
# sound vignettes on the pad shelf (a curated collection, not a feature grid)
def pad_with_art(m):
    eng = re.search(r'<span class="eng">([A-Z]+)', m.group(0)).group(1)
    return m.group(0).replace('<div class="pad">', '<div class="pad">' + art.pad_art(eng, hash(m.group(1)) % 997), 1)
p11 = re.sub(r'<div class="pad"><span class="nm">([^<]+)</span><span class="eng">[^<]*', pad_with_art, p11)
# split the step-sequencer page in two (refinement 1)
cut = p25.index('<div class="row" style="grid-template-columns:1.9fr 1fr;')
p25a = p25[:cut] + "\n</section>\n"
p25b = ('<section class="page trk1" data-part="Part 2 · Rhythm and low end">\n'
        '<div class="kicker"><span class="chno">L8</span><span>Lesson eight · continued</span></div>\n'
        '<h1>Two clocks in one loop</h1>\n' + p25[cut:])
p25b = p25b.replace('<div class="row" style="grid-template-columns:1.9fr 1fr;align-items:center;gap:6mm;margin-top:0;">',
                    '<div class="row c-1-1" style="align-items:center;">')
# the diagram, drawn large: the only place the book shows two clocks side by side
p25b = re.sub(r'<svg viewBox="0 0 200 58" width="92%">.*?</svg>',
              lambda m: '<figure style="margin:1mm 0 3mm;"><svg viewBox="0 0 352 90" width="100%">' + diagrams.poly_wide() + '</svg></figure>', p25b, flags=re.S)
p25b = p25b.replace('<div class="row c-1-1" style="align-items:center;">', '<div class="row" style="grid-template-columns:1fr;">')
p25b = p25b.replace('<div class="hear" style="margin:3mm 0 3mm;padding:3.4mm 5mm 3.4mm 4.4mm;">', '<div class="hear">')

i = idx_of(lambda s: 'id="l1"' in s); secs[i + 1] = p11
i = idx_of(lambda s: 'slow&#8209;music trick' in s and 'Build a slow chord bed' in s); secs[i:i + 1] = [p25a, p25b]

# the illustrated compositions approved in round 2 (pages 14, 18, 23), with iPad variants of every drawing
import interior_sections as IP
def ipadify(sec):
    """every large drawing gets a sibling with larger lettering for the iPad edition"""
    def rep(m):
        svg_ = m.group(0)
        if 'class="wave"' in svg_ or 'viewBox="0 0 12 12"' in svg_ or 'class="gl' in svg_: return svg_
        return '<div class="a4-only">' + svg_ + '</div><div class="ipad-only">' + illus.scale_fonts(svg_, 1.32) + '</div>'
    return re.sub(r'<svg\b.*?</svg>', rep, sec, flags=re.S)
def from_interior(page_html, data_part):
    s = strip_chrome(page_html)
    s = re.sub(r'<section class="page[^"]*"', f'<section class="page r2" data-part="{data_part}"', s, count=1)
    s = re.sub(r'\s*data-part="[^"]*"\s*data-part=', ' data-part=', s)
    return ipadify(s)
p14 = from_interior(IP.p14, "Part 1 · Atmosphere")
p18 = from_interior(IP.p18, "Part 1 · Atmosphere")
p23 = IP.p23.replace(re.search(r'<figure style="[^"]*">' + re.escape(interior.four_bars()) + r'</figure>', IP.p23).group(0),
                     '<figure style="margin:0 0 1mm;width:150mm;">' + illus.counted_take() + '</figure>') if interior.four_bars() in IP.p23 else IP.p23
p23 = from_interior(p23, "Part 2 · Rhythm and low end")
i = idx_of(lambda s: 'id="l2"' in s); secs[i] = p14
i = idx_of(lambda s: 'id="l4"' in s); secs[i] = p18
i = idx_of(lambda s: 'A pattern to copy' in s); secs[i] = p23

# every other lesson that benefits from one explanatory graphic
import pages2
secs = pages2.apply(secs)

# the hardware diagram: on the iPad edition it turns through 90° and fills a page of its own
i = idx_of(lambda s: 'id="ch3"' in s)
hw = secs[i]
m = re.search(r'(<svg viewBox="70 236 860 618".*?</svg>)', hw, flags=re.S)
hw_svg = m.group(1)
hw = hw.replace(hw_svg, '<div class="hw-a4 a4-only">' + hw_svg + '</div>')
# iPad: the diagram page comes first, then the chapter text (so the heading and its table sit together)
hw = re.sub(r'(<section class="page[^>]*>\s*)', r'\1<div class="hw-ipad ipad-only"><div class="hw-rot">' + hw_svg.replace('\\', '\\\\') + '</div></div>', hw, count=1)
secs[i] = hw

# the 16 drum sounds: A4 keeps the two-row strip; iPad gets a four-row grid
i = idx_of(lambda s: 'id="l6"' in s)
m = re.search(r'(<svg viewBox="0 0 176 22".*?</svg>)', secs[i], flags=re.S)
secs[i] = secs[i].replace(m.group(1), '<div class="a4-only">' + m.group(1) + '</div>'
    '<div class="ipad-only"><svg viewBox="0 0 176 53" width="100%" style="margin:1mm 0 2mm;">' + diagrams.drum_keys_tall() + '</svg></div>')

# running-head labels and track colours per lesson
TRK = {"ch1": "trk0", "ch2": "trk0", "ch3": "trk0", "l1": "trk1", "l2": "trk1", "l3": "trk1", "l4": "trk0", "l5": "trk2",
       "l6": "trk4", "l7": "trk3", "l8": "trk4", "l9": "trk0", "l10": "trk0", "ch14": "trk0", "ch15": "trk0",
       "r1": "trk0", "r2": "trk0", "gloss": "trk0", "links": "trk0"}
GLOBAL_HEAD = {"l4": "global · any track", "l9": "the whole mix", "l10": "all four tracks"}
LBL = {"ch1": "1 · what SLOOP turns your FM-1 into", "ch2": "2 · install, back up, stay safe", "ch3": "3 · meet the hardware",
       "l1": "L1 · your first sound", "l2": "L2 · shaping a sound", "l3": "L3 · record your first loop", "l4": "L4 · weather",
       "l5": "L5 · playing in key", "l6": "L6 · drums, gently", "l7": "L7 · bass, melody and the mix",
       "l8": "L8 · the step sequencer, essentials only", "l9": "L9 · live hands", "l10": "L10 · sections, songs, saving",
       "ch14": "14 · the web editor", "ch15": "15 · where to next", "r1": "reference · everyday controls",
       "r2": "reference · deeper shortcuts", "gloss": "glossary", "links": "troubleshooting & links"}
TRKNO = {"trk1": "track 1", "trk2": "track 2", "trk3": "track 3", "trk4": "track 4", "trk0": ""}

# ------------------------------------------------------------------ openers, cover, contents
def opener(pid, no, title, quiet, artsvg, art_style, trk, kind="wide"):
    return (f'<section class="page opener {trk}" id="{pid}" data-part="{title}">\n'
            f'<svg class="art {kind} art-{pid}" {art_style}>{artsvg[artsvg.index(">")+1:]}'
            f'<div class="inner" style="top:34mm;"><div class="partno">PART {no}</div>'
            f'<div class="big" style="margin-top:4mm;">{title}</div>'
            f'<div class="quiet" style="margin-top:9mm;">{quiet}</div></div>\n</section>\n')

def svg_open(s):   # take the <svg …> open tag's attributes from a generated svg
    return s[:s.index(">")]

op0 = opener("part0", "0", "Before<br>the music", "Install it, back it up, learn the panel. Ten quiet minutes, and then nothing stands between you and the keys.",
             art.ring(140, 3, 2200), 'viewBox="0 0 140 140"', "trk1", "ring")
op1 = opener("part1", "1", "Atmosphere", "A sound you can live inside. We start with pads, reverb and weather, and learn to make the FM&#8209;1 hold a chord while your hands wander.",
             art.cloud(210, 130, 11, 5200), 'viewBox="0 0 210 130" preserveAspectRatio="none"', "trk1")
op2 = opener("part2", "2", "Rhythm<br>and low end", "Sixteen steps make a bar. Drums arrive quietly, the bass holds the floor, and the step sequencer shows you the shape of what you played.",
             art.pulse(210, 115, 2), 'viewBox="0 0 210 115" preserveAspectRatio="none"', "trk4")
op3 = opener("part3", "3", "Performing<br>and keeping it", "Effects under your fingers, sections on the bar, and the small habit that protects weeks of music.",
             art.ribbons(210, 125, 4), 'viewBox="0 0 210 125" preserveAspectRatio="none"', "trk2")
op4 = opener("part4", "4", "Reference", "Two sheets to print and keep beside the FM&#8209;1, a plain&#8209;words glossary, and where to go when something seems wrong.",
             art.ring(140, 9, 1600, playhead=False), 'viewBox="0 0 140 140"', "trk3", "ring")

cover = ('<section class="page cover" id="cover">\n'
         f'<svg class="field" {svg_open(art.field(210,150,7,5400))[4:]}>{art.field(210,150,7,5400).split(">",1)[1]}'
         '<div class="title">SLOOP,<br>Gently</div>'
         '<div class="sub">Atmospheres first, drums later.<br>A slow, friendly tour of the M&#8209;VAVE FM&#8209;1<br>running the SLOOP groovebox firmware.</div>'
         '<div class="meta">A BEGINNER\'S HANDBOOK · WRITTEN FOR SLOOP <b>2.8.4</b> · BETA FIRMWARE · NOVEMBER 2026</div>\n</section>\n')

TOC = [("Part 0 · Before the music", "trk1", [("1", "ch1", "What SLOOP turns your FM-1 into"), ("2", "ch2", "Install, back up, stay safe"), ("3", "ch3", "Meet the hardware")]),
       ("Part 1 · Atmosphere", "trk1", [("L1", "l1", "Your first sound"), ("L2", "l2", "Shaping a sound"), ("L3", "l3", "Record your first loop"), ("L4", "l4", "Weather: textures and dust"), ("L5", "l5", "Playing in key")]),
       ("Part 2 · Rhythm and low end", "trk4", [("L6", "l6", "Drums, gently"), ("L7", "l7", "Bass, melody and the mix"), ("L8", "l8", "The step sequencer, essentials only")]),
       ("Part 3 · Performing and keeping it", "trk2", [("L9", "l9", "Live hands: punch-in effects and fills"), ("L10", "l10", "Sections, songs, and saving your music"), ("14", "ch14", "The web editor in ten minutes"), ("15", "ch15", "Where to next: the advanced shelf")]),
       ("Part 4 · Reference", "trk3", [("R1", "r1", "Everyday controls"), ("R2", "r2", "Deeper shortcuts"), ("G", "gloss", "Plain-words glossary"), ("T", "links", "Troubleshooting & links")])]
COL = {"trk1": "#2f6fde", "trk2": "#22995a", "trk3": "#e0a92a", "trk4": "#e2661d"}

def contents(pages_by_id):
    cols = [[], []]
    for k, (part, trk, items) in enumerate(TOC):
        html = f'<div class="toc-part"><i style="background:{COL[trk]}"></i>{part}</div><ul class="toc">'
        for no, pid, title in items:
            html += f'<li><span class="no">{no}</span><a href="#{pid}">{title}</a><span class="pn">{pages_by_id.get(pid, "")}</span></li>'
        html += '</ul>'
        cols[0 if k < 3 else 1].append(html)
    return ('<section class="page" id="contents" data-part="Contents">\n<div class="kicker"><span>Contents</span></div>\n<h1>The journey</h1>\n'
            '<div class="row c-1-1" style="margin-top:4mm;"><div>' + "".join(cols[0]) + '</div><div>' + "".join(cols[1]) +
            '<figure class="shot" style="margin-top:7mm;"><span class="frame"><img src="{{IMG:visualiser.png}}" alt="SLOOP visualiser"></span>'
            '<figcaption><b>The reward for pressing HOME twice:</b> SLOOP\'s full&#8209;width visualiser. Twelve styles; this one draws the stereo image of whatever you are playing. Turn <kbd class="knob">SELECT</kbd> to change style, tap <kbd>HOME</kbd> to leave.</figcaption></figure>'
            '</div></div>\n'
            '<div class="aside" style="margin-top:6mm;"><div class="label">How to use the lessons</div><p>Each lesson opens with <b>starting from here</b>, the exact state it assumes, so you can sit down weeks later and do any lesson on its own. Each one ends with an audible result, a small <b>try this</b> idea, and a <b>made a mess?</b> note for undoing whatever went sideways.</p></div>\n</section>\n')

# ------------------------------------------------------------------ assemble order
about = set_classes(about, ["trk0"])
order = [cover, about, "CONTENTS", op0]
for s in secs:
    if 'id="l1"' in s: order.append(op1)
    if 'id="l6"' in s: order.append(op2)
    if 'id="l9"' in s: order.append(op3)
    if 'id="r1"' in s: order.append(op4)
    order.append(s)

def chrome(sec, n, cur):
    """A4 page chrome: running head, folio, track class, odd/even"""
    m = re.search(r'id="([a-z0-9]+)"', sec[:200])
    pid = m.group(1) if m else None
    if pid in TRK: cur["trk"] = TRK[pid]; cur["glob"] = GLOBAL_HEAD.get(pid, "")
    if pid in LBL: cur["lbl"] = LBL[pid]
    trk = cur["trk"]; lbl = cur["lbl"]
    own = re.search(r'<section class="[^"]*\b(trk[0-4])\b', sec[:200])      # a page may carry its own track class
    if own: trk = own.group(1)
    sec = set_classes(sec, [trk, "odd" if n % 2 else "even"])
    if "opener" in sec[:120] or "cover" in sec[:120]:
        head = ""
    elif "refpage" in sec[:160] or pid in ("gloss", "links") or cur["lbl"].startswith(("reference", "glossary", "troubleshooting")):
        head = f'<div class="runhead"><span>{lbl}</span><span>SLOOP 2.8.4</span></div>'
    elif trk == "trk0":
        oh = re.search(r'data-head="([^"]*)"', sec[:300])
        right = oh.group(1) if oh else cur.get("glob", "")
        head = f'<div class="runhead"><span>{lbl}</span><span>{right}</span></div>'
    else:
        head = f'<div class="runhead"><span>{lbl}</span><span class="trk">{TRKNO[trk]}</span></div>'
    folio = "" if "cover" in sec[:120] else f'<div class="folio"><span class="n">{n}</span><span class="t">SLOOP, Gently</span></div>'
    close = sec.rstrip()
    assert close.endswith("</section>"), sec[:80]
    return close[:-len("</section>")] + head + folio + "\n</section>\n"

def glyph_pass(html):
    # arrows and ≈ are missing from the Latin subsets: draw them, so the PDF keeps to its three families
    ARROW = '<svg class="gl" viewBox="0 0 12 10" aria-label="→"><path d="M1,5 H10.2 M7,1.8 L10.4,5 L7,8.2" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    DARROW = '<svg class="gl" viewBox="0 0 14 10" aria-label="↔"><path d="M1.6,5 H12.4 M4.6,1.8 L1.4,5 L4.6,8.2 M9.4,1.8 L12.6,5 L9.4,8.2" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    APPROX = '<svg class="gl approx" viewBox="0 0 12 10" aria-label="≈"><path d="M1.2,3.6 C3,1.6 4.6,1.6 6,3.3 C7.4,5 9,5 10.8,3 M1.2,7.2 C3,5.2 4.6,5.2 6,6.9 C7.4,8.6 9,8.6 10.8,6.6" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round"/></svg>'
    parts = re.split(r"(<svg\b.*?</svg>)", html, flags=re.S)
    for k, part in enumerate(parts):
        if not part.startswith("<svg"):
            parts[k] = part.replace("→", ARROW).replace("↔", DARROW)
    html = "".join(parts)
    html = html.replace(".gb::before{content:\"≈\";", ".gb::before{content:\"\";")
    html = html.replace('<div class="gb">', '<div class="gb">' + APPROX)
    # non-breaking hyphen is missing from the Latin font subsets: hold the word together with a span (plain hyphen inside SVG)
    parts = re.split(r"(<svg\b.*?</svg>)", html, flags=re.S)
    for k, part in enumerate(parts):
        if part.startswith("<svg"):
            parts[k] = part.replace("&#8209;", "-")
        else:
            parts[k] = re.sub(r"(\w+)&#8209;(\w+)", r'<span style="white-space:nowrap">\1-\2</span>', part).replace("&#8209;", "-")
    return "".join(parts)

XREF = [('<a href="#ch15">"Where to next", page&nbsp;31</a>', '<a href="#ch15">"Where to next", page&nbsp;{{P:ch15}}</a>'),
        ('<a href="#ch15">page&nbsp;31</a>', '<a href="#ch15">page&nbsp;{{P:ch15}}</a>'),
        ('<a href="#links">page&nbsp;35</a>', '<a href="#links">page&nbsp;{{P:links}}</a>'),
        ("page&nbsp;8's map", '<a href="#ch3">page&nbsp;{{P:ch3}}</a>\'s map'),
        ('<a href="#">"Where to next", page&nbsp;31</a>', '<a href="#ch15">"Where to next", page&nbsp;{{P:ch15}}</a>')]
def resolve_xrefs(html, pages_by_id):
    for a, t in XREF: html = html.replace(a, t)
    return re.sub(r"\{\{P:([a-z0-9]+)\}\}", lambda m: str(pages_by_id.get(m.group(1), "?")), html)

def assemble(edition, pages_by_id=None):
    pages_by_id = pages_by_id or {}
    out = []; cur = {"trk": "trk0", "lbl": "SLOOP, Gently", "glob": ""}
    for n, s in enumerate(order, 1):
        if s == "CONTENTS":
            s = contents(pages_by_id)
        out.append(chrome(s, n, cur) if edition == "a4" else s)
    body = "\n".join(out)
    css = inline_fonts(open(P("ds.css"), encoding="utf-8").read() + "\n" + open(P(f"{edition}.css"), encoding="utf-8").read())
    body = SYMBOLS + body
    html = ('<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>SLOOP, Gently — a beginner\'s handbook for the M-VAVE FM-1 (SLOOP 2.8.4)</title>'
            f'<style>{css}</style></head><body class="ed-{edition}">\n{body}\n</body></html>')
    html = inline_imgs(html)
    html = resolve_xrefs(html, pages_by_id)
    return glyph_pass(html)

def a4_pages_by_id():
    d = {}
    for n, s in enumerate(order, 1):
        m = re.search(r'id="([a-z0-9]+)"', (s if s != "CONTENTS" else '')[:200])
        if m: d[m.group(1)] = n
    return d

def render(html_path, pdf_path):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path], check=True, capture_output=True)

def pdf_pages_by_id(pdf_path, ids):
    """where did each anchor land? (read the contents page's link destinations)"""
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    pageno = {p.indirect_reference.idnum: i + 1 for i, p in enumerate(r.pages)}
    found = {}
    for p in r.pages[:6]:
        for a in (p.get("/Annots") or []):
            o = a.get_object()
            A = o.get("/A"); d = o.get("/Dest") or (A.get("/D") if A else None)
            if d is None: continue
            if isinstance(d, str):
                d = r.named_destinations.get(d)
                if d is None: continue
                d = d.get("/Page") if hasattr(d, "get") else d
                tgt = d
            else:
                tgt = d[0]
            try: found.setdefault(None, 0)
            except Exception: pass
            try:
                ref = tgt.indirect_reference if hasattr(tgt, "indirect_reference") else tgt
                found_page = pageno.get(ref.idnum)
            except Exception:
                found_page = None
            if found_page: found[(o.get("/Rect")[1], o.get("/Rect")[0])] = found_page
    return found

def anchor_pages(pdf_path):
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    pages = {p.indirect_reference.idnum: i + 1 for i, p in enumerate(r.pages)}
    out = {}
    for name, dest in r.named_destinations.items():
        try:
            pg = dest.get("/Page") if hasattr(dest, "get") else dest[0]
            ref = pg if hasattr(pg, "idnum") else pg.indirect_reference
            out[str(name).lstrip("/")] = pages[ref.idnum]
        except Exception:
            pass
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    no_render = "--no-render" in sys.argv
    if which in ("a4", "all"):
        html = assemble("a4", a4_pages_by_id())
        open(P("sloop-gently-A4.html"), "w", encoding="utf-8").write(html)
        print("A4 pages:", len(order))
        if not no_render:
            render(P("sloop-gently-A4.html"), P("sloop-gently-A4.pdf")); print("A4 rendered")
    if which in ("ipad", "all"):
        html = assemble("ipad", {})
        open(P("sloop-gently-iPad.html"), "w", encoding="utf-8").write(html)
        if not no_render:
            render(P("sloop-gently-iPad.html"), P("sloop-gently-iPad.pdf")); print("iPad pass 1 rendered")
            ap = anchor_pages(P("sloop-gently-iPad.pdf"))
            html = assemble("ipad", ap)
            open(P("sloop-gently-iPad.html"), "w", encoding="utf-8").write(html)
            render(P("sloop-gently-iPad.html"), P("sloop-gently-iPad.pdf")); print("iPad pass 2 rendered; anchors:", len(ap))
