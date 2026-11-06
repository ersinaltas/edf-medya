"""artistler.json'dan ikas'a yapıştırılacak artist sayfası HTML'ini üretir.
Kullanım: python3 tools/sayfa_uret.py embed|artifact CIKTI.html MEDYA_BASE_URL"""
import sys, html, re, json, os
mode=sys.argv[1]; out=sys.argv[2]; base=sys.argv[3]
MAN=os.path.join(os.path.dirname(__file__),'..','artistler.json')
# Branş: Drive klasör adı -> (etiket, çerçeve rengi, etiket yazı rengi)
BR={'Salsa':('SALSA','#E44351','#fff'),'Bachata':('BACHATA','#29649D','#fff'),'Kizomba':('KIZOMBA','#EF6A64','#fff'),
    'Hip Hop':('HIP HOP','#41B8A6','#fff'),'Heels':('HEELS','#FF5994','#fff'),'Oryantal':('ORYANTAL','#B04FD9','#fff'),
    'Zumba':('ZUMBA','#3CB44B','#fff'),'DJ':('DJ','#F0E559','#1B2E4A'),'Organizer Promoter':('ORGANİZATÖR','#DDE3EA','#1B2E4A')}
SIRA=list(BR)
def slug(b): return re.sub(r'[^a-z0-9]+','-',b.lower()).strip('-') or 'x'
A=[dict(id=a['id'],n=a['ad'],b=a['brans'],f=a['one_cikan']) for a in json.load(open(MAN))]
for a in A:
    if a['b'] and a['b'] not in BR: BR[a['b']]=(a['b'].upper(),'#9B7BD4','#fff'); SIRA.append(a['b'])
TR=str.maketrans('ÇĞİIÖŞÜ','CGIIOSU')
def key(a): return a['n'].translate(TR)
grid=sorted(A,key=key)
feat=[a for a in A if a['f']]
E=html.escape
def card(a,cls='',video=False):
    b=a['b']; lab,col,fg=BR.get(b,('','',''))
    st=f' style="--c:{col};--cf:{fg}"' if col else ''
    tag=f'<span class="tg">{lab}</span>' if lab else ''
    v=f'<video muted loop playsinline preload="none" poster="{base}{a["id"]}.jpg" data-src="{base}{a["id"]}.mp4"></video>' if video else ''
    return (f'<a class="cd b-{slug(b)} {cls}" href="{base}{a["id"]}.mp4" data-id="{a["id"]}" data-n="{E(a["n"])}"{st}>'
            f'<img src="{base}{a["id"]}.jpg" alt="{E(a["n"])} – EDF 2027 artist afişi" loading="lazy" decoding="async">{v}{tag}<span class="pl">▶</span></a>')
brs=[b for b in SIRA if any(a['b']==b for a in A)]
wrap = "max-width:1200px;margin:24px auto;border-radius:16px;"
css=f'''
#edf-art{{--nv:#1B2E4A;--rd:#E44351;--bl:#29649D;--ye:#F0E559;--sa:#EF6A64;--bg:#F6F4EF;--ink:#1B2E4A;--g:max(16px,env(safe-area-inset-left,0px));
 font-family:'Montserrat',system-ui,sans-serif;color:var(--ink);background:var(--bg);box-sizing:border-box;{wrap}overflow:hidden;border-right:14px solid var(--rd)}}
'''+r'''
#edf-art *{box-sizing:border-box}
#edf-art a{color:inherit;text-decoration:none}
#edf-art .pad{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(24px,env(safe-area-inset-right,0px))}
#edf-art .hero{padding-block:44px 18px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px}
#edf-art h1{margin:0;font-weight:900;font-size:clamp(36px,5.5vw,72px);line-height:.9;letter-spacing:-.02em;text-transform:uppercase;text-wrap:balance}
#edf-art h1 span{color:var(--rd);display:block}
#edf-art .hero p{margin:0;max-width:390px;font-weight:600;font-size:14px;line-height:1.5}
#edf-art .hero p b{display:block;font-weight:900;font-size:clamp(16px,1.8vw,22px);color:var(--rd);margin-bottom:6px;text-transform:uppercase;letter-spacing:.01em}
#edf-art .up{animation:edfUp .8s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,0ms)}
@keyframes edfUp{from{opacity:.001;transform:translateY(24px)}}
#edf-art .band{background:var(--nv);color:#fff;overflow:hidden;white-space:nowrap;padding:12px 0;transform:rotate(-1.2deg);margin:14px -10px 8px}
#edf-art .band div{display:inline-block;animation:edfMq 30s linear infinite;font-weight:900;font-size:clamp(14px,1.6vw,20px);letter-spacing:.06em}
#edf-art .band i{font-style:normal;color:var(--ye);margin:0 18px}
@keyframes edfMq{to{transform:translateX(-50%)}}
#edf-art .st{display:flex;align-items:baseline;gap:12px;padding-block:38px 4px;font-weight:900;font-size:clamp(18px,2.2vw,28px);text-transform:uppercase}
#edf-art .st:after{content:"";flex:1;height:3px;background:var(--nv);opacity:.15;align-self:center}
#edf-art .st small{font-size:12px;font-weight:700;opacity:.6;text-transform:none}
/* card */
#edf-art .cd{position:relative;display:block;aspect-ratio:9/16;max-width:100%;border-radius:12px;overflow:hidden;background:#24364f;
 outline:3px solid var(--c,transparent);outline-offset:-3px;box-shadow:0 10px 26px rgba(27,46,74,.2);transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
#edf-art .cd img,#edf-art .cd video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#edf-art .cd video{opacity:0;transition:opacity .4s}
#edf-art .cd video.ok{opacity:1}
#edf-art .cd .tg{position:absolute;top:10px;left:0;writing-mode:vertical-rl;transform:rotate(180deg);background:var(--c);color:var(--cf,#fff);font-weight:800;font-size:10px;letter-spacing:.08em;padding:8px 4px;border-radius:4px 0 0 4px;z-index:2;box-shadow:0 2px 8px rgba(0,0,0,.25)}
#edf-art .cd .pl{position:absolute;left:50%;top:50%;width:54px;height:54px;margin:-27px 0 0 -27px;border-radius:50%;background:rgba(228,67,81,.92);color:#fff;display:grid;place-items:center;font-size:20px;padding-left:4px;opacity:0;transform:scale(.7);transition:all .25s;z-index:2}
#edf-art .cd:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(27,46,74,.3)}
#edf-art .cd:hover .pl,#edf-art .cd:focus-visible .pl{opacity:1;transform:none}
#edf-art .cd:focus-visible{outline:3px solid var(--rd);outline-offset:3px}
/* featured */
#edf-art .fw{position:relative}
#edf-art .ft{display:flex;gap:clamp(12px,2vw,28px);overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:26px calc(50% - clamp(200px,21vw,280px)/2) 38px}
#edf-art .ft::-webkit-scrollbar{display:none}
#edf-art .ft .cd{flex:0 0 clamp(200px,21vw,280px);scroll-snap-align:center;transform:scale(.84);opacity:.5;filter:saturate(.6)}
#edf-art .ft .cd.on{transform:scale(1);opacity:1;filter:none;box-shadow:0 26px 54px rgba(27,46,74,.38)}
#edf-art .ft .cd.on:after{content:"ÖNE ÇIKAN";position:absolute;top:14px;right:-36px;transform:rotate(35deg);background:var(--ye);color:var(--nv);font-weight:900;font-size:11px;padding:5px 42px;letter-spacing:.08em;z-index:3}
#edf-art .ar{position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:50px;height:50px;border-radius:50%;border:0;background:var(--nv);color:#fff;font:900 24px/1 'Montserrat',sans-serif;cursor:pointer;display:none;place-items:center;box-shadow:0 6px 18px rgba(0,0,0,.2)}
#edf-art.js .ar{display:grid}
#edf-art .ar:hover{background:var(--rd)}
#edf-art .ar.p{left:20px}#edf-art .ar.n{right:20px}
#edf-art .dots{display:flex;justify-content:center;gap:7px;margin-top:-16px;flex-wrap:wrap}
#edf-art .dots b{width:8px;height:8px;border-radius:8px;background:var(--nv);opacity:.2;transition:all .3s;cursor:pointer}
#edf-art .dots b.on{width:28px;opacity:1;background:var(--rd)}
/* marquee */
#edf-art .mq{overflow:hidden;padding:12px 0;-webkit-mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
#edf-art .mq .rw{display:flex;gap:14px;width:max-content;animation:edfMq 110s linear infinite}
#edf-art .mq.rv .rw{animation-direction:reverse;animation-duration:125s}
#edf-art .mq:hover .rw{animation-play-state:paused}
#edf-art .mq .cd{width:clamp(110px,9vw,145px);flex:0 0 auto}
/* filter + grid */
#edf-art input[type=radio]{position:absolute;opacity:0;pointer-events:none}
#edf-art .fl{display:flex;gap:8px;flex-wrap:wrap;padding-block:14px 0}
#edf-art .fl label{cursor:pointer;border:2px solid var(--nv);border-radius:40px;padding:8px 16px;font-weight:800;font-size:12px;letter-spacing:.04em;background:#fff;transition:background .2s}
#edf-art .fl label small{opacity:.55;margin-left:4px}
#edf-art .fl label:hover{background:var(--ye)}
#edf-art .gr{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:18px;padding-block:22px 10px}
#edf-art .gr .cd{animation:edfPop .45s cubic-bezier(.2,.7,.2,1) both}
@keyframes edfPop{from{opacity:.001;transform:scale(.94) translateY(12px)}}
#edf-art .more{margin-block:26px 48px;padding:26px;border-radius:14px;background:var(--rd);color:#fff;display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:center}
#edf-art .more b{font-weight:900;font-size:clamp(18px,2.4vw,30px);text-transform:uppercase;line-height:1.05}
#edf-art .more a{background:#fff;color:var(--rd);font-weight:900;padding:14px 22px;border-radius:40px;font-size:14px;text-transform:uppercase}
/* story viewer */
#edf-sv{position:fixed;inset:0;z-index:99999;background:rgba(12,20,33,.94);display:none;align-items:center;justify-content:center;font-family:'Montserrat',system-ui,sans-serif;
 padding:max(12px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) max(12px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px))}
#edf-sv.op{display:flex;animation:edfFade .25s both}
@keyframes edfFade{from{opacity:0}}
#edf-sv .box{position:relative;height:min(92vh,100%);aspect-ratio:9/16;max-width:100%;border-radius:14px;overflow:hidden;background:#000;box-shadow:0 30px 80px rgba(0,0,0,.6)}
#edf-sv video{width:100%;height:100%;object-fit:cover;display:block}
#edf-sv .pb{position:absolute;top:10px;left:10px;right:10px;display:flex;gap:3px;z-index:3}
#edf-sv .pb i{flex:1;height:3px;border-radius:3px;background:rgba(255,255,255,.3);overflow:hidden}
#edf-sv .pb i b{display:block;height:100%;width:0;background:#fff}
#edf-sv .pb i.dn b{width:100%}
#edf-sv .tz{position:absolute;top:0;bottom:0;width:35%;z-index:2;cursor:pointer;background:none;border:0}
#edf-sv .tz.l{left:0}#edf-sv .tz.r{right:0}
#edf-sv .x{position:absolute;top:24px;right:12px;z-index:4;width:40px;height:40px;border-radius:50%;border:0;background:rgba(0,0,0,.45);color:#fff;font-size:22px;cursor:pointer}
#edf-sv .nb{position:absolute;top:50%;transform:translateY(-50%);width:52px;height:52px;border-radius:50%;border:0;background:#fff;color:#1B2E4A;font:900 24px/1 'Montserrat',sans-serif;cursor:pointer}
#edf-sv .nb.p{left:max(20px,calc(50% - min(92vh,100vh)*9/32 - 80px))}#edf-sv .nb.n{right:max(20px,calc(50% - min(92vh,100vh)*9/32 - 80px))}
#edf-sv .nb:hover{background:#F0E559}
@media(max-width:700px){#edf-art{border-right-width:8px}#edf-art .hero{padding-block:30px 10px}#edf-art .gr{grid-template-columns:repeat(2,1fr);gap:12px}
 #edf-art .ft{padding-left:calc(50% - 31vw);padding-right:calc(50% - 31vw)}#edf-art .ft .cd{flex-basis:62vw}#edf-art .ar,#edf-sv .nb{display:none!important}#edf-sv .box{height:auto;width:100%;max-height:100%}}
@media (prefers-reduced-motion:reduce){#edf-art *,#edf-sv{animation:none!important;transition:none!important}}
'''
css+='#edf-art #af-all:checked~.fl label[for=af-all]{background:var(--nv);color:#fff}\n'
for b in brs:
    s_=slug(b);css+=f'#edf-art #af-{s_}:checked~.fl label[for=af-{s_}]{{background:var(--nv);color:#fff}}\n#edf-art #af-{s_}:checked~.gr .cd:not(.b-{s_}){{display:none}}\n'
band=' <i>✦</i> '.join(['5 GÜN','10 DANS STİLİ','200+ EĞİTMEN VE DJ','100+ WORKSHOP','5 PARTİ ALANI'])+' <i>✦</i> '
H=[]
if mode=='artifact':
    H.append('<title>EDF 2027 Artistler</title><meta name="claude:viewport-fit-sides" content="cover">')
    H.append('<style>:root{color-scheme:light}body{background:#F6F4EF;overflow-x:hidden}</style>')
H.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap">')
H.append(f'<div id="edf-art"><style>{css}</style>')
H.append(f'<div class="hero pad"><h1 class="up">EDF 2027<span>Artistler</span></h1><p class="up" style="--d:150ms"><b>Tüm artistleri afişe sığdıramadık</b>3–7 Şubat 2027 · Tasigo Hotel, Eskişehir. Şu ana kadar açıklanan {len({a["n"] for a in A})} artist; liste her hafta büyüyor.</p></div>')
H.append(f'<div class="band"><div>{band*4}{band*4}</div></div>')
H.append('<div class="st pad up" style="--d:250ms">Öne çıkanlar</div>')
H.append('<div class="fw"><button class="ar p" type="button" aria-label="Önceki">‹</button><div class="ft">'+''.join(card(a,'on' if i==0 else '',True) for i,a in enumerate(feat))+'</div><button class="ar n" type="button" aria-label="Sonraki">›</button></div>')
H.append('<div class="dots">'+''.join(f'<b{" class=on" if i==0 else ""}></b>' for i in range(len(feat)))+'</div>')
H.append('<div class="st pad">Line-up <small>durdurmak için üstüne gel</small></div>')
half=(len(grid)+1)//2
for k,grp in enumerate([grid[:half],grid[half:]]):
    row=''.join(card(a,'mi') for a in grp)
    H.append(f'<div class="mq{" rv" if k else ""}"><div class="rw">{row}{row.replace("<a ","<a tabindex=\"-1\" aria-hidden=\"true\" ")}</div></div>')
H.append('<div class="pad"><div class="st">Tüm artistler <small>izlemek için afişe dokun</small></div>')
H.append('<input type="radio" name="edfaf" id="af-all" checked>'+''.join(f'<input type="radio" name="edfaf" id="af-{slug(b)}">' for b in brs))
H.append(f'<div class="fl"><label for="af-all">TÜMÜ<small>{len(grid)}</small></label>'+''.join(f'<label for="af-{slug(b)}">{BR[b][0]}<small>{sum(a["b"]==b for a in grid)}</small></label>' for b in brs)+'</div>')
H.append('<div class="gr">'+''.join(card(a,'gi') for a in grid)+'</div>')
H.append('<div class="more"><b>Daha fazla isim<br>çok yakında açıklanacak</b><a href="#">Pass al →</a></div></div></div>')
H.append('<div id="edf-sv" role="dialog" aria-modal="true" aria-label="Artist afişi"><button class="nb p" type="button" aria-label="Önceki">‹</button><div class="box"><div class="pb"></div><video muted playsinline></video><button class="tz l" type="button" aria-label="Önceki"></button><button class="tz r" type="button" aria-label="Sonraki"></button><button class="x" type="button" aria-label="Kapat">✕</button></div><button class="nb n" type="button" aria-label="Sonraki">›</button></div>')
H.append(r'''<script>(function(){var R=document.getElementById('edf-art');if(!R)return;R.classList.add('js');
function load(v){if(!v.src&&v.dataset.src){v.src=v.dataset.src;v.addEventListener('playing',function(){v.classList.add('ok')})}}
function play(v){load(v);var p=v.play();if(p&&p.catch)p.catch(function(){})}
/* featured */
var t=R.querySelector('.ft'),c=[].slice.call(t.querySelectorAll('.cd')),d=[].slice.call(R.querySelectorAll('.dots b')),i=-1,tm;
function mark(){var m=t.scrollLeft+t.clientWidth/2,b=0,bd=1e9;c.forEach(function(e,k){var dd=Math.abs(e.offsetLeft+e.offsetWidth/2-m);if(dd<bd){bd=dd;b=k}});
 if(b===i)return;i=b;c.forEach(function(e,k){e.classList.toggle('on',k==b);var v=e.querySelector('video');if(k==b)play(v);else if(v.src)v.pause()});d.forEach(function(e,k){e.classList.toggle('on',k==b)})}
function go(k){k=(k+c.length)%c.length;var e=c[k];t.scrollTo({left:e.offsetLeft-(t.clientWidth-e.offsetWidth)/2,behavior:'smooth'})}
function auto(){clearInterval(tm);tm=setInterval(function(){if(!sv.classList.contains('op'))go(i+1)},5000)}
t.addEventListener('scroll',function(){requestAnimationFrame(mark)},{passive:true});
R.querySelector('.ar.n').onclick=function(){go(i+1);auto()};R.querySelector('.ar.p').onclick=function(){go(i-1);auto()};
d.forEach(function(e,k){e.onclick=function(){go(k);auto()}});
t.addEventListener('pointerdown',function(){clearInterval(tm)});t.addEventListener('mouseenter',function(){clearInterval(tm)});t.addEventListener('mouseleave',auto);
setTimeout(function(){mark();go(0);auto()},300);
/* grid: play while visible */
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){var a=en.target,v=a.querySelector('video');
 if(en.isIntersecting){if(!v){v=document.createElement('video');v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute('playsinline','');v.preload='none';v.dataset.src=a.getAttribute('href');a.insertBefore(v,a.querySelector('.tg,.pl'))}play(v)}
 else if(v)v.pause()})},{threshold:.6});R.querySelectorAll('.gr .cd').forEach(function(a){io.observe(a)})}
/* story viewer */
var sv=document.getElementById('edf-sv');document.body.appendChild(sv);var vv=sv.querySelector('video'),pb=sv.querySelector('.pb'),L=[],j=0,raf;
var many=false;function bars(){many=L.length>20;pb.innerHTML=many?'<i><b></b></i>':L.map(function(_,k){return '<i class="'+(k<j?'dn':'')+'"><b></b></i>'}).join('')}
function tick(){var b=pb.children[many?0:j]&&pb.children[many?0:j].firstChild;if(b&&vv.duration)b.style.width=(vv.currentTime/vv.duration*100)+'%';raf=requestAnimationFrame(tick)}
function show(k){if(k<0)k=0;if(k>=L.length){close();return}j=k;bars();var a=L[j];vv.poster=a.querySelector('img').src;vv.src=a.getAttribute('href');var p=vv.play();if(p&&p.catch)p.catch(function(){})}
function open(list,a){L=list;sv.classList.add('op');document.documentElement.style.overflow='hidden';show(L.indexOf(a));cancelAnimationFrame(raf);tick();sv.querySelector('.x').focus()}
function close(){sv.classList.remove('op');vv.pause();vv.removeAttribute('src');vv.load();cancelAnimationFrame(raf);document.documentElement.style.overflow=''}
vv.addEventListener('ended',function(){show(j+1)});
sv.querySelector('.tz.l').onclick=sv.querySelector('.nb.p').onclick=function(){show(j-1)};
sv.querySelector('.tz.r').onclick=sv.querySelector('.nb.n').onclick=function(){show(j+1)};
sv.querySelector('.x').onclick=close;sv.addEventListener('click',function(e){if(e.target===sv)close()});
document.addEventListener('keydown',function(e){if(!sv.classList.contains('op'))return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(j+1);if(e.key==='ArrowLeft')show(j-1)});
R.addEventListener('click',function(e){var a=e.target.closest('.cd');if(!a)return;e.preventDefault();
 var list=a.closest('.ft')?c:[].slice.call(R.querySelectorAll('.gr .cd')).filter(function(x){return x.offsetParent!==null});
 if(!a.closest('.ft')&&list.indexOf(a)<0){var g=R.querySelector('.gr .cd[data-id="'+a.dataset.id+'"]');a=g}
 open(list,a)});
})();</script>''')
open(out,'w').write('\n'.join(H))
print(len(A),len(feat),len(grid),brs)
