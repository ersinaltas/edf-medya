"""Google E-Tablo'daki (her gün ayrı sekme) güncel programı program_tablo.csv'ye (sayfaya gömülen yedek kopya) yazar.
Tablo 'linke sahip herkes görüntüleyebilir' olmalı. Başarısız olursa eski kopya kalır."""
import csv, json, os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sid = json.load(open(os.path.join(ROOT, 'program_ayar.json')))['sheet_id']
from urllib.parse import quote
GUN = ['Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
rows = []
for g in GUN:
    t = subprocess.run(['curl', '-sS', '-L', '--max-time', '60', f'https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:json&headers=1&sheet={quote(g)}'],
                       capture_output=True, text=True).stdout
    try:
        j = json.loads(t[t.index('{'):t.rindex('}') + 1]); assert j.get('status') != 'error'
    except Exception:
        print(f'program: "{g}" sekmesi okunamadı (paylaşım kapalı olabilir), eski kopya kullanılıyor'); sys.exit(0)
    for r in j['table']['rows']:
        v = [(c.get('f') if c and c.get('f') is not None else (str(c.get('v')) if c and c.get('v') is not None else '')) for c in (r.get('c') or [])][:8]
        v = v + [''] * (8 - len(v))
        if any(v): rows.append([g] + v)
bas = ['Gün', 'Başlangıç', 'Bitiş', 'Salon', 'Bitiş Salonu', 'Başlık', 'Eğitmen', 'Kategori', 'Not']
csv.writer(open(os.path.join(ROOT, 'program_tablo.csv'), 'w', newline='')).writerows([bas] + rows)
print('program: tablodan', len(rows), 'satır çekildi')
