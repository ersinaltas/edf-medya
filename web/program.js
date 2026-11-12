/* EDF workshop programı. Google E-Tablo'da her gün ayrı sekme; satırlar (Başlangıç, Bitiş, Salon, Bitiş Salonu, Başlık, Eğitmen, Kategori, Not) gün adıyla birleştirilip (Gün, Başlangıç, Bitiş, Salon, Bitiş Salonu, Başlık, Eğitmen, Kategori, Not)
   gün sekmeli ızgara çizer. Önce sayfaya gömülü kopyayı çizer, sonra Google E-Tablo'yu canlı okur; fark varsa yeniden çizer. */
(function () {
  var hepsi = document.querySelectorAll('#edf-prog');
  var R = hepsi[hepsi.length - 1];
  if (!R || R.getAttribute('data-ok')) return;
  R.setAttribute('data-ok', '1');

  var GUN = [['Çarşamba', '3 Şubat'], ['Perşembe', '4 Şubat'], ['Cuma', '5 Şubat'], ['Cumartesi', '6 Şubat'], ['Pazar', '7 Şubat']];
  var SALON = ['SALON 1', 'SALON 2', 'SALON 3', 'SALON 4', 'SALON 5', 'SALON 6', 'SALON 7', 'DIŞ ALAN'];
  var KAT = { 'Beginner': 'beg', 'Intermediate': 'int', 'All Level': 'all', 'Advanced': 'adv', 'Hip Hop & Free Style': 'hh',
    'Lindy Hop / Jazz': 'lindy', 'Zumba': 'zumba', 'K-Pop': 'kpop', 'Kids': 'kids', 'Competition': 'comp', 'Party': 'party',
    'Sunset Party': 'sunset', 'Red Bull': 'redbull', 'Free Time': 'free', 'Show / Rehearsal': 'rehearsal' };
  var HEP_ETKINLIK = { party: 1, sunset: 1, redbull: 1, free: 1, rehearsal: 1 };
  var ETK_KELIME = /party|arena|cup|battle|match|play|show|final/i;
  var aktif = 1;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function saat(t) { var m = String(t || '').match(/(\d{1,2})[:.](\d{2})/); return m ? ('0' + m[1]).slice(-2) + ':' + m[2] : ''; }
  function dk(t) { var p = t.split(':'), h = +p[0]; return (h < 6 ? h + 24 : h) * 60 + (+p[1]); }
  function bas(s) { return String(s || '').trim().toLocaleLowerCase('tr'); }

  function temizle(rows) {
    return rows.map(function (r) {
      return { gun: String(r[0] || '').trim(), b: saat(r[1]), e: saat(r[2]), s1: String(r[3] || '').trim().toUpperCase(),
        s2: String(r[4] || '').trim().toUpperCase(), t: String(r[5] || '').trim(), eg: String(r[6] || '').trim(),
        k: String(r[7] || '').trim(), n: String(r[8] || '').trim() };
    }).filter(function (x) { return x.gun && x.b && x.t && SALON.indexOf(x.s1) >= 0; });
  }

  function gunCiz(liste) {
    if (!liste.length) return '<div class="bos">Bu günün programı yakında açıklanacak.</div>';
    /* Sütunlar: kullanılan salonlar (birleşik hücrelerin arasındakiler dahil) */
    var kul = {};
    liste.forEach(function (x) {
      var a = SALON.indexOf(x.s1), b = x.s2 && SALON.indexOf(x.s2) >= 0 ? SALON.indexOf(x.s2) : a;
      for (var i = Math.min(a, b); i <= Math.max(a, b); i++) kul[i] = 1;
    });
    var cols = SALON.filter(function (_, i) { return kul[i]; });
    /* Satırlar: farklı başlangıç saatleri */
    var bl = [];
    liste.forEach(function (x) { if (bl.indexOf(x.b) < 0) bl.push(x.b); });
    bl.sort(function (a, b) { return dk(a) - dk(b); });
    var n = cols.length;
    var h = '<div class="sc"><div class="g" style="grid-template-columns:86px repeat(' + n + ',minmax(140px,1fr));min-width:' + (86 + n * 144) + 'px">';
    h += '<div class="th c0" style="grid-row:1;grid-column:1">SAAT</div>';
    cols.forEach(function (c, i) { h += '<div class="th" style="grid-row:1;grid-column:' + (i + 2) + '">' + esc(c) + '</div>'; });
    bl.forEach(function (b, r) {
      var son = liste.filter(function (x) { return x.b === b && x.e; }).map(function (x) { return x.e; })
        .sort(function (p, q) { return dk(p) - dk(q); })[0];
      h += '<div class="tm" style="grid-row:' + (r + 2) + '">' + b + '<br>' + (son || '…') + '</div>';
    });
    liste.forEach(function (x) {
      var r0 = bl.indexOf(x.b), r1 = bl.length - 1;
      if (x.e) { r1 = r0; for (var i = r0; i < bl.length; i++) if (dk(bl[i]) < dk(x.e)) r1 = i; }
      var c0 = cols.indexOf(x.s1), c1 = x.s2 && cols.indexOf(x.s2) >= 0 ? cols.indexOf(x.s2) : c0;
      if (c1 < c0) { var tmp = c0; c0 = c1; c1 = tmp; }
      var pos = 'grid-row:' + (r0 + 2) + ' / span ' + (r1 - r0 + 1) + ';grid-column:' + (c0 + 2) + ' / span ' + (c1 - c0 + 1);
      var k = KAT[x.k] || 'party';
      var etk = HEP_ETKINLIK[k] || (!x.eg && /^(comp|kids|hh|kpop)$/.test(k) && ETK_KELIME.test(x.t));
      if (etk) {
        var cls = k + (/arena/i.test(x.t) ? ' arena' : '');
        var alt = x.n ? x.n.split(/\s*·\s*|\n/).map(function (s) { return '<small>' + esc(s) + '</small>'; }).join('') : '';
        h += '<div class="e ' + cls + '" style="' + pos + '">' + esc(x.t) + alt + '</div>';
      } else {
        h += '<div class="w k-' + k + '" style="' + pos + '"><s lang="en">' + esc(x.k) + '</s><b>' + esc(x.t) + '</b><em>' + (x.eg ? esc(x.eg) : 'Eğitmen TBA') + '</em>' +
          (x.n ? '<em>' + esc(x.n) + '</em>' : '') + '</div>';
      }
    });
    return h + '</div></div>';
  }

  var tabs = R.querySelector('.tabs'), pns = R.querySelector('.pns'), imza = '';
  function ciz(rows) {
    var v = temizle(rows), yeni = JSON.stringify(v);
    if (yeni === imza) return;
    imza = yeni;
    tabs.innerHTML = GUN.map(function (g, i) {
      return '<button type="button" class="' + (i === aktif ? 'on' : '') + '" data-i="' + i + '">' + g[0] + '<small>' + g[1] + '</small></button>';
    }).join('');
    pns.innerHTML = GUN.map(function (g, i) {
      return '<div class="pn"' + (i === aktif ? '' : ' hidden') + '>' + gunCiz(v.filter(function (x) { return bas(x.gun) === bas(g[0]); })) + '</div>';
    }).join('');
  }
  tabs.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    aktif = +b.getAttribute('data-i');
    [].forEach.call(tabs.children, function (x, i) { x.classList.toggle('on', i === aktif); });
    [].forEach.call(pns.children, function (x, i) { x.hidden = i !== aktif; });
  });

  /* 1) Gömülü kopya: anında */
  try { ciz(JSON.parse(R.querySelector('.veri').textContent)); } catch (e) {}

  /* 2) Canlı tablo: Google E-Tablo, her gün kendi sekmesinde (tablo link ile görüntülenebilir olmalı) */
  var id = R.getAttribute('data-sheet');
  if (id && window.fetch && window.Promise) {
    Promise.all(GUN.map(function (g) {
      return fetch('https://docs.google.com/spreadsheets/d/' + id + '/gviz/tq?tqx=out:json&headers=1&sheet=' + encodeURIComponent(g[0]))
        .then(function (r) { return r.text(); })
        .then(function (t) {
          var j = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
          if (j.status === 'error') throw new Error('sekme');
          return (j.table.rows || []).map(function (r) {
            return [g[0]].concat((r.c || []).map(function (c) { return c ? (c.f != null ? c.f : (c.v != null ? String(c.v) : '')) : ''; }));
          });
        });
    })).then(function (gunler) {
      var rows = [].concat.apply([], gunler);
      if (rows.length) ciz(rows);
    }).catch(function () {});
  }
})();
