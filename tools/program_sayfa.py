"""program_tablo.csv + program_listeler.json'dan Program sayfası parçasını üretir. Izgarayı/listeyi web/program.js çizer;
sayfa önce gömülü kopyayı gösterir, sonra Google E-Tablo'yu canlı okur.
Kullanım: python3 tools/program_sayfa.py sayfalar/program.html"""
import csv, json, os, sys, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
AYAR = json.load(open(os.path.join(ROOT, 'program_ayar.json')))
rows = list(csv.reader(open(os.path.join(ROOT, 'program_tablo.csv'))))[1:]
L = json.load(open(os.path.join(ROOT, 'program_listeler.json')))
css = open(os.path.join(ROOT, 'web', 'program.css')).read()
veri = json.dumps({'listeler': L, 'rows': rows}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
IK_T = '<svg viewBox="0 0 16 16"><rect x="1.5" y="1.5" width="13" height="13" rx="2"/><path d="M1.5 6h13M6 6v8.5"/></svg>'
IK_L = '<svg viewBox="0 0 16 16"><path d="M5 3.5h9.5M5 8h9.5M5 12.5h9.5M1.5 3.5h.5M1.5 8h.5M1.5 12.5h.5"/></svg>'
H = ['<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap">',
     f'<div id="edf-prog" lang="tr" data-sheet="{html.escape(AYAR["sheet_id"])}"><style>{css}</style>',
     '<div class="hd"><div><h2>EDF 2027 <span>Workshop</span> Programı</h2><div class="meta">3–7 Şubat 2027 · Tasigo Hotel, Eskişehir</div></div>'
     + (f'<div class="draft">{html.escape(AYAR["rozet"])}</div>' if AYAR.get('rozet') else '') + '</div>',
     '<div class="tb"><div class="ara"><input type="search" placeholder="Eğitmen, stil ya da workshop ara…" aria-label="Eğitmen, stil ya da workshop ara" autocomplete="off"></div>'
     f'<div class="gv" role="group" aria-label="Görünüm"><button type="button" data-v="tablo" aria-pressed="false">{IK_T}Tablo</button><button type="button" data-v="liste" aria-pressed="false">{IK_L}Liste</button></div></div>',
     '<div class="fl" role="group" aria-label="Stil ve seviyeye göre filtrele"></div>',
     '<button type="button" class="gb" hidden>× Filtreleri temizle</button>',
     '<div class="ara so"><div class="sonuc" aria-live="polite"></div></div>',
     '<div class="tabs" role="tablist"></div>',
     '<div class="pns"></div>',
     f'<div class="ft">{html.escape(AYAR["dipnot"])}</div>',
     f'<script type="application/json" class="veri">{veri}</script>',
     '<script src="{{KOK}}web/program.js"></script></div>']
open(sys.argv[1], 'w').write(''.join(H))
print('program:', len(rows), 'satır,', len(L['stil']), 'stil')
