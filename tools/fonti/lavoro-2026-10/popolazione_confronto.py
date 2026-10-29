# Eventi futuri noti per pagina QN contro abitanti stimati -> eventi_per_abitanti.xlsx
import json,collections,statistics,openpyxl
from openpyxl.styles import Font,PatternFill
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); Z={z['publication_zone_id']:z for z in gz['publication_zones'] if z['is_page']}
POP=json.load(open(f'{S}/popolazione/abitanti_pagina.json'))
D=json.load(open(f'{S}/pagina_eventi/eventi_zu.json')); E=[e for e in D['eventi'] if e['z'] in Z]   # eventi con la stessa geografia degli abitanti
OLD=collections.Counter(e['z'] for e in json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi'])   # geografia della pagina pubblicata
ev=collections.Counter(e['z'] for e in E); loc=collections.Counter(e['z'] for e in E if e['src'] in ('Facebook','Facebook (post)','sito della fonte'))
CENTRO={z for z in Z if Z[z]['primary_municipality']=='I'}|{'parioli-flaminio'}   # centro e grandi istituzioni culturali: fuori dal riferimento
rate={z:10000*ev[z]/POP[z] for z in Z if POP.get(z,0)>=5000 and z not in CENTRO}
REF=statistics.median(rate.values()); ATT=statistics.quantiles(rate.values(),n=4)[2]   # mediana e quartile alto dei quartieri fuori dal centro
FW=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
def utile(f):
    r=f.get('registro') or {}; c=f.get('censimento') or {}
    return (r and r.get('decisione')!='scartare') or str(c.get('verdetto') or '').replace('servizio o impresa sociale: ','').startswith(('rientra','da verificare','locale'))
fonti=collections.Counter(f['zona'] for f in FW if f.get('zona') in Z and utile(f))
rows=[]
for z,p in Z.items():
    a=POP.get(z,0); r=10000*ev[z]/a if a else None
    cl=('centro e grandi istituzioni (fuori dal riferimento)' if z in CENTRO else 'poco abitata (meno di 5.000)' if a<5000 else 'molto sotto (meno di metà della mediana)' if r<REF/2 else 'sotto la mediana' if r<REF else 'fra mediana e quartiere attivo' if r<ATT else 'quartiere attivo')
    rows.append({'pagina':p['name_display'],'id':z,'municipio':p['primary_municipality'],'abitanti_stimati':int(round(a,-2)),'eventi':ev[z],'di_cui_locali':loc[z],'eventi_nella_pagina_pubblicata':OLD[z],'fonti_note':fonti[z],
                 'eventi_per_10000':round(r,1) if r is not None else None,'mancanti_alla_mediana':max(0,round(a*REF/10000-ev[z])),
                 'mancanti_a_quartiere_attivo':max(0,round(a*ATT/10000-ev[z])),'classe':cl})
rows.sort(key=lambda r:(-r['mancanti_a_quartiere_attivo'],-r['abitanti_stimati']))
json.dump({'mediana':REF,'attivo':ATT,'righe':rows},open(f'{S}/popolazione/confronto.json','w'),ensure_ascii=False,indent=1)
wb=openpyxl.Workbook(); w=wb.active; w.title='Pagine'; cols=list(rows[0])
w.append(cols)
for c in w[1]: c.font=Font(bold=True)
fill={'molto sotto (meno di metà della mediana)':'F4CCCC','sotto la mediana':'FCE5CD','fra mediana e quartiere attivo':'FFF2CC','quartiere attivo':'D9EAD3'}
for r in rows:
    w.append([r[c] for c in cols])
    if r['classe'] in fill:
        for c in w[w.max_row]: c.fill=PatternFill('solid',fgColor=fill[r['classe']])
for i,c in enumerate(cols,1): w.column_dimensions[get_column_letter(i)].width=26 if c in ('pagina','classe') else 14
w.column_dimensions['M'].width=46; w.freeze_panes='B2'
z2=wb.create_sheet('Zone urbanistiche'); z2.append(['zona_urbanistica','denominazione','pagina_qn','abitanti_stimati'])
for c in z2[1]: c.font=Font(bold=True)
for zu,n,zona,v in json.load(open(f'{S}/popolazione/zu_pagina.json')): z2.append([zu,n,Z[zona]['name_display'],int(round(v,-1))])
m=wb.create_sheet('Metodo')
for t in ['Abitanti: griglia statistica di Roma Capitale (geoportale, livello DIPAU:griglia_p_statistiche_7792, celle di 1 km, campo «abitanti»; totale 2,82 milioni).',
          'Ogni cella è divisa in 25 punti; ogni punto va nella sua zona urbanistica ufficiale (155) e poi alla pagina QN del toponimo del gazetteer più vicino fra quelli di quella zona urbanistica.',
          'Il totale per zona urbanistica coincide con il dato ufficiale del gazetteer (rapporto mediano 0,96); la divisione di una zona urbanistica fra più pagine è una stima (anche ±30%).',
          'Eventi: tutti gli eventi futuri noti al 25 ottobre 2026 della pagina Eventi dei quartieri (culture.roma.it, eventi Facebook, post Facebook, siti delle fonti, Roma Today), comprese le mostre in corso, esclusi gli 85 fuori Roma trovati in questo controllo.',
          'Gli eventi con coordinate (o con la sede della fonte geolocalizzata) sono riassegnati con la stessa geografia degli abitanti; «eventi_nella_pagina_pubblicata» è il conto con la geografia attuale della pagina (suddivisioni toponomastiche), che accorpa per esempio San Giovanni nel Tuscolano e Centocelle nel Prenestino.',
          '«di_cui_locali»: eventi Facebook, post Facebook e siti delle fonti (esclusi culture.roma.it e Roma Today).',
          '«fonti_note»: fonti della wiki fonti-eventi con sede nella pagina, nel registro (non scartate) o nei censimenti con verdetto «rientra», «da verificare» o «locale».',
          f'Riferimento: le pagine fuori dal centro (escluso il Municipio I e Parioli-Flaminio, che hanno i grandi musei e teatri) con almeno 5.000 abitanti. La pagina mediana fa {REF:.1f} eventi ogni 10.000 abitanti; il quartile alto («quartiere attivo») ne fa {ATT:.1f}.',
          '«mancanti_alla_mediana» e «mancanti_a_quartiere_attivo» = eventi in più che servirebbero per arrivare a quei due livelli con gli abitanti stimati. Conti a grandi numeri, non al singolo evento.']:
    m.append([t])
m.column_dimensions['A'].width=160
wb.save('/mnt/user-data/outputs/eventi_per_abitanti.xlsx')
print('mediana',round(REF,2),'attivo',round(ATT,2),'eventi per 10k; totale citta',round(10000*len(E)/sum(POP.values()),2))
print(collections.Counter(r['classe'] for r in rows))
for r in rows[:30]: print(f"{r['pagina']:24} {r['municipio']:5} ab {r['abitanti_stimati']:>7} ev {r['eventi']:>4} loc {r['di_cui_locali']:>3} fonti {r['fonti_note']:>3} /10k {r['eventi_per_10000']} med {r['mancanti_alla_mediana']} att {r['mancanti_a_quartiere_attivo']} {r['classe'][:12]}")
print('...sopra:'); 
for r in sorted(rows,key=lambda r:-(r['eventi_per_10000'] or 0))[:10]: print(f"   {r['pagina']:24} ab {r['abitanti_stimati']:>7} ev {r['eventi']:>4} /10k {r['eventi_per_10000']}")
