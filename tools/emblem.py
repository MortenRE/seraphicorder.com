"""Generates the Seraphic Order emblem, favicon and celestial diagram SVGs,
and inlines the emblem symbols into index.html.

    python tools/emblem.py

Raster icons (favicon.ico, apple-touch-icon.png, icon-*.png, og.jpg) were rendered
from these SVGs with a headless browser and Pillow; regenerate them if the emblem changes.
"""
import math, os, re, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')
C = 100.0

def pol(r, deg):
    a = math.radians(deg - 90)
    return (C + r*math.cos(a), C + r*math.sin(a))

def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')

def ticks(r0, r1, step, skip_every=None, sw=0.5):
    d = []
    n = int(360/step)
    for i in range(n):
        if skip_every and i % skip_every == 0: continue
        x0,y0 = pol(r0, i*step); x1,y1 = pol(r1, i*step)
        d.append(f"M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}")
    return f'<path d="{"".join(d)}" stroke-width="{sw}"/>'

def star4(cx, cy, s):
    k = s*0.28
    return (f'<path d="M{f(cx)} {f(cy-s)}Q{f(cx+k)} {f(cy-k)} {f(cx+s)} {f(cy)}'
            f'Q{f(cx+k)} {f(cy+k)} {f(cx)} {f(cy+s)}Q{f(cx-k)} {f(cy+k)} {f(cx-s)} {f(cy)}'
            f'Q{f(cx-k)} {f(cy-k)} {f(cx)} {f(cy-s)}Z" fill="currentColor" stroke="none"/>')

def wing(angle, tip=60, width=11.5):
    """A feathered wing/petal pointing up, rotated into place."""
    g = []
    g.append(f'<path d="M100 100C{f(100-width)} {f(100-tip*0.36)} {f(100-width)} {f(100-tip*0.74)} 100 {f(100-tip)}'
             f'C{f(100+width)} {f(100-tip*0.74)} {f(100+width)} {f(100-tip*0.36)} 100 100Z" stroke-width="0.9"/>')
    g.append(f'<path d="M100 {f(100-tip*0.14)}L100 {f(100-tip*0.9)}" stroke-width="0.5"/>')
    barbs = []
    for k in range(7):
        t = 0.24 + k*0.1
        y = 100 - tip*t
        hw = 0.62*width*(math.sin(math.pi*t)**0.85)
        for s in (-1, 1):
            barbs.append(f"M100 {f(y)}L{f(100+s*hw)} {f(y-hw*0.75)}")
    g.append(f'<path d="{"".join(barbs)}" stroke-width="0.38"/>')
    return f'<g transform="rotate({angle} 100 100)">{"".join(g)}</g>'

def mark_inner():
    p = []
    p.append('<circle cx="100" cy="100" r="72" stroke-width="0.9"/>')
    p.append('<circle cx="100" cy="100" r="69.5" stroke-width="0.45"/>')
    for a in range(0, 360, 60):
        p.append(wing(a))
    for a in range(30, 360, 60):
        x,y = pol(52, a); p.append(star4(x, y, 3.2))
    p.append(ticks(69.5, 72, 10, sw=0.4))
    p.append('<circle cx="100" cy="100" r="8.5" fill="var(--emblem-bg, #0b0908)" stroke-width="0.9"/>')
    p.append('<circle cx="100" cy="100" r="5.5" stroke-width="0.45"/>')
    p.append('<circle cx="100" cy="100" r="1.7" fill="currentColor" stroke="none"/>')
    return "".join(p)

def mark_outer():
    p = []
    p.append('<circle cx="100" cy="100" r="97" stroke-width="1"/>')
    p.append('<circle cx="100" cy="100" r="92" stroke-width="0.5"/>')
    p.append(ticks(92.6, 96.4, 5, skip_every=6, sw=0.45))
    p.append(ticks(91, 97, 30, sw=0.8))
    return "".join(p)

def ring_text(font="'Cormorant Garamond', Cormorant, Georgia, serif"):
    # top arc runs clockwise (left -> right over the top); glyphs grow outward from r=79.5
    top = f'<path id="so-arc-top" d="M{f(C-79.5)} 100A79.5 79.5 0 0 1 {f(C+79.5)} 100" fill="none" stroke="none"/>'
    # bottom arc runs counter-clockwise (left -> right under the bottom); glyphs grow inward from r=86.5
    bot = f'<path id="so-arc-bot" d="M{f(C-86.5)} 100A86.5 86.5 0 0 0 {f(C+86.5)} 100" fill="none" stroke="none"/>'
    style = f'font-family="{font}" font-size="10.2" font-weight="500" letter-spacing="2.2" fill="currentColor" stroke="none"'
    t1 = f'<text {style}><textPath href="#so-arc-top" startOffset="50%" text-anchor="middle">SERAPHIC ORDER</textPath></text>'
    t2 = f'<text {style}><textPath href="#so-arc-bot" startOffset="50%" text-anchor="middle">DIGITAL CREATIONS</textPath></text>'
    lz = ''.join(f'<path transform="translate({f(x)} {f(y)})" d="M0 -3L2 0L0 3L-2 0Z" fill="currentColor" stroke="none"/>' for x,y in (pol(82,90), pol(82,270)))
    return top+bot+t1+t2+lz

base = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"'

seal = f'<g {base}>{mark_outer()}{ring_text()}{mark_inner()}</g>'
mark = f'<g {base}>{mark_outer()}<g transform="translate(100 100) scale(1.2) translate(-100 -100)">{mark_inner()}</g></g>'

def svg(body, size=None, extra=''):
    s = f' width="{size}" height="{size}"' if size else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"{s}{extra}>{body}</svg>'

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'seal.svg'), 'w', encoding='utf-8') as fh:
    fh.write(svg(seal, extra=' color="#c8a662"'))
with open(os.path.join(OUT, 'emblem.svg'), 'w', encoding='utf-8') as fh:
    fh.write(svg(mark, extra=' color="#c8a662"'))

# favicon: dark disc, bolder strokes
fav_inner = mark
for a, b in (('stroke-width="0.38"','stroke-width="1"'), ('stroke-width="0.4"','stroke-width="1.1"'),
             ('stroke-width="0.45"','stroke-width="1.1"'), ('stroke-width="0.5"','stroke-width="1.3"'),
             ('stroke-width="0.8"','stroke-width="1.6"'), ('stroke-width="0.9"','stroke-width="1.7"'),
             ('stroke-width="1"/>','stroke-width="1.8"/>')):
    fav_inner = fav_inner.replace(a, b)
fav = f'<circle cx="100" cy="100" r="100" fill="#0e0b09"/>{fav_inner}'
with open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8') as fh:  # served from the site root
    fh.write(svg(fav, extra=' color="#d4b36f"'))


symbols = ('<svg aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">\n'
             '  <defs>\n'
             '    <linearGradient id="grad-rule" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity="0"/><stop offset=".5" stop-color="currentColor"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient>\n'
             '  </defs>\n'
             f'  <symbol id="sym-seal" viewBox="0 0 200 200">{seal}</symbol>\n'
             f'  <symbol id="sym-mark" viewBox="0 0 200 200">{mark}</symbol>\n</svg>\n')

# Celestial diagram, viewBox 0 0 1000 1000
cc = 500.0
def cpol(r, deg):
    a = math.radians(deg-90); return (cc + r*math.cos(a), cc + r*math.sin(a))
def cticks(r0, r1, step, sw):
    d=[]
    for i in range(int(360/step)):
        x0,y0=cpol(r0,i*step); x1,y1=cpol(r1,i*step); d.append(f"M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}")
    return f'<path d="{"".join(d)}" stroke-width="{sw}"/>'
cel = ['<g fill="none" stroke="currentColor" stroke-linecap="round">']
cel.append('<circle cx="500" cy="500" r="498" stroke-width="0.8"/>')
cel.append('<circle cx="500" cy="500" r="486" stroke-width="0.5"/>')
cel.append(cticks(487, 497, 2, 0.35))
cel.append(cticks(482, 498, 10, 0.7))
cel.append(cticks(470, 498, 30, 1))
cel.append('<circle cx="500" cy="500" r="440" stroke-width="0.5" stroke-dasharray="1 6"/>')
cel.append('<circle cx="500" cy="500" r="372" stroke-width="0.6"/>')
cel.append('<circle cx="500" cy="500" r="366" stroke-width="0.4"/>')
d=[]
for i in range(12):
    x0,y0=cpol(372,i*30); x1,y1=cpol(440,i*30); d.append(f"M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}")
cel.append(f'<path d="{"".join(d)}" stroke-width="0.5"/>')
cel.append('<circle cx="500" cy="500" r="300" stroke-width="0.5" stroke-dasharray="2 4"/>')
cel.append('<circle cx="500" cy="500" r="214" stroke-width="0.5"/>')
cel.append('<circle cx="500" cy="500" r="120" stroke-width="0.5" stroke-dasharray="1 5"/>')
cel.append('<ellipse cx="500" cy="500" rx="372" ry="150" stroke-width="0.7" transform="rotate(-23.5 500 500)"/>')
cel.append('<ellipse cx="500" cy="500" rx="214" ry="86" stroke-width="0.45" transform="rotate(-23.5 500 500)" stroke-dasharray="3 5"/>')
cel.append('<path d="M500 2V998M2 500H998" stroke-width="0.35"/>')
for r,ang,pr in ((300, 52, 4.5),(214, 203, 3.2),(440, 311, 3.8),(120, 140, 2.6)):
    x,y=cpol(r,ang); cel.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{pr}" stroke-width="0.8"/><circle cx="{f(x)}" cy="{f(y)}" r="{pr+6}" stroke-width="0.35"/>')
random.seed(7)
pts=[]
for i in range(26):
    r=random.uniform(130,470); a=random.uniform(0,360); x,y=cpol(r,a); s=random.choice((2.2,2.8,3.6))
    pts.append(f'M{f(x-s)} {f(y)}H{f(x+s)}M{f(x)} {f(y-s)}V{f(y+s)}')
cel.append(f'<path d="{"".join(pts)}" stroke-width="0.6"/>')
cel.append('</g>')
with open(os.path.join(OUT, 'celestial.svg'), 'w', encoding='utf-8') as fh:
    fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" color="#c8a662">'+''.join(cel)+'</svg>')
print("svg ok")
