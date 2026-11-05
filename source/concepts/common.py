"""Shared plumbing for the three Weather-lesson concepts: fonts, images, the hardware drawing, rendering."""
import base64, glob, os, re, subprocess, io, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "..", "book")
FONTS = os.path.join(HERE, "fonts")
CHROME = "google-chrome"

def b64(data, mime): return f"data:{mime};base64," + base64.b64encode(data).decode()

def font_face(family_dir, family_name, weights, italics=()):
    """@font-face rules with the woff2 inlined (Fontsource latin subsets)."""
    out = []
    files = glob.glob(os.path.join(FONTS, f"fontsource-{family_dir}-*", "package", "files", "*"))
    for w in weights:
        for style in (("normal",) + (("italic",) if w in italics else ())):
            fn = [f for f in files if f.endswith(f"-latin-{w}-{style}.woff2")]
            if not fn: raise SystemExit(f"missing {family_dir} {w} {style}")
            out.append(f'@font-face{{font-family:"{family_name}";font-weight:{w};font-style:{style};'
                       f'src:url({b64(open(fn[0],"rb").read(),"font/woff2")}) format("woff2");}}')
    return "\n".join(out)

def img_uri(name):
    p = os.path.join(BOOK, "img", name)
    return b64(open(p, "rb").read(), "image/png")

# ------------------------------------------------------------------ the FM-1, from the photo-traced drawing
def fm1(viewbox=None, highlight=(), screen_img=None, annotations=False, body="#3a3a3d", glow="#f2c14e", label_font="Inter"):
    """Return the hardware SVG (geometry untouched) restyled: optional crop, highlighted controls, the real screen on the screen.
    highlight: iterable of printed labels, e.g. ("GLO","FX","KNOB2")."""
    s = open(os.path.join(BOOK, "fm1_topview.svg")).read()
    # drop the annotation layer (SLOOP key numbers/notes, legend row, screen note) unless asked for
    if not annotations:
        s = re.sub(r'<text[^>]*fill="#a8c4f2"[^>]*>.*?</text>', "", s)
        s = re.sub(r'<text[^>]*fill="#3d5a80"[^>]*>.*?</text>', "", s)
        s = re.sub(r'<text[^>]*fill="#8a8378"[^>]*>.*?</text>', "", s)
        s = re.sub(r'<line[^>]*stroke="#3d5a80"[^>]*/>', "", s)
        s = re.sub(r'<rect x="(86|318|642)" y="817".*?</text>', "", s, flags=re.S)
        s = re.sub(r'<text x="396" y="368"[^>]*>SCREEN</text>', "", s)
        s = re.sub(r'<circle cx="(341|377|413|449)" cy="434" r="10" fill="none" stroke="#[0-9a-f]+" stroke-width="3"/>', "", s)
        s = re.sub(r'<text x="[0-9.]+" y="[0-9.]+"[^>]*fill="#5a544a"[^>]*>.*?</text>', "", s)
    s = s.replace('fill="#3a3a3d"', f'fill="{body}"', 1)
    s = s.replace(f'font-family="Inter"', f'font-family="{label_font}"')
    if screen_img:
        s = s.replace('<rect x="318" y="311" width="156" height="150" rx="5" fill="#050505" stroke="#2c2c2c" stroke-width="1"/>',
                      '<rect x="318" y="311" width="156" height="150" rx="5" fill="#050505"/>'
                      f'<image href="{screen_img}" x="321" y="311" width="150" height="150" preserveAspectRatio="xMidYMid slice"/>')
    for h in highlight:
        if h.startswith("KNOB"):
            cx = {"KNOB1": 553, "KNOB2": 648, "KNOB3": 742, "KNOB4": 838}[h]
            s = s.replace(f'<circle cx="{cx}" cy="327" r="19" fill="#202023" stroke="#141415" stroke-width="1.5"/>',
                          f'<circle cx="{cx}" cy="327" r="26" fill="none" stroke="{glow}" stroke-width="2.5" opacity=".95"/>'
                          f'<circle cx="{cx}" cy="327" r="19" fill="#202023" stroke="{glow}" stroke-width="1.5"/>')
        else:
            if h == "PLAY":
                m = re.search(r'<rect x="(752)" y="(451)" width="46" height="44" rx="8" fill="#1c1c1e" stroke="#0e0e0f" stroke-width="1.2"/>', s)
            else:
                m = re.search(rf'<rect x="([0-9.]+)" y="([0-9.]+)" width="46" height="44" rx="8" fill="#1c1c1e" stroke="#0e0e0f" stroke-width="1.2"/>\s*<text x="[0-9.]+" y="[0-9.]+"[^>]*>{h}</text>', s)
            if m:
                x, y = m.group(1), m.group(2)
                s = s.replace(m.group(0), m.group(0).replace('fill="#1c1c1e" stroke="#0e0e0f" stroke-width="1.2"',
                              f'fill="#1c1c1e" stroke="{glow}" stroke-width="3"', 1)
                              + f'<rect x="{float(x)-6}" y="{float(y)-6}" width="58" height="56" rx="12" fill="none" stroke="{glow}" stroke-width="1.2" opacity=".7"/>')
    if viewbox:
        s = re.sub(r'viewBox="[^"]+"', f'viewBox="{viewbox}"', s, 1)
    s = s.replace('style="margin:1mm 0 0;"', "")
    return s

# ------------------------------------------------------------------ generated "photographs" of weather (PIL + numpy)
def texture_image(kind, w=900, h=600, seed=1, tint=(20, 22, 26), fg=(220, 214, 200), jpeg_q=82):
    import numpy as np
    from PIL import Image, ImageFilter, ImageDraw
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), dtype=np.float32)
    for c in range(3): base[..., c] = tint[c]
    # soft vignette / gradient
    yy, xx = np.mgrid[0:h, 0:w]
    grad = (1 - ((xx / w - .5) ** 2 + (yy / h - .5) ** 2) * 1.1).clip(0, 1)
    base *= (0.55 + 0.45 * grad)[..., None]
    img = Image.fromarray(base.clip(0, 255).astype("uint8"))
    d = ImageDraw.Draw(img, "RGBA")
    if kind == "rain":
        # distant warm lights, out of focus
        for _ in range(28):
            x = rng.integers(0, w); y = rng.integers(int(h * .35), h); r = rng.integers(14, 60)
            col = (236, 196, 120) if rng.random() < .6 else (160, 190, 230)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(rng.integers(14, 40)),))
        img = img.filter(ImageFilter.GaussianBlur(9)); d = ImageDraw.Draw(img, "RGBA")
        for _ in range(1400):
            x = rng.integers(0, w); y = rng.integers(0, h); ln = rng.integers(14, 90); a = int(rng.integers(40, 150))
            d.line([(x, y), (x - ln * .16, y + ln)], fill=fg + (a,), width=1)
        for _ in range(90):
            x = rng.integers(0, w); y = rng.integers(0, h); r = rng.integers(5, 30); a = int(rng.integers(30, 90))
            d.ellipse([x - r, y - r, x + r, y + r], outline=fg + (a,), width=2)
            d.ellipse([x - r*.5, y - r*.3, x + r*.2, y + r*.3], outline=fg + (a//2,), width=1)
        img = img.filter(ImageFilter.GaussianBlur(0.7))
    elif kind == "vinyl":
        cx, cy = w * 1.25, h * .5
        for r in range(40, int(w * 1.4), 3):
            a = int(60 + 50 * math.sin(r * .21) + rng.integers(0, 40))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg + (max(20, min(a, 140)),), width=1)
        for _ in range(400):
            x = rng.integers(0, w); y = rng.integers(0, h)
            d.point((x, y), fill=fg + (int(rng.integers(60, 200)),))
        img = img.filter(ImageFilter.GaussianBlur(0.6))
    elif kind == "tape":
        for y in range(0, h, 2):
            a = int(25 + 25 * math.sin(y * .05) + rng.integers(0, 25))
            d.line([(0, y + rng.integers(-1, 2)), (w, y)], fill=fg + (a,), width=1)
        for _ in range(12):
            x = rng.integers(0, w); d.line([(x, 0), (x + rng.integers(-40, 40), h)], fill=fg + (int(rng.integers(30, 80)),), width=rng.integers(1, 3))
        img = img.filter(ImageFilter.GaussianBlur(1.2))
    elif kind == "wind":
        for i in range(70):
            y0 = rng.integers(-50, h + 50); amp = rng.integers(20, 90); ph = rng.random() * 6; a = int(rng.integers(25, 90))
            pts = [(x, y0 + amp * math.sin(x / w * 6 + ph) * math.sin(x / w * 1.3)) for x in range(0, w, 8)]
            d.line(pts, fill=fg + (a,), width=rng.integers(1, 3))
        img = img.filter(ImageFilter.GaussianBlur(1.5))
    elif kind == "radio":
        arr = np.array(img).astype(np.float32)
        noise = rng.normal(0, 1, (h, w))
        for _ in range(9):
            y = rng.integers(0, h); hh = rng.integers(4, 40); arr[y:y + hh] += rng.normal(0, 1, (min(hh, h - y), w, 1)) * 60 + 20
        arr += noise[..., None] * 22
        img = Image.fromarray(arr.clip(0, 255).astype("uint8"))
    elif kind == "room":
        arr = np.array(img).astype(np.float32)
        # very soft, almost nothing: a window of light and fine grain
        arr += (grad[..., None] * 18)
        arr += rng.normal(0, 1, (h, w, 1)) * 7
        img = Image.fromarray(arr.clip(0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(2))
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([w * .62, h * .18, w * .86, h * .74], fill=fg + (26,))
    # film grain on everything
    arr = np.array(img).astype(np.float32)
    arr += rng.normal(0, 1, (h, w, 1)) * 6
    img = Image.fromarray(arr.clip(0, 255).astype("uint8"))
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=jpeg_q)
    return b64(buf.getvalue(), "image/jpeg")

def render(html, out_pdf, name):
    p = os.path.join(HERE, "out", name + ".html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", p], check=True, capture_output=True)
    return out_pdf

ARROW = '<svg class="arr" viewBox="0 0 12 10" style="height:.62em;width:.75em;vertical-align:-.02em;display:inline-block"><path d="M1,5 H10.2 M7,1.8 L10.4,5 L7,8.2" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def glyphs(html):
    return html.replace("<arrow/>", ARROW)
