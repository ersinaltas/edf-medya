"""Drive 'EDF 2027 Afişler' klasörünü tarar, her afiş için id/ad/branş/boyut çıkarır.
Kullanım: python3 drive_tara.py ROOT_FOLDER_ID > drive_simdi.json"""
import sys, re, json, subprocess, html, concurrent.futures as cf
def get(url):
    return subprocess.run(['curl','-sS','-L','--max-time','60',url],capture_output=True,text=True).stdout
def ls(fid):
    s=get(f'https://drive.google.com/embeddedfolderview?id={fid}')
    out=[]
    for m in re.finditer(r'id="entry-([\w-]+)".*?href="([^"]+)".*?flip-entry-title">([^<]*)<',s,re.S):
        eid,href,title=m.groups()
        out.append(dict(id=eid,ad=html.unescape(title).strip(),klasor='/folders/' in href))
    return out
def boyut(fid):
    h=subprocess.run(['curl','-sS','-L','-r','0-0','-D','-','-o','/dev/null','--max-time','60',
        f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'],capture_output=True,text=True).stdout
    m=re.findall(r'(?i)content-range: bytes 0-0/(\d+)',h)
    return int(m[-1]) if m else None
def tara(fid,yol=()):
    res=[]
    for e in ls(fid):
        if e['klasor']: res+=tara(e['id'],yol+(e['ad'],))
        else: res.append(dict(id=e['id'],dosya=e['ad'],klasor=list(yol)))
    return res
if __name__=='__main__':
  files=tara(sys.argv[1])
  with cf.ThreadPoolExecutor(10) as ex:
    for f,b in zip(files,ex.map(lambda f:boyut(f['id']),files)): f['boyut']=b
  json.dump(files,sys.stdout,ensure_ascii=False,indent=1)
