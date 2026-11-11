"""ekip.json'dan Ekibimiz sayfası parçasını üretir.
Kullanım: python3 tools/ekip_uret.py sayfalar/ekip.html
Fotoğraf: 'foto' alanına dosya adı (repo/ekip/ altında, örn. "aykan.jpg") ya da tam adres. Boşsa baş harfli renkli kart çıkar."""
import json, os, sys, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = json.load(open(os.path.join(ROOT, 'ekip.json')))
E = html.escape
RENK = ['#E44351', '#29649D', '#EF6A64', '#1B2E4A', '#F0E559']
def bas(ad):
    p = [x for x in ad.replace('&', ' ').split() if x[:1].isalpha()]
    return (p[0][0] + (p[-1][0] if len(p) > 1 else '')).upper() if p else '?'
def foto(k, i):
    f = k.get('foto', '')
    c = RENK[i % len(RENK)]; fg = '#1B2E4A' if c == '#F0E559' else '#fff'
    if f:
        src = f if f.startswith('http') else '{{KOK}}ekip/' + f
        return f'<div class="ft"><img src="{E(src)}" alt="{E(k["ad"])}" loading="lazy" decoding="async"></div>'
    return f'<div class="ft bos" style="--c:{c};--fg:{fg}"><span>{E(bas(k["ad"]))}</span></div>'
def ig(k):
    h = k.get('instagram', '').lstrip('@')
    return f'<a class="ig" href="https://instagram.com/{E(h)}" target="_blank" rel="noopener">@{E(h)}</a>' if h else ''
css = r'''
#edf-ek{--nv:#1B2E4A;--rd:#E44351;--bl:#29649D;--ye:#F0E559;--sa:#EF6A64;font-family:'Montserrat',system-ui,sans-serif;color:var(--nv);background:#fff;line-height:1.5;font-size:15px;text-align:left}
#edf-ek *{box-sizing:border-box;line-height:inherit}
#edf-ek a{color:inherit;text-decoration:none}
#edf-ek h1,#edf-ek h2,#edf-ek h3,#edf-ek p{margin:0}
#edf-ek .ey{font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--rd)}
#edf-ek .hero{padding:36px 0 8px;display:grid;grid-template-columns:1.2fr 1fr;gap:32px;align-items:end}
#edf-ek h1{font-weight:900;font-size:clamp(36px,5.6vw,72px);line-height:.95;letter-spacing:-.02em;text-transform:uppercase;margin-top:10px}
#edf-ek h1 span{color:var(--rd)}
#edf-ek .lead{font-weight:600;font-size:16px;max-width:460px}
#edf-ek .st{display:flex;align-items:center;gap:14px;margin:48px 0 20px;font-weight:900;font-size:clamp(20px,2.4vw,30px);text-transform:uppercase}
#edf-ek .st:after{content:"";flex:1;height:3px;background:var(--nv);opacity:.12}
#edf-ek .ft{position:relative;aspect-ratio:4/5;border-radius:14px;overflow:hidden;background:#EEE}
#edf-ek .ft img{width:100%;height:100%;object-fit:cover;display:block;filter:grayscale(.15);transition:transform .4s,filter .4s}
#edf-ek .ft.bos{background:var(--c);display:grid;place-items:center;background-image:repeating-linear-gradient(115deg,transparent 0 22px,rgba(255,255,255,.07) 22px 44px)}
#edf-ek .ft.bos span{font-weight:900;font-size:clamp(44px,6vw,84px);letter-spacing:-.03em;color:var(--fg);opacity:.95}
#edf-ek .kur{display:grid;grid-template-columns:1fr 1fr;gap:24px}
#edf-ek .kk{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:22px;align-items:end;border:1px solid #E6E2DA;border-radius:16px;padding:18px}
#edf-ek .kk h3{font-weight:900;font-size:clamp(22px,2.4vw,30px);line-height:1.05;text-transform:uppercase}
#edf-ek .gv{display:inline-block;margin:10px 0 12px;background:var(--nv);color:#fff;font-weight:800;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border-radius:4px}
#edf-ek .kk p{font-weight:600;font-size:14px;opacity:.85}
#edf-ek .ig{display:inline-block;margin-top:10px;font-weight:800;font-size:13px;color:var(--rd)}
#edf-ek .gr{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
#edf-ek .uy h3{font-weight:900;font-size:17px;text-transform:uppercase;margin-top:12px}
#edf-ek .uy .rl{font-weight:700;font-size:13px;color:var(--bl);margin-top:2px}
#edf-ek .uy:hover .ft img{transform:scale(1.04);filter:none}
#edf-ek .cta{margin:52px 0 32px;padding:30px;border-radius:14px;background:var(--nv);color:#fff;display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center;background-image:repeating-linear-gradient(115deg,transparent 0 26px,rgba(255,255,255,.035) 26px 52px)}
#edf-ek .cta b{font-weight:900;font-size:clamp(20px,2.6vw,32px);line-height:1.05;text-transform:uppercase}
#edf-ek .cta b em{font-style:normal;color:var(--ye)}
#edf-ek .cta p{font-weight:600;font-size:14px;opacity:.85;margin-top:8px;max-width:520px}
#edf-ek .cta .ml{font-weight:900;font-size:15px;background:#fff;color:var(--nv);padding:14px 20px;border-radius:40px;user-select:all}
@media(max-width:960px){#edf-ek .kur{grid-template-columns:1fr}#edf-ek .gr{grid-template-columns:repeat(3,1fr)}}
@media(max-width:700px){#edf-ek .hero{grid-template-columns:1fr;gap:16px}#edf-ek .gr{grid-template-columns:1fr 1fr;gap:16px}}
@media(max-width:480px){#edf-ek .kk{grid-template-columns:1fr;padding:14px}#edf-ek .kk .ft{max-width:240px}#edf-ek .cta{padding:22px}}
'''
H = ['<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap">',
     f'<div id="edf-ek"><style>{css}</style>',
     '<section class="hero"><div><p class="ey">EDF Turkey · Ekip</p><h1>Ekibimiz<span>.</span></h1></div>',
     '<p class="lead">Beş günlük festivalin arkasında aylar süren bir hazırlık ve bu işi tutkuyla yapan bir ekip var. EDF\'yi her yıl birlikte kuranlarla tanışın.</p></section>',
     '<h2 class="st">Kurucular</h2><div class="kur">']
for i, k in enumerate(D['kurucular']):
    H.append(f'<div class="kk">{foto(k, i)}<div><h3>{E(k["ad"])}</h3><span class="gv">{E(k["gorev"])}</span><p>{E(k.get("aciklama", ""))}</p>{ig(k)}</div></div>')
H.append('</div><h2 class="st">Ekip</h2><div class="gr">')
for i, k in enumerate(D['ekip']):
    H.append(f'<div class="uy">{foto(k, i + 1)}<h3>{E(k["ad"])}</h3><p class="rl">{E(k["gorev"])}</p>{ig(k)}</div>')
H.append('</div><div class="cta"><div><b>Ekibe <em>katıl.</em></b><p>Festival haftasında gönüllü olmak ya da ekibimizde yer almak istersen bize yaz.</p></div><span class="ml">info@edfturkey.com</span></div></div>')
open(sys.argv[1], 'w').write(''.join(H))
print('ekip:', len(D['kurucular']), 'kurucu,', len(D['ekip']), 'üye')
