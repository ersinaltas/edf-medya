/* EDF artist sayfası. HTML'deki ızgara kartlarından öne çıkanları, akan şeritleri ve story penceresini kurar. */
(function () {
  var R = document.getElementById('edf-art');
  if (!R || R.dataset.ok) return;
  R.dataset.ok = '1';
  R.classList.add('js');
  var B = R.dataset.base || '';
  var G = [].slice.call(R.querySelectorAll('.gr .cd'));
  var hover = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches;

  function vid(a) { return B + a.dataset.id + '.mp4'; }
  function big(a) { return B + a.dataset.id + '.jpg'; }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  /* Durdur, başa sar, afiş görseline geri dön */
  function stop(v) { if (!v) return; v.pause(); try { v.currentTime = 0; } catch (e) {} v.classList.remove('ok'); }
  function fv(e) {
    var v = e.querySelector('video');
    if (!v) {
      v = document.createElement('video');
      v.muted = true; v.loop = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'none';
      v.poster = e.querySelector('img').src; v.src = vid(e);
      v.addEventListener('playing', function () { v.classList.add('ok'); });
      e.insertBefore(v, e.querySelector('.tg'));
    }
    return v;
  }
  function clone(a, full) {
    var n = a.cloneNode(true);
    if (full) { var im = n.querySelector('img'); im.src = big(a); im.removeAttribute('width'); im.removeAttribute('height'); }
    return n;
  }

  /* Öne çıkanlar: sadece ortadaki kartın videosu iner ve oynar */
  var t = R.querySelector('.ft'), dw = R.querySelector('.dots');
  G.filter(function (a) { return a.hasAttribute('data-f'); }).forEach(function (a) { t.appendChild(clone(a, true)); });
  var c = [].slice.call(t.children), i = -1, tm;
  if (!c.length) { /* öne çıkan yoksa bölümü gizle */
    [t.closest('.fw'), dw, R.querySelector('.jso .st')].forEach(function (e) { if (e) e.style.display = 'none'; });
  }
  dw.innerHTML = c.map(function () { return '<b></b>'; }).join('');
  var d = [].slice.call(dw.children);
  function mark() {
    if (!c.length) return;
    var m = t.scrollLeft + t.clientWidth / 2, b = 0, bd = 1e9;
    c.forEach(function (e, k) { var x = Math.abs(e.offsetLeft + e.offsetWidth / 2 - m); if (x < bd) { bd = x; b = k; } });
    if (b === i) return; i = b;
    c.forEach(function (e, k) { e.classList.toggle('on', k === b); if (k === b) play(fv(e)); else stop(e.querySelector('video')); });
    d.forEach(function (e, k) { e.classList.toggle('on', k === b); });
  }
  function go(k) { if (!c.length) return; k = (k + c.length) % c.length; var e = c[k]; t.scrollTo({ left: e.offsetLeft - (t.clientWidth - e.offsetWidth) / 2, behavior: 'smooth' }); }
  function auto() { clearInterval(tm); tm = setInterval(function () { if (!sv.classList.contains('op')) go(i + 1); }, 5000); }
  t.addEventListener('scroll', function () { requestAnimationFrame(mark); }, { passive: true });
  R.querySelector('.ar.n').onclick = function () { go(i + 1); auto(); };
  R.querySelector('.ar.p').onclick = function () { go(i - 1); auto(); };
  d.forEach(function (e, k) { e.onclick = function () { go(k); auto(); }; });
  t.addEventListener('pointerdown', function () { clearInterval(tm); });
  t.addEventListener('mouseenter', function () { clearInterval(tm); });
  t.addEventListener('mouseleave', auto);

  /* Akan şeritler: ızgaradaki küçük görsellerin kopyası */
  var rows = R.querySelectorAll('.mq .rw'), half = Math.ceil(G.length / 2);
  [G.slice(0, half), G.slice(half)].forEach(function (grp, k) {
    var rw = rows[k]; if (!rw) return;
    for (var r = 0; r < 2; r++) grp.forEach(function (a) { var n = clone(a); n.setAttribute('tabindex', '-1'); if (r) n.setAttribute('aria-hidden', 'true'); rw.appendChild(n); });
  });

  /* Izgara: masaüstünde üstüne gelince video oynar, telefonda veri harcamaz */
  if (hover) G.forEach(function (a) {
    a.addEventListener('mouseenter', function () { var v = fv(a); try { v.currentTime = 0; } catch (e) {} play(v); });
    a.addEventListener('mouseleave', function () { stop(a.querySelector('video')); });
  });

  /* Story penceresi */
  var old = document.getElementById('edf-sv'); if (old) old.parentNode.removeChild(old);
  var sv = document.createElement('div'); sv.id = 'edf-sv';
  sv.innerHTML = '<button class="nb p" type="button" aria-label="Önceki">‹</button><div class="box"><div class="pb"></div><video muted playsinline></video><button class="tz l" type="button" aria-label="Önceki"></button><button class="tz r" type="button" aria-label="Sonraki"></button><button class="x" type="button" aria-label="Kapat">✕</button></div><button class="nb n" type="button" aria-label="Sonraki">›</button>';
  document.body.appendChild(sv);
  var vv = sv.querySelector('video'), pb = sv.querySelector('.pb'), L = [], j = 0, raf, many = false;
  function bars() { many = L.length > 20; pb.innerHTML = many ? '<i><b></b></i>' : L.map(function (_, k) { return '<i class="' + (k < j ? 'dn' : '') + '"><b></b></i>'; }).join(''); }
  function tick() { var x = pb.children[many ? 0 : j]; if (x && vv.duration) x.firstChild.style.width = (vv.currentTime / vv.duration * 100) + '%'; raf = requestAnimationFrame(tick); }
  function show(k) { if (k < 0) k = 0; if (k >= L.length) { close(); return; } j = k; bars(); var a = L[j]; vv.poster = big(a); vv.src = vid(a); play(vv); }
  function open(list, a) { L = list; sv.classList.add('op'); document.documentElement.style.overflow = 'hidden'; show(Math.max(0, L.indexOf(a))); cancelAnimationFrame(raf); tick(); }
  function close() { sv.classList.remove('op'); vv.pause(); vv.removeAttribute('src'); vv.load(); cancelAnimationFrame(raf); document.documentElement.style.overflow = ''; }
  vv.addEventListener('ended', function () { show(j + 1); });
  sv.querySelector('.tz.l').onclick = sv.querySelector('.nb.p').onclick = function () { show(j - 1); };
  sv.querySelector('.tz.r').onclick = sv.querySelector('.nb.n').onclick = function () { show(j + 1); };
  sv.querySelector('.x').onclick = close;
  sv.addEventListener('click', function (e) { if (e.target === sv) close(); });
  document.addEventListener('keydown', function (e) {
    if (!sv.classList.contains('op')) return;
    if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(j + 1); if (e.key === 'ArrowLeft') show(j - 1);
  });
  R.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.cd'); if (!a) return;
    e.preventDefault();
    if (a.closest('.ft')) { clearInterval(tm); open(c, a); return; }
    var list = G.filter(function (x) { return x.offsetParent !== null; });
    var g = G.filter(function (x) { return x.dataset.id === a.dataset.id; })[0];
    open(list.indexOf(g) < 0 ? G : list, g);
  });

  setTimeout(function () { mark(); go(0); auto(); }, 300);
})();
