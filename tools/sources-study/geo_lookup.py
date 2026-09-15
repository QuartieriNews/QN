"""Deterministic localisation for the sources study (method §3.3): same key space and
normalisation as tests/zone_distribution.py (text_contains tier), plus a Municipio mention
regex. Returns per text: toponym flag, municipio (roman), zone id, tier."""
import json,re,unicodedata,sys
G=json.load(open('/home/user/QN/gazetteer/gazetteer.json'))
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def norm(s):
    if not s: return ""
    s=unicodedata.normalize("NFKD",str(s)); s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^a-z0-9 ]+"," ",s.casefold()); return re.sub(r"\s+"," ",s).strip()
INDEX={}
ZMUN={z['publication_zone_id']:z.get('primary_municipality') for z in G['publication_zones']}
for n in G['neighbourhoods']:
    for k in [n['name_display']]+[a.strip() for a in n['aliases'].split('|') if a.strip()]:
        INDEX.setdefault(norm(k),set()).add(n['publication_zone_id'])
for z in G['publication_zones']: INDEX.setdefault(norm(z['name_display']),set()).add(z['publication_zone_id'])
STOP={norm(s) for s in G['free_text_stoplist']}; NEVER={norm(s) for s in G['never_substring']}
KEYS=[k for k in INDEX if k not in NEVER and k not in STOP]
TOPO=re.compile(r"\b(via|viale|piazza|piazzale|largo|corso|lungotevere|vicolo|circonvallazione|quartiere|zona|borgata|litorale|parco|villa)\s+(?:de[lgi]{0,3}\s+|d[ae]l?l[aeo']\s*)?[A-ZÀ-Ú][\w'’.-]+",re.U)
MUNRE=re.compile(r"\b(?:Municipio|Municipi|MUNICIPIO)\s+(?:Roma\s+)?([IVX]{1,4}|\d{1,2})\b|\b([IVX]{1,4})\s+Municipio\b|\bMunicipio\s+Roma\s+([IVX]{1,4})\b")
def municipi(text):
    out=set()
    for m in MUNRE.finditer(text or ''):
        v=next((g for g in m.groups() if g),None)
        if v and v.isdigit() and 1<=int(v)<=15: v=ROM[int(v)-1]
        if v in ROM: out.add(v)
    return out
def zones(text):
    t=f" {norm(text)} "; hits={}
    for k in KEYS:
        if f" {k} " in t:
            for z in INDEX[k]: hits.setdefault(z,set()).add(k)
    return hits
def localise(text):
    text=text or ''
    mun=municipi(text); zh=zones(text); topo=bool(TOPO.search(text)) or bool(zh)
    zone=None; tier=''
    if len(zh)==1: zone=next(iter(zh)); tier='text_contains'
    elif len(zh)>1: tier='ambiguous'
    mun_det=''
    if len(mun)==1: mun_det=next(iter(mun))
    elif zone: mun_det=ZMUN.get(zone) or ''
    elif len(mun)>1: mun_det='multi:'+'/'.join(sorted(mun,key=ROM.index))
    return {'toponimo':topo,'municipio':mun_det,'zona':zone or '','zone_hits':';'.join(sorted(zh)),'tier':tier,'mun_mentions':'/'.join(sorted(mun,key=ROM.index))}
if __name__=='__main__':
    import csv
    src,textcols,out=sys.argv[1],sys.argv[2].split(','),sys.argv[3]
    rows=list(csv.DictReader(open(src),delimiter='\t'))
    for r in rows:
        r.update(localise(' '.join(r.get(c,'') for c in textcols)))
    with open(out,'w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()),delimiter='\t'); w.writeheader(); w.writerows(rows)
    n=len(rows); print(src,n,"| toponimo:",sum(1 for r in rows if r['toponimo']),"| municipio det:",sum(1 for r in rows if r['municipio'] and not r['municipio'].startswith('multi')),"| zona det:",sum(1 for r in rows if r['zona']),"| ambiguous:",sum(1 for r in rows if r['tier']=='ambiguous'))
