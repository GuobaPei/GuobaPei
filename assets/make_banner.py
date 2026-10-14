#!/usr/bin/env python3
"""Build banner-light.svg and banner-dark.svg next to this file.

Same comic look as guobapei.github.io. All text is converted to outlines,
because an SVG shown as an <img> (which is how GitHub shows it) cannot load
web fonts; outlines look identical on every machine.

ponytail: macOS system font paths; point the three face() calls elsewhere to
run it on another OS.
"""
import math
import os
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
SUP = '/System/Library/Fonts/Supplemental/'


def face(path, want=None):
    if not path.endswith('.ttc'):
        return TTFont(path)
    for f in TTCollection(path).fonts:
        if f['name'].getDebugName(4) == want:
            return f
    raise SystemExit(f'no face {want!r} in {path}')


IMPACT = face(SUP + 'Impact.ttf')                   # the favicon's font on the homepage
CHALK = face(SUP + 'ChalkboardSE.ttc', 'Chalkboard SE Bold')
HIRA = face('/System/Library/Fonts/Hiragino Sans GB.ttc', 'Hiragino Sans GB W6')

NAME = 'JIEYUAN PEI'
CN = '裴杰远'
SAY_PRE, SAY_HL, SAY_POST = 'I build ', 'physical intelligence you can trust outside the lab', '.'
BURST = [('INCOMING', 23), ('HKUST (GZ)', 40), ('MPhil · 2027', 25)]
BURST_DY = (-30, 14, 50)              # baselines relative to the burst centre
TAGS = [('AI FOR SCIENCE', 'blue'), ('AUTONOMOUS DRIVING', 'red'), ('MULTIMODAL MODELS', 'green')]

THEMES = {
    'light': dict(panel='#fffdf7', ink='#16161a', mute='#6d6860', edge='#16161a', on='#fff',
                  mark='#ffd23f', yellow='#ffd23f', red='#e4372e', blue='#2f6be0', green='#12a05c'),
    # dark accents are light, so text on them is dark; shadows and outlines stay black
    'dark': dict(panel='#1e2027', ink='#efe9dc', mute='#a19c92', edge='#000', on='#16161a',
                 mark='rgba(255,221,107,.3)', yellow='#ffdd6b', red='#ff6a58', blue='#6d9bff',
                 green='#37cd85'),
}


def advance(font, s, size, track=0):
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    k = size / font['head'].unitsPerEm
    return sum(gs[cmap[ord(c)]].width * k for c in s) + track * (len(s) - 1)


def outline(font, s, size, x, y, track=0, middle=False):
    """Path data for `s`, baseline at y, starting (or centred, with middle) at x."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    k = size / font['head'].unitsPerEm
    if middle:
        x -= advance(font, s, size, track) / 2
    pen = SVGPathPen(gs, ntos=lambda n: ('%.1f' % n).rstrip('0').rstrip('.'))
    for c in s:
        g = gs[cmap[ord(c)]]
        g.draw(TransformPen(pen, (k, 0, 0, -k, x, y)))
        x += g.width * k + track
    return pen.getCommands()


def star(cx, cy, R, r, n=16):
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n - math.pi / 2
        rad = R if i % 2 == 0 else r
        pts.append(f'{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}')
    return ' '.join(pts)


def build(t):
    W, H = 1200, 430
    px, py, pw, ph = 22, 22, 1140, 372                 # the comic panel
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
           f'aria-labelledby="t"><title id="t">Jieyuan Pei (裴杰远) — I build physical '
           f'intelligence you can trust outside the lab. AI for Science, Autonomous Driving, '
           f'Multimodal Models. Incoming MPhil student at HKUST (Guangzhou), 2027.</title>',
           # transform-only motion, never opacity, and every first frame fits the panel:
           # some renderers show an <img> SVG frozen at t=0 (seen in a browser pane)
           '<style>'
           '.stamp{transform-box:fill-box;transform-origin:center;'
           'animation:stamp .62s cubic-bezier(.2,.9,.3,1.15) both}'
           '@keyframes stamp{0%{transform:scale(1.08) rotate(-2.5deg)}55%{transform:scale(.98) '
           'rotate(.8deg)}100%{transform:none}}'
           '.wob{transform-box:fill-box;transform-origin:center;animation:wob 2.8s ease-in-out infinite}'
           '@keyframes wob{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg) scale(1.05)}}'
           '.rise{animation:rise .55s cubic-bezier(.2,.85,.25,1) both}'
           '@keyframes rise{from{transform:translateY(-10px)}to{transform:none}}'
           '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
           '</style>',
           f'<defs><pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">'
           f'<circle cx="6" cy="6" r="1.3" fill="{t["blue"]}" opacity=".16"/></pattern></defs>',
           f'<rect x="{px + 12}" y="{py + 12}" width="{pw}" height="{ph}" fill="{t["edge"]}"/>',
           f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{t["panel"]}"/>',
           f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#dots)" '
           f'stroke="{t["ink"]}" stroke-width="6"/>']

    # name: yellow, black outline, red offset -- the homepage h1
    size, x0, base = 138, 64, 170
    d = outline(IMPACT, NAME, size, x0, base, track=4)
    out.append('<g transform="rotate(-2 400 120)"><g class="stamp">'
               f'<path d="{d}" fill="{t["red"]}" transform="translate(9 9)"/>'
               f'<path d="{d}" fill="{t["yellow"]}" stroke="{t["edge"]}" stroke-width="11" '
               'stroke-linejoin="round" paint-order="stroke"/></g></g>')

    out.append(f'<path d="{outline(HIRA, CN, 40, 70, 232, track=24)}" fill="{t["mute"]}"/>')

    # speech bubble, tail pointing up at the name
    fs, bx, by = 25, 64, 262
    w_pre, w_hl = advance(CHALK, SAY_PRE, fs), advance(CHALK, SAY_HL, fs)
    bw = 28 + advance(CHALK, SAY_PRE + SAY_HL + SAY_POST, fs) + 28
    tx, ty = bx + 28, by + 41
    out += [f'<rect x="{bx}" y="{by}" width="{bw:.0f}" height="62" rx="26" fill="{t["panel"]}" '
            f'stroke="{t["ink"]}" stroke-width="4"/>',
            f'<path d="M{bx + 44} {by + 2}L{bx + 30} {by - 22}L{bx + 76} {by + 2}" '
            f'fill="{t["panel"]}" stroke="{t["ink"]}" stroke-width="4" stroke-linejoin="round"/>',
            f'<rect x="{bx + 44}" y="{by + 1}" width="30" height="5" fill="{t["panel"]}"/>',
            f'<rect x="{tx + w_pre:.1f}" y="{ty - 9}" width="{w_hl:.1f}" height="12" fill="{t["mark"]}"/>',
            f'<path d="{outline(CHALK, SAY_PRE + SAY_HL + SAY_POST, fs, tx, ty)}" fill="{t["ink"]}"/>']

    # research threads as tags
    x, y, fs = 64, 352, 23
    for i, (label, c) in enumerate(TAGS):
        w = advance(IMPACT, label, fs, 1.5) + 30
        out.append(f'<g class="rise" style="animation-delay:{.15 + i * .08:.2f}s">'
                   f'<rect x="{x + 5}" y="{y + 5}" width="{w:.0f}" height="38" fill="{t["edge"]}"/>'
                   f'<rect x="{x}" y="{y}" width="{w:.0f}" height="38" fill="{t[c]}" '
                   f'stroke="{t["ink"]}" stroke-width="3.5"/>'
                   f'<path d="{outline(IMPACT, label, fs, x + 15, y + 28, 1.5)}" fill="{t["on"]}"/></g>')
        x += w + 18

    # starburst: next stop, HKUST (GZ)
    cx, cy = 1004, 206
    lines = ''.join(f'<path d="{outline(IMPACT, s, fz, cx, cy + dy, 1, middle=True)}" fill="{t["on"]}"/>'
                    for (s, fz), dy in zip(BURST, BURST_DY))
    out.append(f'<g transform="rotate(8 {cx} {cy})"><g class="wob">'
               f'<polygon points="{star(cx + 8, cy + 8, 136, 104)}" fill="{t["edge"]}"/>'
               f'<polygon points="{star(cx, cy, 136, 104)}" fill="{t["red"]}" stroke="{t["ink"]}" '
               f'stroke-width="5" stroke-linejoin="round"/>{lines}</g></g>')

    out.append('</svg>')
    return ''.join(out)


if __name__ == '__main__':
    for name, t in THEMES.items():
        p = os.path.join(HERE, f'banner-{name}.svg')
        open(p, 'w', encoding='utf-8').write(build(t))
        print(p, os.path.getsize(p) // 1024, 'KB')
    # layout check: the name and the bubble must not run into the starburst
    name_right = 64 + advance(IMPACT, NAME, 138, 4)
    bubble_right = 64 + 56 + advance(CHALK, SAY_PRE + SAY_HL + SAY_POST, 25)
    assert name_right < 1004 - 136 and bubble_right < 1004 - 136, (name_right, bubble_right)
    print(f'name ends at x={name_right:.0f}, bubble at x={bubble_right:.0f}, burst starts at x={1004 - 136}')
    # burst text must stay inside the inner radius (104) of the star
    for (s, fz), dy in zip(BURST, BURST_DY):
        reach = math.hypot(advance(IMPACT, s, fz, 1) / 2, max(abs(dy - .75 * fz), abs(dy)))
        assert reach < 104, (s, round(reach))
        print(f'burst line {s!r} reaches r={reach:.0f} of 104')
