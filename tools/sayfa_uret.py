"""artistler.json'dan artist sayfası HTML'ini üretir.
  python3 tools/sayfa_uret.py embed    CIKTI.html CDN_KOK   -> ikas'a yapıştırılacak hafif HTML (CSS/JS/medya CDN'den)
  python3 tools/sayfa_uret.py parca    sayfalar/artistler.html  -> yükleyicinin çektiği parça ({{KOK}} = sürüm kökü)
  python3 tools/sayfa_uret.py artifact CIKTI.html           -> önizleme (CSS/JS içinde, medya göreli 'media/')
CDN_KOK örneği: https://cdn.jsdelivr.net/gh/ersinaltas/edf-medya@<commit>/"""
import sys, html, re, json, os
mode, out = sys.argv[1], sys.argv[2]
cdn = sys.argv[3] if mode == 'embed' else ('{{KOK}}' if mode == 'parca' else '')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
base = cdn + 'media/'
# Branş: Drive klasör adı -> (etiket, çerçeve rengi, etiket yazı rengi)
BR = {'Salsa': ('SALSA', '#E44351', '#fff'), 'Bachata': ('BACHATA', '#29649D', '#fff'), 'Kizomba': ('KIZOMBA', '#EF6A64', '#fff'),
      'Hip Hop': ('HIP HOP', '#41B8A6', '#fff'), 'Heels': ('HEELS', '#FF5994', '#fff'), 'Oryantal': ('ORYANTAL', '#B04FD9', '#fff'),
      'Zumba': ('ZUMBA', '#3CB44B', '#fff'), 'DJ': ('DJ', '#F0E559', '#1B2E4A'), 'Organizer Promoter': ('ORGANİZATÖR', '#DDE3EA', '#1B2E4A')}
SIRA = list(BR)
def slug(b): return re.sub(r'[^a-z0-9]+', '-', b.lower()).strip('-') or 'x'
A = [dict(id=a['id'], n=a['ad'], b=a['brans'], f=a['one_cikan']) for a in json.load(open(os.path.join(ROOT, 'artistler.json')))]
for a in A:
    if a['b'] and a['b'] not in BR: BR[a['b']] = (a['b'].upper(), '#9B7BD4', '#fff'); SIRA.append(a['b'])
TR = str.maketrans('ÇĞİIÖŞÜ', 'CGIIOSU')
grid = sorted(A, key=lambda a: a['n'].translate(TR))
brs = [b for b in SIRA if any(a['b'] == b for a in A)]
E = html.escape

def card(a):
    lab = BR.get(a['b'], ('',))[0]
    tag = f'<span class="tg">{lab}</span>' if lab else ''
    f = ' data-f' if a['f'] else ''
    return (f'<a class="cd b-{slug(a["b"])}" href="{base}{a["id"]}.mp4" data-id="{a["id"]}"{f}>'
            f'<img src="{base}{a["id"]}_k.jpg" width="270" height="480" alt="{E(a["n"])}" loading="lazy" decoding="async">{tag}</a>')

# Veriye bağlı küçük stil: branş renkleri + filtre kuralları
dyn = ''.join(f'#edf-art .b-{slug(b)}{{--c:{BR[b][1]};--cf:{BR[b][2]}}}' for b in brs)
dyn += '#edf-art #af-all:checked~.fl label[for=af-all]'
for b in brs:
    s = slug(b)
    dyn += f',#edf-art #af-{s}:checked~.fl label[for=af-{s}]'
dyn += '{background:var(--nv);color:#fff}'
dyn += ''.join(f'#edf-art #af-{slug(b)}:checked~.gr .cd:not(.b-{slug(b)}){{display:none}}' for b in brs)

band = ' <i>✦</i> '.join(['5 GÜN', '10 DANS STİLİ', '200+ EĞİTMEN VE DJ', '100+ WORKSHOP', '5 PARTİ ALANI']) + ' <i>✦</i> '
css = open(os.path.join(ROOT, 'web', 'artist.css')).read()
js = open(os.path.join(ROOT, 'web', 'artist.js')).read()

H = []
if mode == 'artifact':
    H.append('<title>EDF 2027 Artistler</title><meta name="claude:viewport-fit-sides" content="cover">')
    H.append('<style>:root{color-scheme:light}body{background:#fff;overflow-x:hidden;padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px))}</style>')
    H.append(f'<style>{css}</style>')
else:
    H.append('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>')
    H.append(f'<link rel="stylesheet" href="{cdn}web/artist.css">')
H.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap">')
H.append(f'<div id="edf-art" data-base="{base}"><style>{dyn}</style>')
H.append(f'<div class="hero pad"><h1>EDF 2027<span>Artistler</span></h1><p><b>Tüm artistleri afişe sığdıramadık</b>3–7 Şubat 2027 · Tasigo Hotel, Eskişehir. Şu ana kadar açıklanan {len(A)} artist; liste her hafta büyüyor.</p></div>')
H.append(f'<div class="band"><div>{band * 4}{band * 4}</div></div>')
H.append('<div class="jso"><div class="st pad">Öne çıkanlar</div>'
         '<div class="fw"><button class="ar p" type="button" aria-label="Önceki">‹</button><div class="ft"></div><button class="ar n" type="button" aria-label="Sonraki">›</button></div><div class="dots"></div>'
         '<div class="st pad">Line-up <small>durdurmak için üstüne gel</small></div><div class="mq"><div class="rw"></div></div><div class="mq rv"><div class="rw"></div></div></div>')
H.append('<div class="pad"><div class="st">Tüm artistler <small>izlemek için afişe dokun</small></div>')
H.append('<input type="radio" name="edfaf" id="af-all" checked>' + ''.join(f'<input type="radio" name="edfaf" id="af-{slug(b)}">' for b in brs))
H.append(f'<div class="fl"><label for="af-all">TÜMÜ<small>{len(grid)}</small></label>' + ''.join(f'<label for="af-{slug(b)}">{BR[b][0]}<small>{sum(a["b"] == b for a in grid)}</small></label>' for b in brs) + '</div>')
H.append('<div class="gr">' + ''.join(card(a) for a in grid) + '</div>')
H.append('<div class="more"><b>Daha fazla isim<br>çok yakında açıklanacak</b><a href="/pages/biletler">Pass al →</a></div></div>')
if mode == 'artifact':
    H.append(f'<script>{js}</script></div>')
elif mode == 'parca':
    H.append(f'<script src="{cdn}web/artist.js"></script></div>')
else:
    # <script> ilk açılışta çalışır; ikas sayfayı sonradan (menüden geçişte) eklerse img onerror yedek olarak yükler.
    boot = f"if(!document.getElementById('edf-art').dataset.ok){{var s=document.createElement('script');s.src='{cdn}web/artist.js';document.body.appendChild(s)}}"
    H.append(f'<script src="{cdn}web/artist.js" defer></script>')
    H.append(f'<img alt="" style="display:none" src="data:,x" onerror="{boot}"></div>')
open(out, 'w').write(''.join(H))
print(mode, len(A), 'artist,', sum(a['f'] for a in A), 'öne çıkan,', os.path.getsize(out), 'bayt')
