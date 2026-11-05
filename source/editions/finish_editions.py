#!/usr/bin/env python3
"""Post-process both PDFs: bookmark outline (built from the anchors' real page numbers), metadata, link audit."""
import sys, re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

OUTLINE = [
 ("Cover", "cover"),
 ("Part 0 · Before the music", "part0", [("About this book", "about"), ("Contents", "contents"),
   ("1 · What SLOOP turns your FM-1 into", "ch1"), ("2 · Install, back up, stay safe", "ch2"), ("3 · Meet the hardware", "ch3")]),
 ("Part 1 · Atmosphere", "part1", [("L1 · Your first sound", "l1"), ("L2 · Shaping a sound", "l2"), ("L3 · Record your first loop", "l3"),
   ("L4 · Weather: textures and dust", "l4"), ("L5 · Playing in key", "l5")]),
 ("Part 2 · Rhythm and low end", "part2", [("L6 · Drums, gently", "l6"), ("L7 · Bass, melody and the mix", "l7"), ("L8 · The step sequencer, essentials only", "l8")]),
 ("Part 3 · Performing and keeping it", "part3", [("L9 · Live hands: punch-in effects and fills", "l9"), ("L10 · Sections, songs, and saving your music", "l10"),
   ("14 · The web editor in ten minutes", "ch14"), ("15 · Where to next: the advanced shelf", "ch15")]),
 ("Part 4 · Reference", "part4", [("R1 · Everyday controls", "r1"), ("R2 · Deeper shortcuts", "r2"), ("Plain-words glossary", "gloss"), ("Troubleshooting & links", "links")]),
]

def anchor_pages(reader):
    """page index for every named destination (Chrome writes id anchors as named dests)"""
    pages = {p.indirect_reference.idnum: i for i, p in enumerate(reader.pages)}
    out = {}
    for name, dest in reader.named_destinations.items():
        try:
            pg = dest.get("/Page") if hasattr(dest, "get") else dest[0]
            ref = pg if hasattr(pg, "idnum") else pg.indirect_reference
            out[str(name).lstrip("/")] = pages[ref.idnum]
        except Exception:
            pass
    # pages without an inbound link (openers, about): find by their text
    marks = {"part0": "PART 0", "part1": "PART 1", "part2": "PART 2", "part3": "PART 3", "part4": "PART 4",
             "about": "A hobby, not a syllabus", "contents": "The journey"}
    for i, p in enumerate(reader.pages[:8] if False else reader.pages):
        t = p.extract_text() or ""
        for k, m in marks.items():
            if k not in out and m in t: out[k] = i
    return out

def finish(path, subject):
    r = PdfReader(path)
    if r.outline:
        print(path, "already finished; rebuild first"); return set()
    w = PdfWriter(); w.append(r)
    ap = anchor_pages(r)
    ap.setdefault("cover", 0)
    # part openers sit on the page before their first chapter (both editions)
    for part, first in (("part0", "ch1"), ("part1", "l1"), ("part2", "l6"), ("part3", "l9"), ("part4", "r1")):
        if part not in ap and first in ap: ap[part] = ap[first] - 1
    missing = []
    def add(title, key, parent=None):
        if key not in ap: missing.append(key); return parent
        return w.add_outline_item(title, ap[key], parent=parent)
    for item in OUTLINE:
        node = add(item[0], item[1])
        for t, k in (item[2] if len(item) > 2 else []):
            add(t, k, node)
    w.add_metadata({"/Title": "SLOOP, Gently: a beginner's handbook for the M-VAVE FM-1 (SLOOP 2.8.4)",
                    "/Author": "suprsomething", "/Subject": subject})
    tmp = path + ".tmp"
    with open(tmp, "wb") as f: w.write(f)
    import os; os.replace(tmp, path)
    # audit
    r2 = PdfReader(path)
    ext = set(); internal = 0; broken = 0
    for p in r2.pages:
        for a in (p.get("/Annots") or []):
            o = a.get_object()
            if o.get("/Subtype") != "/Link": continue
            A = o.get("/A")
            if A and A.get("/S") == "/URI": ext.add(str(A["/URI"]))
            else:
                d = o.get("/Dest") or (A.get("/D") if A else None)
                if d is None: broken += 1
                elif isinstance(d, str) and d not in r2.named_destinations: broken += 1
                else: internal += 1
    print(f"{path}: {len(r2.pages)} pages · outline items {len(r2.outline)} roots · internal links {internal} (broken {broken}) · external {len(ext)} · missing anchors {missing}")
    return ext

e1 = finish("out/SLOOP-Gently-A4.pdf", "A4 edition · v0.9 Preview · documents SLOOP 2.8.4")
e2 = finish("out/SLOOP-Gently-iPad-Mini.pdf", "iPad mini edition · v0.9 Preview · documents SLOOP 2.8.4")
need = ["isod89.github.io/sloop-fm1", "webapp/editor", "clipper-fm1", "blob/v2.8.4/GUIDE.md", "blob/v2.8.4/SLOOP.md", "releases", "issues", "m-vave.com", "fm1-demo.pingywon", "elektronauts"]
for ed, ext in (("A4", e1), ("iPad", e2)):
    print(ed, "expected URLs present:", all(any(n in u for u in ext) for n in need), "| same set in both:", e1 == e2)
