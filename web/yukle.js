/* EDF sayfa yükleyici. ikas'taki sabit kod bunu çağırır; içerik GitHub'daki sabit bir sürümden gelir.
   Kullanım: <div data-edf="artistler"></div> veya <div data-edf="program"></div> */
(function () {
  var V = '84071dcb310221f5bb6d365bedf4f4d8094d228c';
  var KOK = 'https://cdn.jsdelivr.net/gh/ersinaltas/edf-medya@' + V + '/';
  function kur(el) {
    if (el.getAttribute('data-edf-ok')) return;
    el.setAttribute('data-edf-ok', '1');
    var ad = el.getAttribute('data-edf');
    fetch(KOK + 'sayfalar/' + ad + '.html').then(function (r) { return r.text(); }).then(function (h) {
      var t = document.createElement('template');
      t.innerHTML = h.replace(/\{\{KOK\}\}/g, KOK);
      var f = t.content, bekle = [];
      /* Önce stiller yüklensin, sayfa çıplak görünmesin */
      [].slice.call(f.querySelectorAll('link[rel=stylesheet],link[rel=preconnect]')).forEach(function (l) {
        if (!document.querySelector('link[href="' + l.getAttribute('href') + '"]')) {
          if (l.rel === 'stylesheet') bekle.push(new Promise(function (ok) { l.onload = l.onerror = ok; setTimeout(ok, 2500); }));
          document.head.appendChild(l);
        } else l.parentNode.removeChild(l);
      });
      var js = [].slice.call(f.querySelectorAll('script')).filter(function (s) { return !s.type || /javascript/i.test(s.type); });
      js.forEach(function (s) { s.parentNode.removeChild(s); });
      Promise.all(bekle).then(function () {
        el.innerHTML = ''; el.appendChild(f);
        js.forEach(function (o) { var s = document.createElement('script'); if (o.src) s.src = o.src; else s.text = o.text; document.body.appendChild(s); });
      });
    });
  }
  function hepsi() { [].slice.call(document.querySelectorAll('[data-edf]')).forEach(kur); }
  hepsi();
  /* ikas sayfalar arası geçişte içeriği sonradan ekler; yeni kutuları yakala */
  if (window.MutationObserver && !window.__edfIzle) {
    window.__edfIzle = 1;
    new MutationObserver(hepsi).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
