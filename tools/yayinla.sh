#!/bin/sh
# Sayfaları üretir, GitHub'a gönderir, yükleyiciyi yeni sürüme çevirir. Yükleyici GitHub Pages'ten ~1 dk içinde güncellenir.
# Kullanım: sh tools/yayinla.sh "commit mesajı"
set -e
cd "$(dirname "$0")/.."
gitc() { git -c user.name="Ersin Altaş" -c user.email="ersinaltas87@gmail.com" commit -q -m "$1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; }
python3 tools/depo_yayinla.py "$1"
python3 tools/sayfa_uret.py parca sayfalar/artistler.html
python3 tools/program_uret.py program_veri.json sayfalar/program.html /dev/null && rm -f program_veri_isimsiz.json
git add -A
gitc "$1" || true
git push -q origin main
H=$(git rev-parse HEAD)
sed -i "s/var V = '[^']*'/var V = '$H'/" web/yukle.js
git add web/yukle.js
gitc "Yükleyici: sürüm $(echo $H | cut -c1-7)"
git push -q origin main
echo "Yayında: $H"
