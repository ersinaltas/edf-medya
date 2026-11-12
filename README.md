# EDF Medya

edfturkey.com'daki EDF sayfalarının kaynağı. ikas'ta sadece sabit bir yükleyici kodu durur; içerik buradan gelir.

## ikas'taki sabit kod
```html
<div data-edf="artistler"><script src="https://ersinaltas.github.io/edf-medya/web/yukle.js"></script><img alt="" style="display:none" src="data:,x" onerror="if(!window.__edfYukle){window.__edfYukle=1;var s=document.createElement('script');s.src='https://ersinaltas.github.io/edf-medya/web/yukle.js';document.body.appendChild(s)}"></div>
```
Program sayfası için `data-edf="program"`, Hakkımızda için `data-edf="hakkimizda"`, Ekibimiz için `data-edf="ekip"`.

## Dosyalar
- `web/yukle.js`: Yükleyici. Hangi sürümün yayında olduğunu tutar (`V`). GitHub Pages'ten çekilir (10 dk önbellek), her push'tan ~1 dk sonra güncellenir.
- `sayfalar/*.html`: Sayfa parçaları (artistler ve program üretilir, hakkimizda.html elle düzenlenir). `{{KOK}}` yerine sürüm kökü yazılır.
- `web/artist.css`, `web/artist.js`: Artist sayfasının stili ve davranışı.
- `media/`: `<id>.mp4` (540×960), `<id>.jpg` (afiş), `<id>_k.jpg` (270×480 küçük görsel).
- `artistler.json` / `ARTISTLER.md`: Drive'ın son hâli (manifest).
- `program_tablo.csv`: Programın gömülü kopyası (Google E-Tablo'dan `tools/program_cek.py` ile çekilir). `program_ayar.json`: tablo ID'si, rozet, dipnot. `web/program.js` + `web/program.css`: ızgarayı çizer, tabloyu canlı okur. (`program_veri.json` eski ızgara verisi, arşiv.)
- `ekip.json`: Ekibimiz sayfası (kurucular + ekip). Fotoğraflar `ekip/` klasörüne, `foto` alanına dosya adı.

## Sürümler ve geri alma
Her yayın `SURUMLER.md` / `surumler.json`'a numaralı (v1, v2…) eklenir; içerik commit'e sabit olduğu için eski sürümler jsDelivr'da kalıcı.
- Liste: `python3 tools/surum.py liste`
- Geri dön: `sh tools/geri_al.sh <no>` → yükleyici o sürüme çevrilir, site ~1-10 dk içinde döner (ikas'a dokunulmaz).
- Not: Google E-Tablo'daki program canlı okunduğu için tablo içeriği sürümden bağımsız; sürüm sayfa kodunu ve gömülü yedeği geri alır.

## Akış
1. `python3 tools/guncelle.py <drive_kok_id> . <gecici_dizin>`: Drive farklarını işler.
2. `sh tools/yayinla.sh "mesaj"`: Üretir, gönderir, yükleyiciyi yeni sürüme çevirir, önbelleği temizler.

Sürüm adresleri sabit olduğu için içerik tarayıcıda ve CDN'de kalıcı önbellekte durur. Sadece küçük yükleyici kısa önbellekli.
## Medya depoları
jsDelivr bir repoyu en fazla 50 MB sunuyor, bu yüzden medya birden fazla repoya bölünür (`depolar.json`):
- `edf-medya` (1): İlk 83 artist.
- `edf-medya-2` (2): Sonra eklenenler. Şu an **aktif** depo.

Her artistin hangi depoda olduğu `artistler.json`'daki `depo` alanında. Mevcut artist kendi deposunda kalır, yeni artist aktif depoya gider. Aktif depo ~45 MB'a gelince yeni repo açılır (`edf-medya-3`), `depolar.json`'a eklenip `aktif` güncellenir. `tools/depo_yayinla.py` ek depoları gönderip sürümlerini yazar, `yayinla.sh` bunu kendisi çağırır.

jsDelivr sınırı: repo 50 MB, dosya 20 MB. Kalite ayarı (540×960, CRF 30) Ersin'in onayıyla sabit, daha fazla sıkıştırılmayacak.
