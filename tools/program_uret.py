import json, sys, html
days=json.load(open(sys.argv[1]))
LEG=[('beg','Beginner'),('int','Intermediate'),('all','All Level'),('adv','Advanced'),('hh','Hip Hop & Free Style'),
     ('lindy','Lindy Hop / Jazz'),('zumba','Zumba'),('kpop','K-Pop'),('kids','Kids'),('comp','Competition')]
LAB=dict(LEG)
def fix(t):
    return t.replace('Ki̇zomba','Kizomba').replace('Coat Party','Coat Party')
def esc(s): return html.escape(s)
out=[]
for d in days:
    for c in d['cells']:
        if c['type']=='ws' and c['_eski']=='RED BULL':
            c.update(type='event',cat='redbull',title='Red Bull Coat Party',sub=[])
        c['title']=fix(c['title'])
        c.pop('_eski',None)
json.dump(days,open(sys.argv[1].replace('.json','_isimsiz.json'),'w'),ensure_ascii=False,indent=1)

css=r'''
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap');
#edf-prog{--nv:#1B2E4A;--rd:#E44351;--bl:#29649D;--ye:#F0E559;--sa:#EF6A64;--bg:#F6F4EF;--ln:#E3DED4;
 font-family:'Montserrat',sans-serif;color:var(--nv);background:var(--bg);padding:28px 24px 32px;box-sizing:border-box;border-right:14px solid var(--rd)}
#edf-prog *{box-sizing:border-box}
#edf-prog .hd{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px;margin-bottom:18px}
#edf-prog h2{font-size:clamp(26px,4vw,44px);font-weight:900;line-height:1;margin:0;letter-spacing:-.5px;text-transform:uppercase}
#edf-prog h2 span{color:var(--rd)}
#edf-prog .meta{font-weight:700;font-size:14px;margin-top:8px;opacity:.8}
#edf-prog .draft{background:var(--ye);font-weight:800;font-size:12px;padding:6px 10px;border-radius:4px;letter-spacing:.5px}
#edf-prog input[type=radio]{position:absolute;opacity:0;pointer-events:none}
#edf-prog .tabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;margin-bottom:14px}
#edf-prog .tabs label{flex:0 0 auto;cursor:pointer;border:2px solid var(--nv);border-radius:6px;padding:8px 14px;font-weight:800;font-size:13px;text-transform:uppercase;line-height:1.15;text-align:center;background:#fff}
#edf-prog .tabs label small{display:block;font-weight:600;font-size:11px;opacity:.7}
#edf-prog .pn{display:none}
'''
for i,d in enumerate(days):
    css+=f"#edf-prog #edfd{i}:checked~.tabs label[for=edfd{i}]{{background:var(--nv);color:#fff}}\n#edf-prog #edfd{i}:checked~.pns .pn{i}{{display:block}}\n"
css+=r'''
#edf-prog .leg{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:11px;font-weight:700;margin:0 0 14px}
#edf-prog .leg i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
#edf-prog .sc{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--ln);border-radius:8px;background:#fff}
#edf-prog .g{display:grid;gap:4px;padding:4px;width:100%}
#edf-prog .th{background:var(--nv);color:#fff;font-weight:800;font-size:12px;letter-spacing:.5px;padding:10px 8px;text-align:center;border-radius:4px}
#edf-prog .tm{position:sticky;left:0;z-index:2;background:#fff;font-weight:800;font-size:12px;padding:8px 6px;display:flex;align-items:center;justify-content:center;text-align:center;border-right:2px solid var(--rd)}
#edf-prog .th.c0{position:sticky;left:0;z-index:3}
#edf-prog .w{background:#fff;border:1px solid var(--ln);border-left:5px solid var(--k);border-radius:4px;padding:7px 8px;min-height:62px;display:flex;flex-direction:column;gap:4px}
#edf-prog .w b{font-size:13px;font-weight:800;line-height:1.2}
#edf-prog .w em{font-style:normal;font-size:11px;font-weight:600;opacity:.45}
#edf-prog .w s{text-decoration:none;align-self:flex-start;font-size:9.5px;font-weight:800;text-transform:uppercase;letter-spacing:.4px;padding:2px 6px;border-radius:3px;background:var(--k);color:var(--kt,#fff)}
#edf-prog .e{border-radius:4px;padding:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:13px;line-height:1.25}
#edf-prog .e small{display:block;font-weight:600;font-size:11px;margin-top:3px;opacity:.85}
#edf-prog .e.arena{align-items:flex-start;text-align:left;justify-content:flex-start}
#edf-prog .e.party{background:var(--nv);color:#fff}
#edf-prog .e.redbull{background:#B3123A;color:#fff}
#edf-prog .e.sunset{background:linear-gradient(160deg,var(--sa),var(--ye));color:var(--nv)}
#edf-prog .e.free{background:repeating-linear-gradient(135deg,#F4F1EA 0 8px,#EEEAE1 8px 16px);color:#9A9386;font-weight:600;font-size:12px}
#edf-prog .e.rehearsal{background:#DDE3EA;color:var(--nv)}
#edf-prog .e.kids{background:#FF5994;color:#fff}
#edf-prog .e.comp{background:#EDE3FA;color:var(--nv);border:2px solid #9B7BD4}
#edf-prog .e.hh{background:#41B8A6;color:#fff}
#edf-prog .e.kpop{background:#B04FD9;color:#fff}
#edf-prog .k-beg{--k:#F0E559;--kt:#1B2E4A}#edf-prog .k-int{--k:#29649D}#edf-prog .k-all{--k:#EF6A64}#edf-prog .k-adv{--k:#E44351}
#edf-prog .k-hh{--k:#41B8A6}#edf-prog .k-lindy{--k:#E9A97E}#edf-prog .k-zumba{--k:#3CB44B}#edf-prog .k-kpop{--k:#B04FD9}
#edf-prog .k-kids{--k:#FF5994}#edf-prog .k-comp{--k:#9B7BD4}
#edf-prog .ft{font-size:11px;font-weight:600;opacity:.7;margin-top:12px}
@media(max-width:700px){#edf-prog{padding:20px 10px;border-right-width:8px}#edf-prog .w b{font-size:12px}}
'''
h=[f'<div id="edf-prog"><style>{css}</style>']
h.append('<div class="hd"><div><h2>EDF 2027 <span>Workshop</span> Programı</h2><div class="meta">3–7 Şubat 2027 · Tasigo Hotel, Eskişehir</div></div><div class="draft">TASLAK · EĞİTMENLER AÇIKLANACAK</div></div>')
for i,_ in enumerate(days):
    h.append(f'<input type="radio" name="edfday" id="edfd{i}"{" checked" if i==1 else ""}>')
h.append('<div class="tabs">'+''.join(f'<label for="edfd{i}">{d["gun"]}<small>{d["tarih"]}</small></label>' for i,d in enumerate(days))+'</div>')
h.append('<div class="leg">'+''.join(f'<span lang="en"><i style="background:var(--k)" class="k-{k}"></i>{v}</span>' for k,v in LEG)+'</div>')
h.append('<div class="pns">')
for i,d in enumerate(days):
    n=d['ncols']
    h.append(f'<div class="pn pn{i}"><div class="sc"><div class="g" style="grid-template-columns:86px repeat({n},minmax(140px,1fr));min-width:{86+n*144}px">')
    h.append('<div class="th c0" style="grid-row:1;grid-column:1">SAAT</div>')
    for c in d['cols']:
        h.append(f'<div class="th" style="grid-row:1;grid-column:{c["c0"]} / span {c["span"]}">{esc(c["name"])}</div>')
    for r,t in enumerate(d['times']):
        if t:
            sp=1
            while r+sp<len(d['times']) and not d['times'][r+sp]: sp+=1
            h.append(f'<div class="tm" style="grid-row:{r+2} / span {sp}">{esc(t).replace(" – ","<br>")}</div>')
    for c in d['cells']:
        pos=f'grid-row:{c["r"]+2} / span {c["rs"]};grid-column:{c["c"]+2} / span {c["cs"]}'
        if c['type']=='ws':
            tag=LAB.get(c['cat'],'')
            h.append(f'<div class="w k-{c["cat"]}" style="{pos}"><s lang="en">{tag}</s><b>{esc(c["title"])}</b><em>{esc(c["egitmen"]) or "Eğitmen TBA"}</em></div>')
        else:
            cls=c['cat'] if c['cat'] in('party','redbull','sunset','free','rehearsal','kids','comp','hh','kpop') else 'party'
            if 'Arena' in c['title']: cls+=' arena'
            sub=''.join(f'<small>{esc(s)}</small>' for s in c['sub'])
            h.append(f'<div class="e {cls}" style="{pos}">{esc(c["title"])}{sub}</div>')
    h.append('</div></div></div>')
h.append('</div><div class="ft">* Program taslaktır; salon, saat ve eğitmen bilgileri değişebilir. Yarışma kategorileri belirtilen saatten erken başlayabilir.</div></div>')
body='\n'.join(h)
open(sys.argv[2],'w').write(body)
open(sys.argv[3],'w').write('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EDF 2027 Program Taslak</title><style>body{margin:0;background:#fff}</style></head><body>'+body+'</body></html>')
