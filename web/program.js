/* EDF workshop programı (v3: Stil · Konu · Seviye).
   Google E-Tablo: her gün ayrı sekme (Başlangıç, Bitiş, Salon, Bitiş Salonu, Stil, Konu, Seviye, Eğitmen, Not)
   + "Listeler" sekmesi (Stil / Stil Türü / Stil Rengi · Seviye / Seviye Türü / Seviye Rengi · Salon · Gün / Tarih).
   Sütunlar başlık adıyla okunur; sırası değişse de çalışır. Önce sayfaya gömülü kopya çizilir, sonra tablo canlı okunur. */
(function () {
  var hepsi = document.querySelectorAll('#edf-prog');
  var R = hepsi[hepsi.length - 1];
  if (!R || R.getAttribute('data-ok')) return;
  R.setAttribute('data-ok', '1');

  var GRI = '#8C96A3';
  var L = { stil: [], seviye: [], salon: [], gun: [] }, IDX = { stil: {}, sev: {} };
  var rows = [], aktif = 1, gorunum = '', fStil = {}, fSev = {}, imza = '';

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function saat(t) { var m = String(t || '').match(/(\d{1,2})[:.](\d{2})/); return m ? ('0' + m[1]).slice(-2) + ':' + m[2] : ''; }
  function dk(t) { var p = t.split(':'), h = +p[0]; return (h < 6 ? h + 24 : h) * 60 + (+p[1]); }
  function bas(s) { return String(s || '').trim().toLocaleLowerCase('tr'); }
  function sade(s) { s = bas(s).replace(/[çğıöşü]/g, function (c) { return { 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u' }[c]; }); return s.normalize ? s.normalize('NFD').replace(/[̀-ͯ]/g, '') : s; }
  function trim(s) { return String(s == null ? '' : s).trim(); }

  /* Renk: "#E44351" ya da iki renk "#EF6A64 #F0E559" (geçişli) */
  function renkler(r) { return (String(r || '').match(/#[0-9a-f]{6}\b|#[0-9a-f]{3}\b/gi) || []); }
  function hex6(h) { return h.length === 4 ? '#' + h[1] + h[1] + h[2] + h[2] + h[3] + h[3] : h; }
  function parlak(h) { h = hex6(h); var r = parseInt(h.substr(1, 2), 16) / 255, g = parseInt(h.substr(3, 2), 16) / 255, b = parseInt(h.substr(5, 2), 16) / 255; return 0.2126 * r + 0.7152 * g + 0.0722 * b; }
  function zemin(r) {
    var c = renkler(r).map(hex6); if (!c.length) return null;
    var ort = c.reduce(function (t, x) { return t + parlak(x); }, 0) / c.length;
    return { bg: c.length > 1 ? 'linear-gradient(160deg,' + c.join(',') + ')' : c[0], ana: c[0], yazi: ort > 0.6 ? '#1B2E4A' : '#fff', acik: ort > 0.88 };
  }

  /* Listeler → hızlı erişim */
  function hazirla(l) {
    L = { stil: l.stil || [], seviye: l.seviye || [], salon: (l.salon || []).map(function (s) { return trim(s).toUpperCase(); }), gun: l.gun || [] };
    IDX = { stil: {}, sev: {} };
    L.stil.forEach(function (x, i) { IDX.stil[bas(x[0])] = { ad: x[0], etk: /etkinlik/i.test(x[1] || ''), renk: x[2] || '', i: i }; });
    L.seviye.forEach(function (x, i) { IDX.sev[bas(x[0])] = { ad: x[0], etk: /etkinlik/i.test(x[1] || ''), renk: x[2] || '', i: i }; });
  }
  function stilBil(s) { return IDX.stil[bas(s)] || { ad: s, etk: false, renk: '', i: 999 }; }
  function sevBil(s) { return IDX.sev[bas(s)] || { ad: s, etk: false, renk: '', i: 999 }; }

  function temizle(r) {
    return r.map(function (x) {
      return { gun: trim(x[0]), b: saat(x[1]), e: saat(x[2]), s1: trim(x[3]).toUpperCase(), s2: trim(x[4]).toUpperCase(),
        stil: trim(x[5]), konu: trim(x[6]), sev: trim(x[7]), eg: trim(x[8]), n: trim(x[9]) };
    }).filter(function (x) { return x.gun && x.b && (x.konu || x.stil) && L.salon.indexOf(x.s1) >= 0; });
  }
  function etkinlikMi(x) { return stilBil(x.stil).etk || (!!x.sev && sevBil(x.sev).etk); }
  function bos(o) { for (var k in o) return false; return true; }
  function eslesir(x, q) {
    if (!bos(fStil) && !fStil[bas(x.stil)]) return false;
    if (!bos(fSev) && !fSev[bas(x.sev)]) return false;
    if (q) { var t = sade([x.stil, x.konu, x.sev, x.eg, x.n, x.s1].join(' ')); return q.split(' ').every(function (p) { return t.indexOf(p) >= 0; }); }
    return true;
  }

  var tabs = R.querySelector('.tabs'), pns = R.querySelector('.pns'), fl = R.querySelector('.fl'),
    kutu = R.querySelector('.ara input'), sonuc = R.querySelector('.sonuc'), gb = R.querySelector('.gb'), gv = R.querySelector('.gv');
  function sorgu() { var q = kutu ? sade(kutu.value).replace(/\s+/g, ' ').trim() : ''; return q.length > 1 ? q : ''; }
  function filtreVar() { return !bos(fStil) || !bos(fSev) || !!sorgu(); }

  /* ---------- Tablo (ızgara) görünümü ---------- */
  function hucre(x, pos) {
    var st = stilBil(x.stil), sv = sevBil(x.sev);
    if (etkinlikMi(x)) {
      var z = zemin(sv.renk) || zemin(st.renk) || zemin('#1B2E4A');
      var alt = x.n ? x.n.split(/\s*·\s*|\n/).map(function (s) { return '<small>' + esc(s) + '</small>'; }).join('') : '';
      var ust = x.sev && !/^event$/i.test(sv.ad) ? sv.ad : (x.stil && !/^(party|free time)$/i.test(st.ad) ? st.ad : '');
      return '<div class="e' + (z.acik ? ' acik' : '') + '" data-i="' + x.id + '" lang="en" style="' + pos + ';background:' + z.bg + ';color:' + z.yazi + '">' +
        (ust ? '<s>' + esc(ust) + '</s>' : '') + '<b>' + esc(x.konu || x.stil) + '</b>' + alt + '</div>';
    }
    var k = zemin(st.renk) || zemin(GRI), sz = zemin(sv.renk);
    return '<div class="w" data-i="' + x.id + '" style="' + pos + ';--k:' + k.ana + ';--kt:' + k.yazi + '">' +
      '<span class="ch"><s lang="en">' + esc(st.ad || '—') + '</s>' + (x.sev ? '<u lang="en"' + (sz ? ' style="--sv:' + sz.ana + '"' : '') + '>' + esc(sv.ad) + '</u>' : '') + '</span>' +
      '<b lang="en">' + esc(x.konu || st.ad) + '</b><em>' + (x.eg ? esc(x.eg) : 'Eğitmen TBA') + '</em>' + (x.n ? '<em>' + esc(x.n) + '</em>' : '') + '</div>';
  }
  function gunTablo(liste) {
    if (!liste.length) return '<div class="bos">Bu günün programı yakında açıklanacak.</div>';
    var S = L.salon, kul = {};
    liste.forEach(function (x) {
      var a = S.indexOf(x.s1), b = x.s2 && S.indexOf(x.s2) >= 0 ? S.indexOf(x.s2) : a;
      for (var i = Math.min(a, b); i <= Math.max(a, b); i++) kul[i] = 1;
    });
    var cols = S.filter(function (_, i) { return kul[i]; });
    var bl = [];
    liste.forEach(function (x) { if (bl.indexOf(x.b) < 0) bl.push(x.b); });
    bl.sort(function (a, b) { return dk(a) - dk(b); });
    var n = cols.length;
    var h = '<div class="sc"><div class="g" style="grid-template-columns:76px repeat(' + n + ',minmax(150px,1fr));min-width:' + (76 + n * 154) + 'px">';
    h += '<div class="th c0" style="grid-row:1;grid-column:1">SAAT</div>';
    cols.forEach(function (c, i) { h += '<div class="th" style="grid-row:1;grid-column:' + (i + 2) + '">' + esc(c) + '</div>'; });
    bl.forEach(function (b, r) {
      var son = liste.filter(function (x) { return x.b === b && x.e; }).map(function (x) { return x.e; }).sort(function (p, q) { return dk(p) - dk(q); })[0];
      h += '<div class="tm" style="grid-row:' + (r + 2) + '">' + b + '<span>' + (son || '…') + '</span></div>';
    });
    liste.forEach(function (x) {
      var r0 = bl.indexOf(x.b), r1 = bl.length - 1;
      if (x.e) { r1 = r0; for (var i = r0; i < bl.length; i++) if (dk(bl[i]) < dk(x.e)) r1 = i; }
      var c0 = cols.indexOf(x.s1), c1 = x.s2 && cols.indexOf(x.s2) >= 0 ? cols.indexOf(x.s2) : c0;
      if (c1 < c0) { var t = c0; c0 = c1; c1 = t; }
      h += hucre(x, 'grid-row:' + (r0 + 2) + ' / span ' + (r1 - r0 + 1) + ';grid-column:' + (c0 + 2) + ' / span ' + (c1 - c0 + 1));
    });
    return h + '</div></div>';
  }

  /* ---------- Liste görünümü (telefon için) ---------- */
  function gunListe(liste) {
    var S = L.salon, q = sorgu(), fv = filtreVar();
    if (!liste.length) return '<div class="bos">Bu günün programı yakında açıklanacak.</div>';
    var l = liste.filter(function (x) { return !fv || eslesir(x, q); }).sort(function (a, b) { return dk(a.b) - dk(b.b) || S.indexOf(a.s1) - S.indexOf(b.s1); });
    if (!l.length) return '<div class="bos">Bu günde seçimine uyan program yok. Diğer günlere bak ya da filtreyi değiştir.</div>';
    var h = '<div class="li">', son = '';
    l.forEach(function (x) {
      var st = stilBil(x.stil), sv = sevBil(x.sev), etk = etkinlikMi(x);
      var z = etk ? (zemin(sv.renk) || zemin(st.renk) || zemin('#1B2E4A')) : (zemin(st.renk) || zemin(GRI)), sz = zemin(sv.renk);
      if (x.b !== son) { h += '<div class="lt">' + x.b + '</div>'; son = x.b; }
      var sal = esc(x.s1) + (x.s2 && x.s2 !== x.s1 ? ' – ' + esc(x.s2.replace('SALON ', '')) : '');
      h += '<div class="lr' + (etk ? ' le' : '') + '" data-i="' + x.id + '" style="--k:' + z.ana + '">' +
        '<div class="ls">' + sal + '<span>' + x.b + (x.e ? '–' + x.e : '') + '</span></div>' +
        '<div class="lm"><span class="ch" style="--kt:' + z.yazi + '"><s lang="en">' + esc(st.ad || '—') + '</s>' + (x.sev && !/^event$/i.test(sv.ad) ? '<u lang="en"' + (sz ? ' style="--sv:' + sz.ana + '"' : '') + '>' + esc(sv.ad) + '</u>' : '') + '</span>' +
        '<b lang="en">' + esc(x.konu || st.ad) + '</b>' + (etk ? '' : '<em>' + (x.eg ? esc(x.eg) : 'Eğitmen TBA') + '</em>') + (x.n ? '<small>' + esc(x.n) + '</small>' : '') + '</div></div>';
    });
    return h + '</div>';
  }

  /* ---------- Filtre çipleri (Stil + Seviye, çoklu seçim) ---------- */
  function cipler() {
    var vs = {}, vv = {};
    rows.forEach(function (x) {
      if (x.stil) vs[bas(x.stil)] = (vs[bas(x.stil)] || 0) + 1;
      if (x.sev && !etkinlikMi(x)) vv[bas(x.sev)] = (vv[bas(x.sev)] || 0) + 1;
    });
    function liste(o, bil) {
      return Object.keys(o).map(function (k) { var s = bil(k); return { k: k, ad: s.ad || k, renk: s.renk, etk: s.etk ? 1 : 0, i: s.i, n: o[k] }; })
        .sort(function (a, b) { return (a.etk - b.etk) || (a.i - b.i) || (a.ad > b.ad ? 1 : -1); });
    }
    function cip(t, x, sec) {
      var z = zemin(x.renk) || zemin(GRI), on = !!sec[x.k];
      return '<button type="button" lang="en" data-t="' + t + '" data-k="' + esc(x.k) + '" aria-pressed="' + on + '"' + (on ? ' class="on"' : '') +
        ' style="--k:' + z.ana + ';--kt:' + z.yazi + '"><i></i>' + esc(x.ad) + '<small>' + x.n + '</small></button>';
    }
    var ss = liste(vs, stilBil), sv = liste(vv, sevBil);
    fl.innerHTML = '<div class="fr"><b>Stil</b><div class="cp">' + ss.map(function (x) { return cip('s', x, fStil); }).join('') + '</div></div>' +
      (sv.length ? '<div class="fr"><b>Seviye</b><div class="cp">' + sv.map(function (x) { return cip('v', x, fSev); }).join('') + '</div></div>' : '');
  }
  fl.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var o = b.getAttribute('data-t') === 's' ? fStil : fSev, k = b.getAttribute('data-k');
    if (o[k]) delete o[k]; else o[k] = 1;
    b.classList.toggle('on', !!o[k]); b.setAttribute('aria-pressed', !!o[k]);
    uygula();
  });

  /* ---------- Çizim ---------- */
  function gunSatir(gi) { var g = L.gun[gi]; return g ? rows.filter(function (x) { return bas(x.gun) === bas(g[0]); }) : []; }
  function panelCiz(gi) {
    var pn = pns.children[gi]; if (!pn) return;
    pn.innerHTML = gorunum === 'liste' ? gunListe(gunSatir(gi)) : gunTablo(gunSatir(gi));
    pn.setAttribute('data-v', gorunum);
  }
  function ciz(veri) {
    var yeni = JSON.stringify(veri);
    if (yeni === imza) return;
    imza = yeni;
    hazirla(veri.listeler || {});
    rows = temizle(veri.rows || []); rows.forEach(function (x, i) { x.id = i; });
    if (aktif >= L.gun.length) aktif = 0;
    tabs.innerHTML = L.gun.map(function (g, i) {
      return '<button type="button" role="tab" aria-selected="' + (i === aktif) + '" class="' + (i === aktif ? 'on' : '') + '" data-i="' + i + '">' + esc(g[0]) + '<small>' + esc(g[1] || '') + '</small></button>';
    }).join('');
    pns.innerHTML = L.gun.map(function (_, i) { return '<div class="pn" role="tabpanel"' + (i === aktif ? '' : ' hidden') + '></div>'; }).join('');
    /* tablodan kalkan stil/seviye seçiliyse bırak */
    var var_ = {}; rows.forEach(function (x) { var_['s:' + bas(x.stil)] = 1; var_['v:' + bas(x.sev)] = 1; });
    Object.keys(fStil).forEach(function (k) { if (!var_['s:' + k]) delete fStil[k]; });
    Object.keys(fSev).forEach(function (k) { if (!var_['v:' + k]) delete fSev[k]; });
    cipler();
    uygula();
  }
  function gec(i) {
    aktif = i;
    [].forEach.call(tabs.children, function (x, k) { x.classList.toggle('on', k === aktif); x.setAttribute('aria-selected', k === aktif); });
    [].forEach.call(pns.children, function (x, k) { x.hidden = k !== aktif; });
    var pn = pns.children[aktif];
    if (pn && (gorunum === 'liste' || pn.getAttribute('data-v') !== gorunum)) panelCiz(aktif);
    isaretle();
  }
  tabs.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) gec(+b.getAttribute('data-i')); });

  function isaretle() {
    var q = sorgu(), fv = filtreVar(), pn = pns.children[aktif];
    R.classList.toggle('arama', fv && gorunum !== 'liste');
    if (gorunum === 'liste') [].forEach.call(R.querySelectorAll('.hit'), function (c) { c.classList.remove('hit'); });
    if (pn && gorunum !== 'liste') [].forEach.call(pn.querySelectorAll('[data-i]'), function (c) { c.classList.toggle('hit', fv && eslesir(rows[+c.getAttribute('data-i')], q)); });
  }
  function uygula() {
    var q = sorgu(), fv = filtreVar(), bul = [];
    if (fv) rows.forEach(function (x) { if (eslesir(x, q)) bul.push(x); });
    var say = L.gun.map(function (g) { return bul.filter(function (x) { return bas(x.gun) === bas(g[0]); }).length; });
    L.gun.forEach(function (g, gi) {
      var tb = tabs.children[gi]; if (!tb) return;
      var i = tb.querySelector('i'); if (i) tb.removeChild(i);
      if (fv) { i = document.createElement('i'); i.textContent = say[gi]; if (!say[gi]) i.className = 'z'; tb.appendChild(i); }
    });
    if (gb) gb.hidden = !fv;
    /* Liste görünümü filtreye göre yeniden çizilir; tabloda sadece vurgulanır */
    [].forEach.call(pns.children, function (p, k) { if (k !== aktif && gorunum === 'liste') p.removeAttribute('data-v'); });
    var pn = pns.children[aktif];
    if (pn && (gorunum === 'liste' || pn.getAttribute('data-v') !== gorunum)) panelCiz(aktif);
    isaretle();
    if (!fv) { sonuc.innerHTML = ''; return; }
    if (!bul.length) { sonuc.innerHTML = '<p>Sonuç yok.' + (q ? ' İsmi farklı yazmayı dene; eğitmenler açıklandıkça program güncelleniyor.' : ' Filtreyi değiştirmeyi dene.') + '</p>'; return; }
    var ozet = '<p>' + bul.length + ' sonuç · ' + L.gun.map(function (g, i) { return say[i] ? esc(g[0]) + ' ' + say[i] : ''; }).filter(Boolean).join(' · ') + '</p>';
    if (!q || gorunum === 'liste') { sonuc.innerHTML = ozet; return; }
    sonuc.innerHTML = ozet + bul.slice(0, 40).map(function (x) {
      var gi = L.gun.map(function (g) { return bas(g[0]); }).indexOf(bas(x.gun));
      return '<button type="button" data-i="' + x.id + '" data-g="' + gi + '"><b>' + esc(x.gun) + ' ' + x.b + '</b><span>' + esc(x.s1) + '</span><strong lang="en">' + esc(x.konu || x.stil) + '</strong>' + (x.eg ? '<em>' + esc(x.eg) + '</em>' : '') + '</button>';
    }).join('');
  }
  sonuc.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    gec(+b.getAttribute('data-g'));
    var el = pns.children[aktif].querySelector('[data-i="' + b.getAttribute('data-i') + '"]'); if (!el) return;
    el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
    el.classList.remove('flas'); void el.offsetWidth; el.classList.add('flas');
  });
  if (kutu) kutu.addEventListener('input', uygula);
  if (gb) gb.addEventListener('click', function () { fStil = {}; fSev = {}; if (kutu) kutu.value = ''; cipler(); uygula(); });

  /* Görünüm: Tablo / Liste (dar ekranda liste varsayılan; seçim hatırlanır) */
  function gorunumYap(v, kaydet) {
    gorunum = v;
    R.setAttribute('data-gorunum', v);
    if (gv) [].forEach.call(gv.querySelectorAll('button'), function (b) { var on = b.getAttribute('data-v') === v; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); });
    if (kaydet) try { localStorage.setItem('edf-prog-gorunum', v); } catch (e) {}
  }
  var kayit = ''; try { kayit = localStorage.getItem('edf-prog-gorunum') || ''; } catch (e) {}
  gorunumYap(kayit === 'liste' || kayit === 'tablo' ? kayit : ((R.clientWidth || window.innerWidth) < 640 ? 'liste' : 'tablo'));
  if (gv) gv.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b || b.getAttribute('data-v') === gorunum) return;
    gorunumYap(b.getAttribute('data-v'), true); uygula();
  });

  /* 1) Gömülü kopya: anında */
  try { ciz(JSON.parse(R.querySelector('.veri').textContent)); } catch (e) {}

  /* 2) Canlı tablo: önce Listeler, sonra günler (sütunlar başlık adıyla bulunur) */
  var id = R.getAttribute('data-sheet');
  function gviz(ad) {
    return fetch('https://docs.google.com/spreadsheets/d/' + id + '/gviz/tq?tqx=out:json&headers=1&sheet=' + encodeURIComponent(ad))
      .then(function (r) { return r.text(); })
      .then(function (t) {
        var j = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
        if (j.status === 'error') throw new Error(ad);
        return { lab: j.table.cols.map(function (c) { return bas(c.label); }),
          rows: (j.table.rows || []).map(function (r) { return (r.c || []).map(function (c) { return c ? (c.f != null ? c.f : (c.v != null ? String(c.v) : '')) : ''; }); }) };
      });
  }
  function sutun(t, adlar) { for (var i = 0; i < adlar.length; i++) { var k = t.lab.indexOf(adlar[i]); if (k >= 0) return k; } return -1; }
  function al(r, k) { return k >= 0 ? trim(r[k]) : ''; }
  if (id && window.fetch && window.Promise) {
    gviz('Listeler').then(function (t) {
      var c = {};
      ['stil', 'stil türü', 'stil rengi', 'seviye', 'seviye türü', 'seviye rengi', 'salon', 'gün', 'tarih'].forEach(function (a) { c[a] = sutun(t, [a]); });
      var l = { stil: [], seviye: [], salon: [], gun: [] };
      t.rows.forEach(function (r) {
        if (al(r, c['stil'])) l.stil.push([al(r, c['stil']), al(r, c['stil türü']), al(r, c['stil rengi'])]);
        if (al(r, c['seviye'])) l.seviye.push([al(r, c['seviye']), al(r, c['seviye türü']), al(r, c['seviye rengi'])]);
        if (al(r, c['salon'])) l.salon.push(al(r, c['salon']));
        if (al(r, c['gün'])) l.gun.push([al(r, c['gün']), al(r, c['tarih'])]);
      });
      if (!l.stil.length || !l.salon.length || !l.gun.length) throw new Error('liste');
      return Promise.all(l.gun.map(function (g) {
        return gviz(g[0]).then(function (t) {
          var k = { b: sutun(t, ['başlangıç']), e: sutun(t, ['bitiş']), s1: sutun(t, ['salon']), s2: sutun(t, ['bitiş salonu']), stil: sutun(t, ['stil']),
            konu: sutun(t, ['konu', 'başlık']), sev: sutun(t, ['seviye', 'kategori']), eg: sutun(t, ['eğitmen']), n: sutun(t, ['not']) };
          if (k.stil < 0 || k.konu < 0) throw new Error('eski düzen');  /* eski sütun düzeni: gömülü kopya kalsın */
          return t.rows.map(function (r) { return [g[0], al(r, k.b), al(r, k.e), al(r, k.s1), al(r, k.s2), al(r, k.stil), al(r, k.konu), al(r, k.sev), al(r, k.eg), al(r, k.n)]; });
        });
      })).then(function (gunler) {
        var hep = [].concat.apply([], gunler);
        if (hep.length) ciz({ listeler: l, rows: hep });
      });
    }).catch(function () {});
  }
})();
