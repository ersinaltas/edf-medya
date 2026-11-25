#!/bin/sh
# Sayfaları üretir, GitHub'a gönderir, yükleyiciyi yeni sürüme çevirir. Yükleyici GitHub Pages'ten ~1 dk içinde güncellenir.
# Kullanım: sh tools/yayinla.sh "commit mesajı"
set -e
cd "$(dirname "$0")/.."
gitc() { git -c user.name="Ersin Altaş" -c user.email="ersinaltas87@gmail.com" commit -q -m "$1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; }
python3 tools/depo_yayinla.py "$1"
python3 tools/sayfa_uret.py parca sayfalar/artistler.html
python3 tools/ekip_uret.py sayfalar/ekip.html
python3 tools/program_cek.py
python3 tools/program_sayfa.py sayfalar/program.html
git add -A
gitc "$1" || true
git push -q origin main
H=$(git rev-parse HEAD)
# jsDelivr önbelleğini ısıt: ilk ziyaretçi soğuk CDN beklemesin
for f in sayfalar/*.html; do curl -sS -o /dev/null -m 60 "https://cdn.jsdelivr.net/gh/ersinaltas/edf-medya@$H/$f" || true; done
SN=$(python3 tools/surum.py ekle "$H" "$1")
git add web/yukle.js surumler.json SURUMLER.md
gitc "Yayın $SN: $1"
git push -q origin main
echo "Yayında: $SN ($H)"
