#!/bin/sh
# Siteyi önceki bir sürüme döndürür (içerik değişmez, sadece yükleyici o sürümü gösterir).
# Kullanım: sh tools/geri_al.sh <no>    Sürümler: python3 tools/surum.py liste
set -e
cd "$(dirname "$0")/.."
R=$(python3 tools/surum.py aktif "$1")
git add web/yukle.js surumler.json SURUMLER.md
git -c user.name="Ersin Altaş" -c user.email="ersinaltas87@gmail.com" commit -q -m "Geri alındı: $R" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin main
echo "Aktif: $R"
