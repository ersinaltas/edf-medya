"""Google E-Tablo'daki güncel programı program_tablo.csv'ye (sayfaya gömülen yedek kopya) yazar.
Tablo 'linke sahip herkes görüntüleyebilir' olmalı. Başarısız olursa eski kopya kalır."""
import csv, json, os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sid = json.load(open(os.path.join(ROOT, 'program_ayar.json')))['sheet_id']
t = subprocess.run(['curl', '-sS', '-L', '--max-time', '60', f'https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:json&headers=1&sheet=Program'],
                   capture_output=True, text=True).stdout
try:
    j = json.loads(t[t.index('{'):t.rindex('}') + 1])
except Exception:
    print('program: tablo okunamadı (paylaşım kapalı olabilir), eski kopya kullanılıyor'); sys.exit(0)
bas = [c.get('label', '') for c in j['table']['cols']][:9]
rows = [[(c.get('f') if c and c.get('f') is not None else (str(c.get('v')) if c and c.get('v') is not None else '')) for c in (r.get('c') or [])][:9] for r in j['table']['rows']]
rows = [r + [''] * (9 - len(r)) for r in rows if any(r)]
csv.writer(open(os.path.join(ROOT, 'program_tablo.csv'), 'w', newline='')).writerows([bas] + rows)
print('program: tablodan', len(rows), 'satır çekildi')
