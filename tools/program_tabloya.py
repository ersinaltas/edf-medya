"""Eski ızgara program verisini (program_veri.json) satır tabloya (CSV) çevirir. Bir kerelik geçiş betiği."""
import json, csv, sys
d = json.load(open('program_veri.json'))
KAT = {'beg':'Beginner','int':'Intermediate','all':'All Level','adv':'Advanced','hh':'Hip Hop & Free Style','lindy':'Lindy Hop / Jazz','zumba':'Zumba','kpop':'K-Pop','kids':'Kids','comp':'Competition','party':'Party','sunset':'Sunset Party','redbull':'Red Bull','free':'Free Time','rehearsal':'Show / Rehearsal'}
SALON = ['SALON 1','SALON 2','SALON 3','SALON 4','SALON 5','SALON 6','SALON 7','DIŞ ALAN']
def tkey(t): h, m = map(int, t.split(':')); return (h + 24 if h < 6 else h) * 60 + m
rows = []
for g in d:
    col = {}
    for c in g['cols']:
        for k in range(c['span']): col[c['c0'] - 2 + k] = c['name']
    T = g['times']
    def satir(r):
        while not T[r]: r -= 1
        return r
    for c in g['cells']:
        r0 = satir(c['r']); rl = c['r'] + c['rs'] - 1
        bas = T[r0].split(' – ')[0]; bit = T[satir(rl)].split(' – ')[1]
        if bit == '…':
            # aynı sütunlarda sonra başlayan hücre varsa açık uçlu değil, onun başında biter
            sonra = [x for x in g['cells'] if x['r'] > rl and not (x['c'] + x['cs'] - 1 < c['c'] or x['c'] > c['c'] + c['cs'] - 1)]
            bit = '00:00' if sonra else ''
        t = c['title'].replace('i̇', 'i')
        if c['cat'] == 'redbull' and t.upper() == 'COAT PARTY': t = 'Red Bull Coat Party'
        s1 = col[c['c']]; s2 = col[c['c'] + c['cs'] - 1]
        rows.append([f"{g['gun']} {g['tarih']}", bas, bit, s1, s2 if s2 != s1 else '', t, '', KAT[c['cat']], ' · '.join(c.get('sub', []))])
# Gece yarısı bölgeleri: "Bachata/Salsa/Kizomba" satırlarına gecenin parti adını ekle, sıfır süreli başlık satırlarını çıkar
ZON = {'Bachata', 'Salsa', 'Kizomba'}
for r in rows:
    if r[5] in ZON and r[1] == '00:00':
        ana = [x for x in rows if x[0] == r[0] and x[4] and x[7] == 'Party' and x[3] == 'SALON 1' and tkey(x[1]) <= tkey('00:00')]
        if ana:
            ana.sort(key=lambda x: tkey(x[1])); r[5] = ana[-1][5] + ' · ' + r[5]; r[8] = r[8] or ana[-1][8]
rows = [r for r in rows if not (r[1] == '00:00' and r[2] == '00:00')]
gs = [f"{g['gun']} {g['tarih']}" for g in d]
rows.sort(key=lambda r: (gs.index(r[0]), tkey(r[1]), SALON.index(r[3])))
w = csv.writer(open(sys.argv[1], 'w', newline=''))
w.writerow(['Gün','Başlangıç','Bitiş','Salon','Bitiş Salonu','Başlık','Eğitmen','Kategori','Not']); w.writerows(rows)
print(len(rows), 'satır')
