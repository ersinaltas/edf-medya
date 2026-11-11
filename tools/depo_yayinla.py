"""Ek medya depolarını (edf-medya-2, ...) GitHub'a gönderir ve depolar.json'a güncel commit'i yazar.
Ana repo (1) bu betikte değil, yayinla.sh'te gönderilir."""
import json, os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'depolar.json'); DEP = json.load(open(P))
msg = sys.argv[1] if len(sys.argv) > 1 else 'Medya güncellemesi'
def git(yol, *a, check=True): return subprocess.run(['git', '-C', yol, *a], capture_output=True, text=True, check=check).stdout.strip()
for k, d in DEP['depolar'].items():
    if k == '1': continue
    yol = os.path.normpath(os.path.join(ROOT, d['yol']))
    git(yol, 'add', '-A')
    if git(yol, 'status', '--porcelain'):
        git(yol, '-c', 'user.name=Ersin Altaş', '-c', 'user.email=ersinaltas87@gmail.com', 'commit', '-q', '-m', msg,
            '-m', 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>')
        git(yol, 'push', '-q', 'origin', 'main')
    d['surum'] = git(yol, 'rev-parse', 'HEAD')
    print(f"{d['ad']}: {d['surum'][:7]}")
json.dump(DEP, open(P, 'w'), ensure_ascii=False, indent=1)
