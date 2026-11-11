"""program_tablo.csv'den Program sayfası parçasını üretir. Izgarayı web/program.js çizer;
sayfa önce gömülü kopyayı gösterir, sonra Google E-Tablo'yu canlı okur.
Kullanım: python3 tools/program_sayfa.py sayfalar/program.html"""
import csv, json, os, sys, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
AYAR = json.load(open(os.path.join(ROOT, 'program_ayar.json')))
rows = list(csv.reader(open(os.path.join(ROOT, 'program_tablo.csv'))))[1:]
css = open(os.path.join(ROOT, 'web', 'program.css')).read()
LEG = [('beg','Beginner'),('int','Intermediate'),('all','All Level'),('adv','Advanced'),('hh','Hip Hop & Free Style'),
       ('lindy','Lindy Hop / Jazz'),('zumba','Zumba'),('kpop','K-Pop'),('kids','Kids'),('comp','Competition')]
veri = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
H = ['<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap">',
     f'<div id="edf-prog" lang="tr" data-sheet="{html.escape(AYAR["sheet_id"])}"><style>{css}</style>',
     '<div class="hd"><div><h2>EDF 2027 <span>Workshop</span> Programı</h2><div class="meta">3–7 Şubat 2027 · Tasigo Hotel, Eskişehir</div></div>'
     + (f'<div class="draft">{html.escape(AYAR["rozet"])}</div>' if AYAR.get('rozet') else '') + '</div>',
     '<div class="tabs" role="tablist"></div>',
     '<div class="leg">' + ''.join(f'<span lang="en"><i style="background:var(--k)" class="k-{k}"></i>{v}</span>' for k, v in LEG) + '</div>',
     '<div class="pns"></div>',
     f'<div class="ft">{html.escape(AYAR["dipnot"])}</div>',
     f'<script type="application/json" class="veri">{veri}</script>',
     '<script src="{{KOK}}web/program.js"></script></div>']
open(sys.argv[1], 'w').write(''.join(H))
print('program:', len(rows), 'satır')
