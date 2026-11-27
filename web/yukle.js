/* EDF sayfa yükleyici. ikas'taki sabit kod bunu çağırır; içerik GitHub'daki sabit bir sürümden gelir.
   Kullanım: <div data-edf="artistler"></div> veya <div data-edf="program"></div>
   Hız: parça CSS+JS'i içinde taşır (tek istek); aynı sürüm tarayıcıda saklanır, tekrar ziyarette ağ beklenmez. */
(function () {
  var V = '18abec9dbbb09672617605251abcd8bb8f7802e6';
  var KOK = 'https://cdn.jsdelivr.net/gh/ersinaltas/edf-medya@' + V + '/';
  function oku(ad) { try { var x = JSON.parse(localStorage.getItem('edf:' + ad) || 'null'); return x && x.v === V ? x.h : null; } catch (e) { return null; } }
  function yaz(ad, h) { try { localStorage.setItem('edf:' + ad, JSON.stringify({ v: V, h: h })); } catch (e) {} }
  function bas(el, h) {
    var t = document.createElement('template');
    t.innerHTML = h.replace(/\{\{KOK\}\}/g, KOK);
    var f = t.content, bekle = [];
    [].slice.call(f.querySelectorAll('link[rel=stylesheet],link[rel=preconnect]')).forEach(function (l) {
      var href = l.getAttribute('href');
      if (!document.querySelector('link[href="' + href + '"]')) {
        /* yazı tipi (Google Fonts) beklenmez; yalnız kendi stil dosyamız varsa beklenir */
        if (l.rel === 'stylesheet' && href.indexOf(KOK) === 0) bekle.push(new Promise(function (ok) { l.onload = l.onerror = ok; setTimeout(ok, 2500); }));
        document.head.appendChild(l);
      } else l.parentNode.removeChild(l);
    });
    var js = [].slice.call(f.querySelectorAll('script')).filter(function (s) { return !s.type || /javascript/i.test(s.type); });
    js.forEach(function (s) { s.parentNode.removeChild(s); });
    function koy() {
      el.innerHTML = ''; el.appendChild(f);
      js.forEach(function (o) { var s = document.createElement('script'); if (o.src) s.src = o.src; else s.text = o.text; document.body.appendChild(s); });
    }
    if (bekle.length) Promise.all(bekle).then(koy); else koy();
  }
  function kur(el) {
    if (el.getAttribute('data-edf-ok')) return;
    el.setAttribute('data-edf-ok', '1');
    var ad = el.getAttribute('data-edf'), h = oku(ad);
    if (h) return bas(el, h);
    fetch(KOK + 'sayfalar/' + ad + '.html').then(function (r) { if (!r.ok) throw r; return r.text(); }).then(function (h) { yaz(ad, h); bas(el, h); });
  }
  function hepsi() { [].slice.call(document.querySelectorAll('[data-edf]')).forEach(kur); }
  hepsi();
  /* ikas sayfalar arası geçişte içeriği sonradan ekler; yeni kutuları yakala */
  if (window.MutationObserver && !window.__edfIzle) {
    window.__edfIzle = 1;
    new MutationObserver(hepsi).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
