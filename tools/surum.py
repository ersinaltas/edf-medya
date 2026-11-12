"""Sürüm kaydı. Her yayın surumler.json + SURUMLER.md'ye numaralı eklenir; geri dönüş yükleyiciyi o sürümün commit'ine çevirir.
  python3 tools/surum.py ekle <commit> "<mesaj>"   (yayinla.sh çağırır)
  python3 tools/surum.py liste
  python3 tools/surum.py aktif <no>                (geri_al.sh çağırır; yükleyiciyi o sürüme çevirir)"""
import json, os, sys, re, datetime
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'surumler.json'); Y = os.path.join(ROOT, 'web', 'yukle.js'); MD = os.path.join(ROOT, 'SURUMLER.md')
S = json.load(open(P)) if os.path.exists(P) else {'aktif': None, 'surumler': []}
def kaydet():
    json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1)
    with open(MD, 'w') as f:
        f.write('# Yayın sürümleri\n\nEn yeni üstte. **Aktif** sürüm sitede görünen. Geri dönmek için: `sh tools/geri_al.sh <no>`\n\n| No | Tarih | Commit | Açıklama |\n|---|---|---|---|\n')
        for s in reversed(S['surumler']):
            f.write(f"| {'**v'+str(s['no'])+' (aktif)**' if s['no'] == S['aktif'] else 'v'+str(s['no'])} | {s['tarih']} | `{s['commit'][:7]}` | {s['mesaj']} |\n")
def yukleyici(commit):
    t = open(Y).read(); open(Y, 'w').write(re.sub(r"var V = '[^']*'", f"var V = '{commit}'", t))
k = sys.argv[1]
if k == 'ekle':
    no = (S['surumler'][-1]['no'] + 1) if S['surumler'] else 1
    S['surumler'].append({'no': no, 'tarih': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%Y-%m-%d %H:%M'), 'commit': sys.argv[2], 'mesaj': sys.argv[3]})
    S['aktif'] = no; yukleyici(sys.argv[2]); kaydet(); print(f'v{no}')
elif k == 'aktif':
    no = int(sys.argv[2].lstrip('v')); s = [x for x in S['surumler'] if x['no'] == no][0]
    S['aktif'] = no; yukleyici(s['commit']); kaydet(); print(f"v{no} {s['commit'][:7]} {s['mesaj']}")
elif k == 'liste':
    for s in S['surumler']: print(('* ' if s['no'] == S['aktif'] else '  ') + f"v{s['no']}  {s['tarih']}  {s['commit'][:7]}  {s['mesaj']}")
