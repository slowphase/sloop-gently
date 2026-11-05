"""Concept D: the all-dark, screen-first edition. Night page, charcoal surfaces for hierarchy,
warm off-white reading text, lime only for annotation. A4 opener + reading page, and the reading page reflowed for iPad mini."""
import os, math, random
import common as C, weather as W

NIGHT, CHAR, CHAR2 = "#0e0e10", "#19191c", "#232327"
TXT, TXT2, TXT3 = "#ece7db", "#bdb8ac", "#8f8b82"
LIME, HAIR = "#d4ff3a", "#2e2e33"

def css(ipad=False):
    page = "@page{size:128.5mm 195.6mm;margin:0}" if ipad else "@page{size:A4;margin:0}"
    tail = ".pg{width:128.5mm;height:195.6mm;padding:11mm 9mm 12mm;overflow:hidden}" if ipad else ""
    body_pt = 11.4 if ipad else 12.4
    return (C.font_face("albert-sans", "Albert Sans", [300, 400, 600], italics=(300,)) +
            C.font_face("big-shoulders-display", "Big Shoulders", [900]) + f"""
{page}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0}}
html{{background:{NIGHT};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:"Albert Sans";font-weight:300;color:{TXT};background:transparent;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:{body_pt}pt;line-height:1.5}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;background:{NIGHT};break-after:page;margin:0 auto}}
.m{{position:absolute;left:16mm;right:16mm}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);column-gap:5mm}}
.sc{{font-weight:600;font-size:{7.6 if not ipad else 7.8}pt;letter-spacing:.16em;text-transform:uppercase;color:{TXT3}}}
.lime{{color:{LIME}}}
.disp{{font-family:"Big Shoulders";font-weight:900;line-height:.8}}
k,kn,v,b{{font-style:normal;font-weight:600;color:{TXT}}}
k,kn{{letter-spacing:.05em;font-size:.9em;background:{CHAR2};padding:.02em .36em .06em;border-radius:.16em}} kn{{border-radius:1em}}
v{{letter-spacing:.07em;font-size:.9em}}
.rule{{border-top:.35mm solid {TXT}}} .hair{{border-top:.2mm solid {HAIR}}}
.foot{{position:absolute;left:16mm;right:16mm;bottom:10mm;display:flex;justify-content:space-between;align-items:baseline;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;color:{TXT3}}}
.foot .n{{font-family:"Big Shoulders";font-weight:900;font-size:22pt;letter-spacing:0;color:{TXT}}}
/* opener */
.word{{position:absolute;left:0;top:2mm;width:210mm;height:120mm}}
.kick{{position:absolute;left:16mm;top:125mm}}
.title{{position:absolute;left:16mm;top:133mm;font-size:34pt;font-weight:300;letter-spacing:-.02em;line-height:1.05}}
.lead{{position:absolute;left:16mm;top:156mm;width:104mm;font-size:13.6pt;line-height:1.42;color:{TXT}}}
.start{{position:absolute;left:131mm;right:16mm;top:156mm;border-top:.4mm solid {LIME};padding-top:2.4mm;font-size:9.8pt;line-height:1.45;color:{TXT2}}}
.start .sc{{color:{LIME};margin-bottom:1.6mm}}
.hero{{position:absolute;left:0;right:0;bottom:0;height:78mm;overflow:hidden;background:{CHAR}}}
.hero svg{{position:absolute;left:-6mm;width:222mm;bottom:0}}
/* reading page */
.head{{display:flex;justify-content:space-between;align-items:baseline;padding-top:1.6mm}}
.step{{display:grid;grid-template-columns:13mm 1fr;padding:3.4mm 0 3.6mm;border-top:.2mm solid {HAIR};align-items:start}}
.step:first-child{{border-top:none;padding-top:0}}
.step .n{{font-family:"Big Shoulders";font-weight:900;font-size:40pt;line-height:.72;color:{TXT}}}
.step p{{margin:0;line-height:1.5;font-weight:300;color:{TXT}}}
.panel{{background:{CHAR};border-radius:2.5mm;padding:4mm 4.5mm 4.5mm}}
.hear{{background:{CHAR};border-top:.5mm solid {LIME};padding:5mm 6mm 5mm;display:grid;grid-template-columns:26mm 1fr;column-gap:6mm;align-items:center}}
.hear .lab{{font-family:"Big Shoulders";font-weight:900;font-size:17pt;line-height:.84;color:{LIME}}}
.hear p{{margin:0;font-size:{13.4 if not ipad else 13}pt;line-height:1.35;font-weight:300;color:{TXT}}}
.cap{{font-size:{9 if not ipad else 9.6}pt;line-height:1.45;color:{TXT2};margin:2.5mm 0 0}}
.marg .sc{{margin:0 0 1.2mm;color:{TXT2}}} .marg p{{margin:0;font-size:{9.8 if not ipad else 10.4}pt;line-height:1.45;color:{TXT2}}}
.weathers{{display:grid;grid-template-columns:repeat(6,1fr);column-gap:3mm}}
.weathers .t{{font-weight:600;font-size:{8.8 if not ipad else 9}pt;letter-spacing:.04em;margin-top:1.4mm;color:{TXT}}} .weathers .d{{font-size:{8 if not ipad else 8.4}pt;color:{TXT2};line-height:1.3}}
.weathers svg{{display:block;width:100%;background:{CHAR};border-radius:1.4mm}}
.weathers .on svg{{box-shadow:inset 0 0 0 .45mm {LIME}}}
.knoblabels{{display:grid;grid-template-columns:repeat(4,1fr);text-align:center;font-size:{8.8 if not ipad else 9.2}pt;line-height:1.3;color:{TXT2}}} .knoblabels b{{color:{TXT}}}
.keylist{{font-size:{9 if not ipad else 9.8}pt;line-height:1.35;margin-top:2.5mm;color:{TXT2}}} .keylist b{{color:{TXT}}}
.keylist div{{display:grid;grid-template-columns:5mm 1fr;column-gap:2mm;align-items:baseline;margin-top:1.4mm}}
.keylist span.t{{display:inline-block;width:4.6mm;height:4.6mm;border-radius:50%;background:{LIME};color:{NIGHT};font-weight:600;font-size:7.6pt;text-align:center;line-height:4.6mm}}
/* ipad reflow */
.ipad .block{{margin-bottom:6mm}}
.ipad .weathers{{grid-template-columns:repeat(3,1fr);row-gap:4mm}}
.ipad .ihead{{display:flex;justify-content:space-between;border-top:.35mm solid {TXT};padding-top:1.6mm;margin-bottom:6mm}}
.ipad .step{{grid-template-columns:12mm 1fr;padding:3.6mm 0 3.8mm}}
.ipad .step .n{{font-size:36pt}}
.ipad .hear{{grid-template-columns:1fr;row-gap:2.5mm;padding:4.5mm 5mm 5mm}}
.ipad .marg{{display:grid;grid-template-columns:1fr;row-gap:5mm}}
.ipad .ifoot{{display:flex;justify-content:space-between;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;color:{TXT3}}}
{tail}
""")

# ------------------------------------------------------------------ opener
def rain_word(rain_img):
    return f"""<svg class="word" viewBox="0 0 210 120" preserveAspectRatio="xMidYMid slice">
  <defs><pattern id="rp" patternUnits="userSpaceOnUse" x="0" y="0" width="210" height="120"><image href="{rain_img}" x="0" y="-14" width="210" height="150" preserveAspectRatio="xMidYMid slice"/></pattern></defs>
  <g font-family="Big Shoulders" font-weight="900" font-size="78" letter-spacing="-.5">
    <text x="16" y="66" fill="url(#rp)">WEA</text><text x="16" y="66" fill="none" stroke="{TXT}" stroke-width=".3" opacity=".6">WEA</text>
    <text x="54" y="117" fill="url(#rp)">THER</text><text x="54" y="117" fill="none" stroke="{TXT}" stroke-width=".3" opacity=".6">THER</text>
  </g>
</svg>"""

def hero(shot):
    hw = C.fm1(viewbox="80 248 840 294", highlight=("GLO",), screen_img=shot, glow=LIME, body="#2a2a2f", label_font="Albert Sans")
    over = f"""<svg viewBox="80 248 840 294" style="position:absolute;left:-6mm;width:222mm;bottom:0;overflow:visible">
      <circle cx="828" cy="398" r="3.2" fill="{LIME}"/>
      <path d="M828,398 L828,372 L706,372" fill="none" stroke="{LIME}" stroke-width="1.4"/>
      <text x="700" y="376" font-family="Albert Sans" font-weight="600" font-size="12" fill="{LIME}" text-anchor="end">GLO<tspan font-weight="300" fill="{TXT}" font-size="10.5"> · tap it until the TEXTURE page shows</tspan></text>
    </svg>"""
    return f'<div class="hero">{hw}{over}</div>'

def page1(shot, rain):
    k = W.KICKER
    return f"""<section class="pg">
  {rain_word(rain)}
  <div class="kick sc lime">{k[0]} · {k[1]} · {k[2]}</div>
  <div class="title">{W.TITLE_B}</div>
  <p class="lead">{W.LEAD}</p>
  <div class="start"><div class="sc">{W.START_LABEL}</div>{W.START[0]}</div>
  {hero(shot)}
  <div class="foot" style="bottom:auto;top:9mm;justify-content:flex-end"><span class="n">18</span></div>
</section>"""

# ------------------------------------------------------------------ pieces
def screen_callouts(shot):
    return f"""<div class="knoblabels" style="margin-bottom:1mm"><div><b>KNOB1</b><br>SRC</div><div><b>KNOB2</b><br>LEVEL</div><div><b>KNOB3</b><br>TONE</div><div><b>KNOB4</b><br>MOVE</div></div>
    <div style="position:relative;padding-top:9mm">
      <img src="{shot}" alt="The TEXTURE page, VINYL source" style="width:100%;display:block;border-radius:2mm;box-shadow:0 0 0 .4mm {CHAR2}">
      <svg viewBox="0 0 500 80" style="display:block;width:100%;position:absolute;left:0;top:0;overflow:visible">
        <g stroke="{LIME}" stroke-width="3" fill="{LIME}">
          <line x1="70" y1="0" x2="70" y2="150"/><line x1="190" y1="0" x2="190" y2="150"/><line x1="310" y1="0" x2="310" y2="150"/><line x1="430" y1="0" x2="430" y2="150"/>
          <circle cx="70" cy="150" r="7"/><circle cx="190" cy="150" r="7"/><circle cx="310" cy="150" r="7"/><circle cx="430" cy="150" r="7"/>
        </g></svg>
    </div>"""

def hw_strip(shot):
    hw = C.fm1(viewbox="526 280 354 228", highlight=("GLO", "FX", "KNOB2"), screen_img=shot, glow=LIME, body="#2a2a2f", label_font="Albert Sans")
    hw = hw.replace('width="100%"', 'width="100%" style="display:block;border-radius:2mm"')
    def tag(x, y, n):
        return f'<circle cx="{x}" cy="{y}" r="11" fill="{LIME}"/><text x="{x}" y="{y+4.5}" font-family="Albert Sans" font-weight="600" font-size="13" fill="{NIGHT}" text-anchor="middle">{n}</text>'
    over = f"""<svg viewBox="526 280 354 228" style="position:absolute;inset:0;width:100%;height:100%;overflow:visible">
      {tag(870, 420, 1)}{tag(534, 420, 2)}{tag(676, 318, 3)}
      <line x1="859" y1="420" x2="851" y2="420" stroke="{LIME}" stroke-width="2"/>
      <line x1="545" y1="420" x2="553" y2="420" stroke="{LIME}" stroke-width="2"/>
      <line x1="665" y1="318" x2="668" y2="322" stroke="{LIME}" stroke-width="2"/>
    </svg>"""
    items = [("1", "<b>GLO</b>, tapped repeatedly until the TEXTURE page shows (step 1)"),
             ("2", "<b>FX</b>, held (step 4)"),
             ("3", "<b>KNOB2</b>, turned while FX is held: DUST (step 4)")]
    lst = "".join(f'<div><span class="t">{n}</span><span>{t}</span></div>' for n, t in items)
    return f'<div style="position:relative">{hw}{over}</div><div class="keylist">{lst}</div>'

def weather_icons():
    rnd = random.Random(9); out = []
    ink = TXT
    for name, what in W.SOURCES:
        g = [f'<svg viewBox="0 0 40 28">']
        s = f'stroke="{ink}" fill="none" stroke-linecap="round"'
        if name == "RAIN":
            for _ in range(26):
                x = 3 + rnd.random() * 34; y = 2 + rnd.random() * 18
                g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-1:.1f}" y2="{y+4:.1f}" {s} stroke-width=".9"/>')
            for _ in range(4):
                x = 6 + rnd.random() * 28; r = 1.5 + rnd.random() * 2
                g.append(f'<ellipse cx="{x:.1f}" cy="24" rx="{r*1.6:.1f}" ry="{r*.6:.1f}" {s} stroke-width=".7"/>')
        elif name == "VINYL":
            for r in range(3, 21, 3): g.append(f'<circle cx="20" cy="14" r="{r}" {s} stroke-width=".8"/>')
            for _ in range(10):
                a = rnd.random() * 6.28; r = 4 + rnd.random() * 15
                g.append(f'<circle cx="{20+r*math.cos(a):.1f}" cy="{14+r*math.sin(a):.1f}" r=".8" fill="{ink}"/>')
        elif name == "TAPE":
            for k in range(7):
                y = 4 + k * 3.3
                g.append(f'<path d="M3,{y} q9,{1.4*math.sin(k)} 17,0 t17,0" {s} stroke-width=".8"/>')
        elif name == "WIND":
            for k in range(4):
                y = 6 + k * 5.5
                g.append(f'<path d="M3,{y} c8,-6 12,6 20,0 s9,-3 14,-1" {s} stroke-width="1.1"/>')
        elif name == "RADIO":
            for k in range(30):
                x = 3 + k * 1.15; h = 2 + abs(math.sin(k * 1.9)) * 18 * (1 if rnd.random() < .5 else .35)
                g.append(f'<line x1="{x:.1f}" y1="{14-h/2:.1f}" x2="{x:.1f}" y2="{14+h/2:.1f}" {s} stroke-width=".9"/>')
        elif name == "ROOM":
            g.append(f'<rect x="4" y="4" width="32" height="20" rx="1" {s} stroke-width=".8"/>')
            g.append(f'<rect x="26" y="8" width="6" height="9" fill="{ink}" opacity=".22"/>')
            for _ in range(24):
                g.append(f'<circle cx="{5+rnd.random()*30:.1f}" cy="{5+rnd.random()*18:.1f}" r=".4" fill="{ink}" opacity=".6"/>')
        g.append("</svg>")
        out.append(f'<div class="{"on" if name=="RAIN" else ""}">{"".join(g)}<div class="t">{name}</div><div class="d">{what}</div></div>')
    return '<div class="weathers">' + "".join(out) + "</div>"

def steps_html():
    return "".join(f'<div class="step"><div class="n">{i+1}</div><p>{t}</p></div>' for i, t in enumerate(W.STEPS))

# ------------------------------------------------------------------ A4 reading page
def page2(shot):
    return f"""<section class="pg">
  <div class="m" style="top:13mm">
    <div class="rule"></div>
    <div class="head"><span class="sc" style="color:{TXT}">Weather · the TEXTURE page</span><span class="sc">GLO · page 7 of 8</span></div>
  </div>
  <div class="m" style="top:24mm">
    <div class="grid">
      <div style="grid-column:1/5">{steps_html()}
        <div style="margin-top:4mm">
          <div class="sc" style="margin-bottom:2mm">The six weathers, as step 2 lists them</div>
          {weather_icons()}
        </div>
      </div>
      <div style="grid-column:5/7">
        {screen_callouts(shot)}
        <p class="cap">{W.SHOT_CAP}</p>
        <div class="panel" style="margin-top:5mm">
          <div class="sc" style="margin-bottom:2.5mm">On the FM-1</div>
          {hw_strip(shot)}
        </div>
      </div>
    </div>
    <div class="hear" style="margin-top:9mm"><div class="lab">YOU SHOULD<br>NOW BE<br>HEARING</div><p>{W.HEAR}</p></div>
    <div class="grid marg" style="margin-top:6mm">
      <div style="grid-column:1/4"><div class="sc">{W.TRY_LABEL}</div><p>{W.TRY}</p></div>
      <div style="grid-column:4/7"><div class="sc">{W.MESS_LABEL}</div><p>{W.MESS}</p></div>
    </div>
  </div>
  <div class="foot"><span>SLOOP, Gently · Lesson four</span><span class="n">19</span></div>
</section>"""

# ------------------------------------------------------------------ iPad mini reflow of the reading page
def ipad_page(shot):
    head = f'<div class="ihead"><span class="sc" style="color:{TXT}">Weather · the TEXTURE page</span><span class="sc">GLO · 7 of 8</span></div>'
    foot = lambda n: f'<div class="ifoot" style="position:absolute;left:9mm;right:9mm;bottom:7mm"><span>SLOOP, Gently · Lesson four</span><span>iPad mini · {n}</span></div>'
    p1 = f'<section class="pg ipad">{head}<div class="block">{steps_html()}</div>{foot(1)}</section>'
    p2 = f'<section class="pg ipad">{head}<div class="block"><div class="sc" style="margin-bottom:3mm">The six weathers, as step 2 lists them</div>{weather_icons()}</div>{foot(2)}</section>'
    p3 = (f'<section class="pg ipad">{head}<div class="block" style="width:62%;margin:0 auto 2mm">{screen_callouts(shot)}</div><p class="cap" style="margin:0 0 7mm">{W.SHOT_CAP}</p>'
          f'<div class="block hear"><div class="lab">YOU SHOULD NOW BE HEARING</div><p>{W.HEAR}</p></div>{foot(3)}</section>')
    p4 = (f'<section class="pg ipad">{head}<div class="block panel"><div class="sc" style="margin-bottom:2.5mm">On the FM-1</div>{hw_strip(shot)}</div>'
          f'<div class="block marg"><div><div class="sc">{W.TRY_LABEL}</div><p>{W.TRY}</p></div><div><div class="sc">{W.MESS_LABEL}</div><p>{W.MESS}</p></div></div>{foot(4)}</section>')
    return p1 + p2 + p3 + p4

def html_a4():
    shot = C.img_uri("texture-page.png")
    rain = C.texture_image("rain", 1400, 1000, seed=7, tint=(52, 60, 80), fg=(242, 238, 226))
    return C.glyphs(f"<!doctype html><html><head><meta charset='utf-8'><title>Concept D dark</title><style>{css()}</style></head><body>{page1(shot, rain)}{page2(shot)}</body></html>")

def html_ipad():
    shot = C.img_uri("texture-page.png")
    return C.glyphs(f"<!doctype html><html><head><meta charset='utf-8'><title>Concept D dark iPad</title><style>{css(ipad=True)}</style></head><body>{ipad_page(shot)}</body></html>")

if __name__ == "__main__":
    C.render(html_a4(), os.path.join(C.HERE, "out", "concept_d_dark_a4.pdf"), "concept_d_dark_a4")
    C.render(html_ipad(), os.path.join(C.HERE, "out", "concept_d_dark_ipad.pdf"), "concept_d_dark_ipad")
    print("ok")
