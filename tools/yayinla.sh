#!/bin/sh
# Sayfaları üretir, GitHub'a gönderir, yükleyiciyi yeni sürüme çevirir ve jsDelivr önbelleğini temizler.
# Kullanım: sh tools/yayinla.sh "commit mesajı"
set -e
cd "$(dirname "$0")/.."
GIT="git -c user.name=Ersin_Altaş -c user.email=ersinaltas87@gmail.com"
python3 tools/sayfa_uret.py parca sayfalar/artistler.html
python3 tools/program_uret.py program_veri.json sayfalar/program.html /dev/null && rm -f program_veri_isimsiz.json
git add -A
$GIT commit -qm "$1" || true
git push -q origin main
H=$(git rev-parse HEAD)
sed -i "s/var V = '[^']*'/var V = '$H'/" web/yukle.js
git add web/yukle.js
$GIT commit -qm "Yükleyici: sürüm $(echo $H | cut -c1-7)"
git push -q origin main
curl -sS --max-time 30 "https://purge.jsdelivr.net/gh/ersinaltas/edf-medya@main/web/yukle.js" > /dev/null
echo "Yayında: $H"
