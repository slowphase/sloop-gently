#!/usr/bin/env python3
"""Measure each A4 .page for overflow (content taller than the page box minus bottom padding)."""
import sys, json
from playwright.sync_api import sync_playwright
path = sys.argv[1] if len(sys.argv) > 1 else "out/SLOOP-Gently-A4.html"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1400})
    import os; pg.goto("file://" + os.path.abspath(path))
    pg.wait_for_timeout(500)
    res = pg.evaluate("""() => [...document.querySelectorAll('.page')].map((el,i)=>{
        const cs=getComputedStyle(el); const padB=parseFloat(cs.paddingBottom); const padT=parseFloat(cs.paddingTop);
        const inner=el.clientHeight-padT-padB;  // available content height
        let bottom=0;
        for(const c of el.children){ if(c.classList.contains('runhead')||c.classList.contains('folio')||c.classList.contains('art')||c.classList.contains('field')) continue;
            const r=c.getBoundingClientRect(); const pr=el.getBoundingClientRect(); bottom=Math.max(bottom, r.bottom-pr.top-padT); }
        const id=(el.id||'')||(el.querySelector('h1,h2')?.textContent||'').slice(0,40);
        return {n:i+1,id, used:Math.round(bottom), avail:Math.round(inner), over:Math.round(bottom-inner)};
    })""")
    b.close()
over = [r for r in res if r["over"] > -8]
print(f"{len(res)} pages; {len([r for r in res if r['over']>0])} overflow, {len([r for r in res if -8<r['over']<=0])} tight")
for r in res:
    flag = "OVER" if r["over"] > 0 else ("tight" if r["over"] > -8 else "")
    print(f"{r['n']:>3} {flag:5} used {r['used']:>4} / {r['avail']:>4}  {r['id']}")
