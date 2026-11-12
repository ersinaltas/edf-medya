"""Google E-Tablo'daki güncel programı sayfaya gömülen yedek kopyaya yazar:
  program_listeler.json  ("Listeler" sekmesi: stil, seviye, salon, gün)
  program_tablo.csv      (her gün sekmesi: Gün, Başlangıç, Bitiş, Salon, Bitiş Salonu, Stil, Konu, Seviye, Eğitmen, Not)
Sütunlar başlık adıyla bulunur. Tablo 'linke sahip herkes görüntüleyebilir' olmalı. Bir sekme okunamazsa eski kopya kalır."""
import csv, json, os, subprocess, sys
from urllib.parse import quote
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sid = json.load(open(os.path.join(ROOT, 'program_ayar.json')))['sheet_id']

def gviz(ad):
    t = subprocess.run(['curl', '-sS', '-L', '--max-time', '60', f'https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:json&headers=1&sheet={quote(ad)}'],
                       capture_output=True, text=True).stdout
    try:
        j = json.loads(t[t.index('{'):t.rindex('}') + 1]); assert j.get('status') != 'error'
    except Exception:
        print(f'program: "{ad}" sekmesi okunamadı (paylaşım kapalı olabilir), eski kopya kullanılıyor'); sys.exit(0)
    lab = [(c.get('label') or '').strip().lower().replace('I', 'ı') for c in j['table']['cols']]
    rows = [[(c.get('f') if c and c.get('f') is not None else (str(c.get('v')) if c and c.get('v') is not None else '')).strip() for c in (r.get('c') or [])] for r in j['table']['rows']]
    return lab, rows

def sutun(lab, *adlar):
    for a in adlar:
        if a in lab: return lab.index(a)
    return -1
al = lambda r, k: r[k] if 0 <= k < len(r) else ''

lab, rows = gviz('Listeler')
c = {a: sutun(lab, a) for a in ['stil', 'stil türü', 'stil rengi', 'seviye', 'seviye türü', 'seviye rengi', 'salon', 'gün', 'tarih']}
L = {'stil': [], 'seviye': [], 'salon': [], 'gun': []}
for r in rows:
    if al(r, c['stil']): L['stil'].append([al(r, c['stil']), al(r, c['stil türü']), al(r, c['stil rengi'])])
    if al(r, c['seviye']): L['seviye'].append([al(r, c['seviye']), al(r, c['seviye türü']), al(r, c['seviye rengi'])])
    if al(r, c['salon']): L['salon'].append(al(r, c['salon']))
    if al(r, c['gün']): L['gun'].append([al(r, c['gün']), al(r, c['tarih'])])
if not (L['stil'] and L['salon'] and L['gun']):
    print('program: Listeler sekmesi eksik, eski kopya kullanılıyor'); sys.exit(0)

out = []
for g, _ in L['gun']:
    lab, rows = gviz(g)
    k = [sutun(lab, 'başlangıç'), sutun(lab, 'bitiş'), sutun(lab, 'salon'), sutun(lab, 'bitiş salonu'), sutun(lab, 'stil'),
         sutun(lab, 'konu', 'başlık'), sutun(lab, 'seviye', 'kategori'), sutun(lab, 'eğitmen'), sutun(lab, 'not')]
    if k[4] < 0 or k[5] < 0:
        print(f'program: "{g}" sekmesi eski sütun düzeninde (Stil/Konu yok), eski kopya kullanılıyor'); sys.exit(0)
    for r in rows:
        v = [al(r, i) for i in k]
        if any(v): out.append([g] + v)
json.dump(L, open(os.path.join(ROOT, 'program_listeler.json'), 'w'), ensure_ascii=False, indent=1)
bas = ['Gün', 'Başlangıç', 'Bitiş', 'Salon', 'Bitiş Salonu', 'Stil', 'Konu', 'Seviye', 'Eğitmen', 'Not']
csv.writer(open(os.path.join(ROOT, 'program_tablo.csv'), 'w', newline='')).writerows([bas] + out)
print('program: tablodan', len(out), 'satır,', len(L['stil']), 'stil,', len(L['seviye']), 'seviye çekildi')
