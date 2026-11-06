# EDF Medya

edfturkey.com'daki EDF sayfalarının kaynağı. ikas'ta sadece sabit bir yükleyici kodu durur; içerik buradan gelir.

## ikas'taki sabit kod
```html
<div data-edf="artistler"><script src="https://ersinaltas.github.io/edf-medya/web/yukle.js"></script><img alt="" style="display:none" src="data:,x" onerror="if(!window.__edfYukle){window.__edfYukle=1;var s=document.createElement('script');s.src='https://ersinaltas.github.io/edf-medya/web/yukle.js';document.body.appendChild(s)}"></div>
```
Program sayfası için `data-edf="program"`.

## Dosyalar
- `web/yukle.js`: Yükleyici. Hangi sürümün yayında olduğunu tutar (`V`). GitHub Pages'ten çekilir (10 dk önbellek), her push'tan ~1 dk sonra güncellenir.
- `sayfalar/*.html`: Sayfa parçaları. `{{KOK}}` yerine sürüm kökü yazılır.
- `web/artist.css`, `web/artist.js`: Artist sayfasının stili ve davranışı.
- `media/`: `<id>.mp4` (540×960), `<id>.jpg` (afiş), `<id>_k.jpg` (270×480 küçük görsel).
- `artistler.json` / `ARTISTLER.md`: Drive'ın son hâli (manifest).
- `program_veri.json`: Workshop programı verisi.

## Akış
1. `python3 tools/guncelle.py <drive_kok_id> . <gecici_dizin>`: Drive farklarını işler.
2. `sh tools/yayinla.sh "mesaj"`: Üretir, gönderir, yükleyiciyi yeni sürüme çevirir, önbelleği temizler.

Sürüm adresleri sabit olduğu için içerik tarayıcıda ve CDN'de kalıcı önbellekte durur. Sadece küçük yükleyici kısa önbellekli.
jsDelivr sınırı: repo 50 MB, dosya 20 MB.
