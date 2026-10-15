"""Deterministic localisation for the sources study (method §3.3): same key space and
normalisation as tests/zone_distribution.py (text_contains tier), plus a Municipio mention
regex. Returns per text: toponym flag, municipio (roman), zone id, tier."""
import json,re,unicodedata,sys,os
# il gazetteer e' nel repository: QN_REPO_ROOT se impostato, altrimenti due cartelle sopra questo file
_ROOT=os.environ.get('QN_REPO_ROOT') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
_QUI=os.path.dirname(os.path.abspath(__file__))
_GAZ=next((p for p in (os.path.join(_ROOT,'gazetteer','gazetteer.json'), os.path.join(_QUI,'gazetteer.json')) if os.path.exists(p)), None)
if not _GAZ: sys.exit('geo_lookup: gazetteer non trovato: imposta QN_REPO_ROOT o copia gazetteer/gazetteer.json accanto a questo file (HANDOFF §4, passo 0)')
G=json.load(open(_GAZ,encoding='utf-8'))
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def norm(s):
    if not s: return ""
    s=unicodedata.normalize("NFKD",str(s)); s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^a-z0-9 ]+"," ",s.casefold()); return re.sub(r"\s+"," ",s).strip()
INDEX={}
# DEC-105: il quartiere d'uso comune e' un'attribuzione a se', non la zona editoriale che lo
# contiene. QUART tiene il quartiere; INDEX resta la zona, che serve alla pubblicazione.
QUART={}
QINFO={n['neighbourhood_id']:n for n in G['neighbourhoods']}
ZMUN={z['publication_zone_id']:z.get('primary_municipality') for z in G['publication_zones']}
for n in G['neighbourhoods']:
    for k in [n['name_display']]+[a.strip() for a in n['aliases'].split('|') if a.strip()]:
        INDEX.setdefault(norm(k),set()).add(n['publication_zone_id'])
        QUART.setdefault(norm(k),set()).add(n['neighbourhood_id'])
for z in G['publication_zones']: INDEX.setdefault(norm(z['name_display']),set()).add(z['publication_zone_id'])
STOP={norm(s) for s in G['free_text_stoplist']}; NEVER={norm(s) for s in G['never_substring']}
KEYS=[k for k in INDEX if k not in NEVER and k not in STOP]
QKEYS=[k for k in QUART if k not in NEVER and k not in STOP]
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
# Un nome di quartiere puo' comparire dentro il nome di una strada. Due casi diversi: "via dei
# Monti Tiburtini" contiene "Monti", che li' non e' il rione (match piu' lungo vince); "parco della
# Caffarella" invece il quartiere lo indica davvero. Il primo si toglie, il secondo si tiene e si
# segnala, perche' decidere da soli quale odonimo "vale" sarebbe una scelta editoriale.
ODONIMO=re.compile(r"(?:^| )(?:via|viale|via di|piazza|piazzale|largo|vicolo|lungotevere|corso|"
                   r"ponte|circonvallazione|stazione|galleria|salita|clivo|borgo|passeggiata)"
                   r"(?: di| del| della| dello| dei| delle| degli| dell| d| a| al| alla)*\s+$")
def quartieri(text, dettaglio=False):
    t=f" {norm(text)} "
    trovati={}
    for k in QKEYS:
        # str.find invece di una regex per chiave: sono 440 chiavi per ogni testo, e il conto si
        # fa su tutto il corpus. La semantica e' la stessa del vecchio `f" {k} " in t`.
        sp=[]; i=t.find(' '+k+' ')
        while i!=-1:
            sp.append((i+1,i+1+len(k))); i=t.find(' '+k+' ',i+1)
        if sp: trovati[k]=sp
    out=set(); odonimo=set()
    for k,sp in trovati.items():
        # occorrenze non contenute dentro il match di un nome piu' lungo
        libere=[s for s in sp if not any(k2!=k and any(a<=s[0] and s[1]<=b for a,b in sp2)
                                         for k2,sp2 in trovati.items())]
        if not libere: continue
        out|=QUART[k]
        if all(ODONIMO.search(t[:s[0]]) for s in libere): odonimo|=QUART[k]
    return (out,odonimo) if dettaglio else out
def municipi_di(qid):
    """I Municipi di un quartiere: quello principale piu' quelli che attraversa."""
    n=QINFO[qid]; out={n['municipality_code']} if n.get('municipality_code') else set()
    out|={x.strip() for x in (n.get('spans_municipalities') or '').replace('/',',').split(',') if x.strip()}
    return {m for m in out if m in ROM}
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
    qh,q_odo=quartieri(text,dettaglio=True)
    # Il quartiere non si sceglie: se il testo ne nomina piu' d'uno restano tutti (DEC-105 §3).
    quart=';'.join(QINFO[q]['name_display'] for q in sorted(qh))
    # Posizionale: la zona urbanistica sta nella stessa posizione del suo quartiere. Togliere i
    # vuoti (uno .strip(';') di troppo) faceva scivolare i codici su un quartiere diverso, cioe'
    # attribuiva a Ponte la zona di Salario senza che niente lo dicesse.
    quart_zu=';'.join((QINFO[q].get('zu_code') or '') for q in sorted(qh))
    mun_gaz=set()
    for q in qh: mun_gaz|=municipi_di(q)
    # Corrispondenza fra quello che il testo dichiara e quello che il gazetteer deduce.
    if mun and mun_gaz and not (mun & mun_gaz):
        dedotto='misto'; mun_det=';'.join(sorted(mun|mun_gaz,key=ROM.index))
    elif mun:
        dedotto='no'
    elif mun_gaz:
        dedotto='si'
        if not mun_det: mun_det=';'.join(sorted(mun_gaz,key=ROM.index))
    else:
        dedotto=''
    return {'toponimo':topo,'municipio':mun_det,'zona':zone or '','zone_hits':';'.join(sorted(zh)),
            'tier':tier,'mun_mentions':'/'.join(sorted(mun,key=ROM.index)),
            'quartiere':quart,'quartiere_zu':quart_zu if quart_zu.strip(';') else '',
            # I Municipi che il gazetteer assegna ai quartieri trovati: servono a chi scrive il
            # database per verificare la corrispondenza geografica (DEC-105 §3), non si pubblicano.
            'quartiere_mun':';'.join(sorted(mun_gaz,key=ROM.index)),
            'quartiere_odonimo':';'.join(QINFO[q]['name_display'] for q in sorted(q_odo)),
            'territorio_dedotto':dedotto}
if __name__=='__main__':
    import csv
    src,textcols,out=sys.argv[1],sys.argv[2].split(','),sys.argv[3]
    rows=list(csv.DictReader(open(src),delimiter='\t'))
    for r in rows:
        r.update(localise(' '.join(r.get(c,'') for c in textcols)))
    with open(out,'w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()),delimiter='\t'); w.writeheader(); w.writerows(rows)
    n=len(rows); print(src,n,"| toponimo:",sum(1 for r in rows if r['toponimo']),"| municipio det:",sum(1 for r in rows if r['municipio'] and not r['municipio'].startswith('multi')),"| zona det:",sum(1 for r in rows if r['zona']),"| ambiguous:",sum(1 for r in rows if r['tier']=='ambiguous'))
