#!/usr/bin/env python3
"""Pasang ikon Udin ke project Android hasil `npx cap add android`.
Jalankan dari root project: python3 scripts/apply-icon.py
Butuh: pip install pillow
"""
import os, sys
from PIL import Image, ImageDraw

RES = os.path.join('android', 'app', 'src', 'main', 'res')
if not os.path.isdir(RES):
    sys.exit("Folder android/ belum ada. Jalankan dulu: npx cap add android")

src_full = Image.open('resources/icon-only.png').convert('RGBA')
src_fg   = Image.open('resources/icon-foreground.png').convert('RGBA')

# ukuran launcher klasik & foreground adaptive (108dp) per kepadatan layar
LAUNCHER = {'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}
ADAPTIVE = {'mdpi':108,'hdpi':162,'xhdpi':216,'xxhdpi':324,'xxxhdpi':432}

def round_mask(sz):
    m = Image.new('L',(sz*4,sz*4),0)
    ImageDraw.Draw(m).ellipse((0,0,sz*4-1,sz*4-1),fill=255)
    return m.resize((sz,sz),Image.LANCZOS)

for d in LAUNCHER:
    folder = os.path.join(RES, f'mipmap-{d}')
    os.makedirs(folder, exist_ok=True)
    s = LAUNCHER[d]
    sq = src_full.resize((s,s), Image.NEAREST)          # NEAREST = pixel art tetap tajam
    sq.save(os.path.join(folder,'ic_launcher.png'))
    rd = sq.copy(); rd.putalpha(round_mask(s))
    rd.save(os.path.join(folder,'ic_launcher_round.png'))
    a = ADAPTIVE[d]
    src_fg.resize((a,a), Image.NEAREST).save(os.path.join(folder,'ic_launcher_foreground.png'))

# adaptive icon: background warna oranye, foreground karakter Udin
os.makedirs(os.path.join(RES,'mipmap-anydpi-v26'), exist_ok=True)
for name in ('ic_launcher.xml','ic_launcher_round.xml'):
    open(os.path.join(RES,'mipmap-anydpi-v26',name),'w').write(
'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
open(os.path.join(RES,'values','ic_launcher_background.xml'),'w').write(
'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#E8863A</color>
</resources>
''')
print("Ikon Udin terpasang.")
