# Luoghi Google Maps (associazione / centro anziani / comitato di quartiere / centro culturale / parrocchia + toponimo) -> candidati nelle pagine deboli
import json,re,sys,glob,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,f'{S}/popolazione'); sys.path.insert(0,f'{S}/supplementare')
from punto_pagina import pagina
from noti import nota
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
DENY=re.compile(r"(?i)ristorante|\bbar\b|pizzeria|trattoria|hotel|b&b|bed and breakfast|agenzia|negozio|studio (legale|medico|dentistico|di)|avvocat|commerciali|medico|clinica|farmacia|supermercato|palestra|centro fitness|parrucchier|estetist|scuola guida|assicura|immobiliar|banca|ufficio postale|officina|autolavaggio|lavanderia|azienda|fornitore|consulen|società di|caf\b|patronato|partito politico|sindacato|casa di riposo|residenza sanitaria|rsa\b|asilo nido privato|scuola privata|ludoteca|sala (feste|ricevimenti)|catering|noleggio|location|wedding|tabacch|gioielleria|abbigliamento|ottica|veterinari|psicolog|fisioterap|poliambulatorio|laboratorio analisi|onoranze|cimitero|parcheggio|distributore|edicola|libreria|negozi|centro commerciale|pub\b|discoteca|night|sexy")
ALLOW=re.compile(r"(?i)associazion|organizzazione (no profit|di volontariato|non governativa|benefica)|onlus|centro (sociale|per anziani|anziani|culturale|comunitario|civico|giovanile|ricreativo|di quartiere)|circolo|club|chiesa|parrocchia|oratorio|luogo di culto|biblioteca|teatro|scout|comitato|pro loco|polisportiva|società sportiva|associazione sportiva|campo sportivo|centro sportivo|coro|banda|ente|fondazione|casa di quartiere|spazio sociale|comunità|cooperativa sociale")
def tipo(cat,name):
    s=f'{cat} {name}'.lower()
    if re.search(r'parrocchi|chiesa|oratorio|luogo di culto|santuario',s): return 'parrocchia o chiesa cattolica' if not re.search(r'evangel|ortodoss|battist|avventist|pentecost|mormon|testimoni|valdes|moschea|islam|buddh|sikh|induis',s) else 'comunità religiosa'
    if re.search(r'anziani',s): return 'centro anziani'
    if re.search(r'comitato|consulta|social street|retake',s): return 'comitato di quartiere o civico'
    if re.search(r'centro sociale|casa di quartiere|spazio sociale|centro comunitario|centro civico|centro giovanile',s): return 'centro sociale, anziani o di quartiere'
    if re.search(r'teatro|biblioteca|centro culturale|museo|cinema|centro arti',s): return 'luogo culturale (teatro, biblioteca, centro arti)'
    if re.search(r'sportiv|polisportiv|asd\b|ssd\b|calcio|basket|volley|tennis|nuoto|campo',s): return 'sport'
    if re.search(r'scout|agesci|cngei',s): return 'scout'
    return 'associazione'
out={}; st=collections.Counter()
for f in sorted(glob.glob(f'{S}/supplementare/maps*.json')):
    if 'punti' in f: continue
    for p in json.load(open(f)):
        pid=p.get('placeId') or p.get('url')
        if pid in out: st['doppioni']+=1; continue
        loc=p.get('location') or {}; z,m=pagina(loc.get('lat'),loc.get('lng'))
        if z not in T: st['fuori dalle pagine deboli']+=1; continue
        cat=p.get('categoryName') or ''; cats=' '.join(p.get('categories') or []); name=p.get('title') or ''
        if p.get('permanentlyClosed') or p.get('temporarilyClosed'): st['chiusi']+=1; continue
        if DENY.search(cat+' '+cats) and not re.search(r'(?i)associazion|parrocchi|chiesa|circolo',cat): st['commerciali']+=1; continue
        if not (ALLOW.search(cat+' '+cats) or ALLOW.search(name)): st['categoria non pertinente']+=1; continue
        site=p.get('website'); fb=site if site and 'facebook.com' in site else None
        out[pid]={'nome':name,'tipo':tipo(cat+' '+cats,name),'categoria_google':cat,'pagina':z,'municipio':m,'indirizzo':p.get('address'),'sito':None if fb else site,'facebook':fb,'telefono':p.get('phone'),
                  'lat':loc.get('lat'),'lon':loc.get('lng'),'recensioni':p.get('reviewsCount'),'origine':'Google Maps','maps':p.get('url'),'ricerca':p.get('searchString'),'gia_nota':nota(name,None if fb else site,fb,loc.get('lat'),loc.get('lng'))}
json.dump(list(out.values()),open(f'{S}/supplementare/maps_target.json','w'),ensure_ascii=False,indent=0)
print(dict(st)); print(len(out),'nuovi',sum(1 for o in out.values() if not o['gia_nota'])); print(collections.Counter(o['tipo'] for o in out.values()).most_common())
print(collections.Counter(o['categoria_google'] for o in out.values()).most_common(25))
