"""EDF artist medyası güncelleyici.
Drive'ı tarar, artistler.json (manifest) ile karşılaştırır; sadece yeni/değişen afişleri indirip
web için küçültür, Drive'dan kalkanları siler, manifest + ARTISTLER.md'yi yazar.
Medya birden fazla repoya bölünür (depolar.json): mevcut artist kendi deposunda kalır, yeni artist "aktif" depoya gider.
Kullanım: python3 tools/guncelle.py DRIVE_KOK_ID REPO_DIZINI ISCI_DIZINI"""
import sys, os, json, re, subprocess, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
from drive_tara import tara, boyut
KOK, REPO, TMP = sys.argv[1], sys.argv[2], sys.argv[3]
MAN = os.path.join(REPO, 'artistler.json')
DEP = json.load(open(os.path.join(REPO, 'depolar.json')))
AKTIF = DEP['aktif']
MEDYA = {int(k): os.path.normpath(os.path.join(REPO, d['yol'], 'media')) for k, d in DEP['depolar'].items()}
for m in MEDYA.values(): os.makedirs(m, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
eski = {a['id']: a for a in json.load(open(MAN))} if os.path.exists(MAN) else {}
files = tara(KOK)
with cf.ThreadPoolExecutor(10) as ex:
    for f, b in zip(files, ex.map(lambda f: boyut(f['id']), files)): f['boyut'] = b
yeni = {}
for f in files:
    ad = re.sub(r'\.mp4$', '', f['dosya'], flags=re.I)
    one = '\u2611' in ad  # ☑️ = sitede öne çıkan (✅ = Instagram'da paylaşıldı, sitede anlamı yok)
    ad = re.sub(r'[\u2611\u2705\ufe0f]', '', ad).strip()
    ad = re.sub(r'\s*-\s*\d+$', '', ad)
    brans = f['klasor'][0] if f['klasor'] else ''
    depo = eski[f['id']].get('depo', 1) if f['id'] in eski else AKTIF
    yeni[f['id']] = dict(id=f['id'], ad=ad, brans=brans, one_cikan=one, boyut=f['boyut'], dosya=f['dosya'], depo=depo)
def M(i): return MEDYA[yeni[i]['depo']]
def kucuk(i):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{M(i)}/{i}.jpg', '-vf', 'scale=270:480:flags=lanczos', '-q:v', '5', f'{M(i)}/{i}_k.jpg'], check=True)
def islem(a):
    i = a['id']; mp4 = f'{M(i)}/{i}.mp4'; jpg = f'{M(i)}/{i}.jpg'; raw = f'{TMP}/{i}.mp4'
    subprocess.run(['curl', '-sS', '-L', '--max-time', '300', '-o', raw,
                    f'https://drive.usercontent.google.com/download?id={i}&export=download&confirm=t'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-vf', 'scale=540:960:flags=lanczos,fps=30', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '30', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', mp4], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '3', '-i', raw, '-frames:v', '1', '-vf', 'scale=540:960', '-q:v', '4', jpg], check=True)
    os.remove(raw); kucuk(i); return a['ad']
lazim = [a for i, a in yeni.items() if i not in eski and not (os.path.exists(f'{M(i)}/{i}.mp4') and os.path.exists(f'{M(i)}/{i}.jpg'))
         or (i in eski and eski[i].get('boyut') != a['boyut'])]
with cf.ThreadPoolExecutor(4) as ex: islenen = list(ex.map(islem, lazim))
for i in yeni:
    if os.path.exists(f'{M(i)}/{i}.jpg') and not os.path.exists(f'{M(i)}/{i}_k.jpg'): kucuk(i)
silinen = []
for d, md in MEDYA.items():
    for fn in os.listdir(md):
        if fn.startswith('.'): continue
        i = fn.rsplit('.', 1)[0].removesuffix('_k')
        if i not in yeni or yeni[i]['depo'] != d: os.remove(os.path.join(md, fn)); silinen.append(i)
silinen_ad = sorted({eski[i]['ad'] if i in eski else i for i in silinen if i not in yeni})
degisen = [(eski[i]['ad'], k, eski[i].get(k), a[k]) for i, a in yeni.items() if i in eski for k in ('ad', 'brans', 'one_cikan') if eski[i].get(k) != a[k]]
TR = str.maketrans('ÇĞİIÖŞÜçğıiöşü', 'CGIIOSUcgiiosu')
liste = sorted(yeni.values(), key=lambda a: (a['brans'].translate(TR), a['ad'].translate(TR)))
json.dump(liste, open(MAN, 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(REPO, 'ARTISTLER.md'), 'w') as md:
    md.write(f'# EDF 2027 Artist Listesi\n\nDrive kaynağından otomatik üretilir, elle düzenleme. Toplam **{len(liste)}** afiş, **{sum(a["one_cikan"] for a in liste)}** öne çıkan.\n\n| Branş | Artist | Öne çıkan | Drive ID |\n|---|---|---|---|\n')
    for a in liste: md.write(f'| {a["brans"] or "—"} | {a["ad"]} | {"☑️" if a["one_cikan"] else ""} | `{a["id"]}` |\n')
def boy(d): return round(sum(os.path.getsize(os.path.join(MEDYA[d], f)) for f in os.listdir(MEDYA[d])) / 1e6, 1)
print(json.dumps(dict(toplam=len(liste), indirilen=islenen, silinen=silinen_ad, degisen=degisen,
                      depolar={DEP['depolar'][str(d)]['ad']: f'{boy(d)} MB' for d in MEDYA}), ensure_ascii=False, indent=1))
