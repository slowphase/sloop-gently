"""Illustrated edition: place one explanatory graphic in each lesson that benefits, around the verified text.
Works on the list of <section> strings produced by build.py. Text is never rewritten; sections are split where a page needs room."""
import re
import illus as L, interior as I, diagrams as D

S_IPAD = 1.32

def fig(a4_svg, ipad_svg=None, style="", caption=None):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    ipad_svg = ipad_svg or L.scale_fonts(a4_svg, S_IPAD)
    return (f'<figure style="{style}"><div class="a4-only">{a4_svg}</div>'
            f'<div class="ipad-only">{ipad_svg}</div>{cap}</figure>')

def fig_S(fn, style="", caption=None, **kw):
    """for illus functions that take S: draw twice"""
    return fig(fn(S=1.0, **kw), fn(S=S_IPAD, **kw), style, caption)

def after(sec, marker, html, nth=1):
    """insert html after the nth occurrence of marker's closing element (marker is an opening tag prefix)"""
    idx = -1
    for _ in range(nth):
        idx = sec.index(marker, idx + 1)
    # find the end of the element: for <p …> take the next </p>; for headings next </hN>; for ol next </ol>; for div class=start next '</div>\n  </div>' approx
    tag = re.match(r'<([a-z0-9]+)', marker).group(1)
    close = f"</{tag}>"
    if tag == "div":
        # walk to the matching close
        depth = 0; i = idx
        while True:
            m = re.compile(r'<div\b|</div>').search(sec, i)
            if m.group(0) == "</div>":
                depth -= 1
                if depth == 0:
                    end = m.end(); break
            else:
                depth += 1
            i = m.end()
    else:
        end = sec.index(close, idx) + len(close)
    return sec[:end] + "\n" + html + "\n" + sec[end:]

def before(sec, marker, html, nth=1):
    idx = -1
    for _ in range(nth):
        idx = sec.index(marker, idx + 1)
    return sec[:idx] + html + "\n" + sec[idx:]

def split_at(sec, marker, new_head, extra_class=""):
    """cut a section into two at marker; the second gets the same section attributes plus new_head"""
    head = re.match(r'<section[^>]*>', sec).group(0)
    if extra_class:
        head = head.replace('class="page', f'class="page {extra_class}', 1)
    idx = sec.index(marker)
    first = sec[:idx].rstrip() + "\n</section>\n"
    second = head + "\n" + new_head + "\n" + sec[idx:]
    return first, second

def apply(secs):
    out = []
    for sec in secs:
        # ---------- ch1: four tracks, one playhead
        if 'id="ch1"' in sec:
            m = re.search(r'<svg class="tracks-bars".*?</svg>', sec, flags=re.S)
            if m:
                sec = sec.replace(m.group(0), fig_S(L.tracks_loop, "margin:3mm 0 1mm;"))
        # ---------- ch2 install: the flow, after the lead
        elif 'id="ch2"' in sec:
            sec = after(sec, '<p class="lead">', fig_S(L.install_flow, "margin:2mm 0 2mm;"))
        # ---------- ch2 recovery: the map
        elif 'If things go wrong: the complete recovery kit' in sec:
            sec = after(sec, '<p>Read this page once now', fig_S(L.recovery_flow, "margin:1mm auto 2mm;width:126mm;"))
            sec = sec.replace('<h3>SLOOP will not start</h3>', '<div class="row c-1-1"><div><h3>SLOOP will not start</h3>')
            sec = sec.replace('<h3>Going back to the official firmware</h3>', '</div><div><h3 style="margin-top:0;">Going back to the official firmware</h3>')
            sec = sec.replace('<div class="careful"><div class="label">Odd settings after going back?</div>', '</div></div>\n<div class="careful"><div class="label">Odd settings after going back?</div>')
        # ---------- ch3 second page: keys → tiles
        elif 'Tap, hold, and the seven layers' in sec:
            sec = after(sec, '<h2 style="margin-top:0;">Tap, hold', fig_S(L.tiles_map, "margin:2mm 0 4mm;"))
        # ---------- L1 first page: the sound bank
        elif 'id="l1"' in sec:
            sec = after(sec, '<ol class="steps">', fig_S(L.soundbank_ribbon, "margin:2mm 0 3mm;"))
        # ---------- L2 second page: the LFO over four bars
        elif 'The LFO: movement you do not have to play' in sec:
            sec = after(sec, '<h2 style="margin-top:0;">The LFO', fig_S(L.lfo_bars, "margin:1mm 0 3mm;"))
        # ---------- L3 second page: overdub passes
        elif 'Prefer a count&#8209;in? There is one' in sec:
            sec = after(sec, '<h2>Layering: the overdub</h2>', fig_S(L.overdub_stack, "margin:1mm 0 2mm;"))
        # ---------- L5 first page: the chord keys
        elif 'id="l5"' in sec:
            sec = after(sec, '<div class="start">', fig_S(L.chord_keys, "margin:0 0 2mm;width:162mm;"))
        # ---------- L5 second page: CHORD+ drawn on the keys (replaces the five-row table that listed the same five facts)
        elif 'Optional exploration: CHORD+' in sec:
            m = re.search(r'<table style="max-width:120mm;">.*?</table>', sec, flags=re.S)
            sec = sec.replace(m.group(0), fig_S(L.chordplus_keys, "margin:1mm 0 2mm;"))
        # ---------- L6 first page: dynamics and kits, after the two steps
        elif 'id="l6"' in sec:
            sec = after(sec, '<ol class="steps">', fig_S(L.drum_dynamics, "margin:4mm 0 2mm;"))
        # ---------- L7: the four-note step, with the melody section moved to a page of its own
        elif 'id="l7"' in sec:
            # the "take the simple path" steps move to the next page, under the four-note figure, above Mixing
            i2 = sec.index('<ol class="steps">', sec.index('<ul class="plain">'))
            j2 = sec.index('</ol>', i2) + len('</ol>')
            apply.l7_steps = sec[i2:j2]
            sec = sec[:i2] + sec[j2:]
        elif 'Mixing: the GLO layer is your desk' in sec:
            steps = getattr(apply, "l7_steps", "")
            sec = sec.replace('<section class="page"', '<section class="page dense trk0" data-head="track 2, then the whole mix"', 1)
            sec = sec.replace('<h2 style="margin-top:0;">Mixing: the GLO layer is your desk</h2>',
                              '<div class="kicker"><span class="chno">L7</span><span>Lesson seven · continued</span></div>'
                              '<h2 style="margin-top:0;">Sharing track 2: a step holds four notes</h2>'
                              + fig_S(L.four_note_step, "margin:1mm auto 1.5mm;width:136mm;") + steps.replace('<ol class="steps">', '<ol class="steps two">', 1) +
                              '<h2>Mixing: the GLO layer is your desk</h2>', 1)
        # ---------- L8 first page: 64 steps, four pages
        elif 'id="l8"' in sec:
            m = re.search(r'<h3>The SEQ layer: the same grid, anywhere</h3>.*?(?=</div>\s*<div>\s*<figure class="shot")', sec, flags=re.S)
            seq_html = m.group(0)
            sec = sec.replace(seq_html, "")
            sec = after(sec, '<div class="row c-3-2">', fig_S(L.step_pages, "margin:2mm auto 3mm;width:150mm;") + seq_html)
        # ---------- L9 first page: momentary effects; the knob paragraphs move to the fills page
        elif 'id="l9"' in sec:
            sec = after(sec, '<div class="start">', fig_S(L.punch_timeline, "margin:0 0 3mm;"))
            m = re.search(r'<h3>The knobs while FX is held</h3>.*?(?=</div>\s*<div>\s*<figure class="shot")', sec, flags=re.S)
            knobs_html = m.group(0)
            sec = sec.replace(knobs_html, "")
            apply.carry = knobs_html
        elif 'Fills: a one&#8209;finger' in sec:
            carry = getattr(apply, "carry", "")
            sec = sec.replace('<h2 style="margin-top:0;">Fills', '<div class="row c-1-1" style="margin-bottom:3mm;"><div>' + carry.replace('<h3>The knobs while FX is held</h3>', '<h2 style="margin-top:0;">The knobs while FX is held</h2>', 1) + '</div><div>' + '<h2 style="margin-top:0;">Fills', 1)
            # fill strip after the four-move aside; then split: hear/try/mess/gb go to a third page
            sec = after(sec, '<div class="aside"><div class="label">Make one fill audible', '</div></div>' + fig_S(L.fill_strip, "margin:3mm 0 2mm;"))
            a, b = split_at(sec, '<div class="hear">', '<div class="kicker"><span class="chno">L9</span><span>Lesson nine · continued</span></div>\n<h1 style="font-size:1.9em;">Everything a punch-in does, and nothing it keeps</h1>')
            out.append(a); sec = b
        # ---------- L10 first page: sections on the bar
        elif 'id="l10"' in sec:
            sec = after(sec, '<div class="start">', fig_S(L.section_timeline, "margin:0 0 3mm;"))
        # ---------- ch14: two pages, two maps
        elif 'id="ch14"' in sec:
            sec = after(sec, '<p class="lead">', fig_S(L.editor_map, "margin:2mm 0 3mm;"))
            a, b = split_at(sec, '<div class="gb"><div class="label">Recording into GarageBand, step by step</div>',
                            '<div class="kicker"><span class="chno">14</span><span>Chapter fourteen · continued</span></div>\n<h1 style="font-size:1.9em;">Recording into GarageBand</h1>' + fig_S(L.audio_path, "margin:2mm 0 4mm;"))
            # the delights + mess stay with page one; move them back
            m = re.search(r'<div class="aside"><div class="label">Three small delights</div>.*?</div>\s*<div class="mess">.*?</div>\s*</section>', b, flags=re.S)
            tail = m.group(0)
            b = b.replace(tail, "</section>")
            a = a.replace("</section>", tail)
            b = b.replace('<div class="gb"><div class="label">Recording into GarageBand, step by step</div>', '<div class="gb" style="max-width:150mm;"><div class="label">Recording into GarageBand, step by step</div>')
            out.append(a); sec = b
        out.append(sec)
    return out
