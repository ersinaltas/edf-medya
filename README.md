# EDF Medya

edfturkey.com artist sayfasının afişleri (jpg) ve hareketli afişleri (mp4, 540×960, web için küçültülmüş).
jsDelivr üzerinden sunulur: `https://cdn.jsdelivr.net/gh/ersinaltas/edf-medya@<commit>/media/`

- **Kaynak:** Google Drive › EDF 2027 Afişler. Alt klasör = branş, dosya adında ✅ = öne çıkan.
- **artistler.json:** Drive'ın son hâli (manifest). Güncellemeler bununla karşılaştırılır.
- **ARTISTLER.md:** Okunur liste.
- **tools/guncelle.py:** Drive'ı tarar, sadece yeni/değişen afişleri işler, kalkanları siler.
- **tools/sayfa_uret.py:** ikas'a yapıştırılacak HTML'i üretir.

jsDelivr sınırı: repo 50 MB, dosya 20 MB.
