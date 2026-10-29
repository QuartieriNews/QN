# Ricerche integrative nate dall'analisi per categoria: perché, costo, esito (numeri calcolati dai file)
import json,os,collections,glob
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
bib=[e for e in E if e['o'].startswith('Biblioteche di Roma')]
fbn=[e for e in E if e['o'].startswith('Facebook: pagine mai lette')]
fbr=[x for f in sorted(glob.glob(f'{P}/fbevents_ev_*.json')) for x in json.load(open(f)) if isinstance(x,dict) and not x.get('error') and (x.get('id') or x.get('url'))]
CG=json.load(open(f'{P}/canali_google.json'))
import re
_k=lambda u: re.sub(r'^https?://(www\.|m\.)?facebook\.com/','',str(u)).strip('/').lower()
_grp={_k(v[2]):v[0] for v in json.load(open(f'{P}/fbevents_cand.json')).values()}
fbg=collections.Counter(_grp.get(_k((x.get('_metadata') or {}).get('query')),'?') for x in fbr
                        if str(x.get('is_past'))!='True' and ('Rome' in str(x.get('city')) or 'Roma' in str(x.get('address'))))

cost=json.load(open(f'{P}/costi.json')) if os.path.exists(f'{P}/costi.json') else {}
I=[
 {'idea':'Agenda delle Biblioteche di Roma (news dell\'OPAC, eventi schema.org per sede)','stato':'eseguita',
  'perché':'Le biblioteche sono la categoria pubblica più presente nelle periferie e quella che attiva più eventi per soggetto, ma nel calendario c\'erano 47 eventi da una decina di sedi.',
  'costo':'0 $ (lettura del sito, una richiesta al secondo; il sito non ha robots.txt)',
  'esito':f"{len(bib)} eventi futuri nella pagina, {sum(1 for e in bib if e['z'] in T)} nelle 41 pagine deboli, da {len({e['org'] for e in bib})} sedi"},
 {'idea':'Eventi futuri delle pagine Facebook mai lette (lista supplementare e promotori)','stato':'eseguita',
  'perché':'Di 226 pagine della lista supplementare (comitati, parrocchie, associazioni delle pagine deboli) e di 384 pagine di promotori avevamo letto al più i post, mai gli eventi.',
  'costo':f"{cost.get('fbevents','0,14')} $",
  'esito':f"lette tutte le 226 pagine della lista supplementare e 13 delle 384 dei promotori (lettura interrotta: circa 5 pagine al minuto, e i promotori sono già nel calendario); {len(fbr)} eventi letti, {fbg['lista supplementare']+fbg['promotore']} futuri a Roma: {fbg['lista supplementare']} dalle 226 pagine dei quartieri deboli, {fbg['promotore']} dalle 13 dei promotori; {len(fbn)} entrati nella pagina dopo filtri e doppioni. Conferma che i piccoli soggetti annunciano nei post, non negli eventi Facebook"},
 {'idea':'Profili Facebook dei promotori senza dati (descrizione, email, sito, Instagram)','stato':'eseguita','perché':'Per 428 promotori con pagina Facebook non avevamo il profilo.',
  'costo':f"{cost.get('fbpages','3,51')} $",'esito':'425 profili letti: 367 con email, 403 con descrizione'},
 {'idea':'Ricerca Google dei canali per i promotori senza sito né Facebook','stato':'eseguita','perché':'154 promotori (soprattutto «a cura di» di culture.roma.it) non avevano un canale da leggere.',
  'costo':f"{cost.get('google','0,39')} $",'esito':f"canali trovati per {len(CG)} promotori: {sum(1 for v in CG.values() if v.get('sito'))} siti, {sum(1 for v in CG.values() if v.get('facebook'))} pagine Facebook, {sum(1 for v in CG.values() if v.get('instagram'))} Instagram"},
 {'idea':'Eventi dei Municipi su comune.roma.it','stato':'provata e scartata','perché':'Gli eventi municipali sono quelli dei quartieri per definizione.',
  'costo':'0 $','esito':'Municipi VI e VII: 11 eventi in elenco, quasi tutti dell\'estate e in parte già noti; l\'elenco non è un calendario aggiornato'},
 {'idea':'Calendario delle gare podistiche (calendariopodismo.it, pagina Lazio)','stato':'provata e scartata','perché':'Le corse su strada e nei parchi sono eventi sportivi di quartiere, spesso in periferia.',
  'costo':'0 $ (4 pagine dell\'elenco; robots.txt aperto)','esito':'98 gare nel Lazio fino a dicembre, 7 a Roma e quasi tutte grandi corse del centro già note; per le periferie meglio i calendari delle società e dei comitati (UISP, CSI)'},
 {'idea':'Bollettini e avvisi parrocchiali (pagine avvisi dei siti, foglio domenicale in PDF)','stato':'proposta',
  'perché':'283 parrocchie e realtà religiose nelle pagine deboli, solo il 8% produce eventi nel calendario; il 46% degli eventi religiosi cade nelle pagine deboli: è la categoria più legata alle periferie.',
  'costo':'0 $ (lettura dei siti e dei PDF; da scrivere un lettore di PDF)','esito':'—'},
 {'idea':'Calendario della Diocesi di Roma (sito con calendario eventi)','stato':'proposta','perché':'Feste patronali, concerti e iniziative delle parrocchie in un unico calendario.',
  'costo':'0 $','esito':'il sito chiede un captcha dopo poche richieste: va chiesto alla Diocesi un feed o un permesso di lettura'},
 {'idea':'Calendari dei tornei e delle gare delle società (UISP Roma, CSI Roma)','stato':'proposta','perché':'196 realtà sportive nelle pagine deboli, l\'11% attive; le gare podistiche e i tornei si svolgono soprattutto in periferia.',
  'costo':'0-1 $','esito':'—'},
 {'idea':'Centri anziani e centri sociali','stato':'proposta (contatto, non ricerca)','perché':'73 nelle pagine deboli, il 3% visibile online: feste e gite non arrivano su web né social.',
  'costo':'0 $','esito':'contatto diretto con i telefoni della lista supplementare o con l\'ufficio centri anziani di ogni Municipio'},
 {'idea':'Gruppi Facebook di quartiere («Sei di … se»)','stato':'proposta (manuale)','perché':'Molti comitati comunicano solo nei gruppi; 23 gruppi già nella lista supplementare.',
  'costo':'0 $','esito':'non leggibili in automatico (gruppi chiusi): iscrizione della redazione e lettura settimanale'},
 {'idea':'Instagram dei promotori senza eventi su Facebook','stato':'proposta','perché':'Persone, associazioni culturali e locali pubblicano soprattutto su Instagram.',
  'costo':'2-5 $ per un giro','esito':'resa attesa bassa nelle pagine deboli: da fare dopo i bollettini parrocchiali'},
]
json.dump(I,open(f'{P}/idee.json','w'),ensure_ascii=False,indent=1)
for i in I: print('-',i['stato'],'|',i['idea'],'|',i['esito'])
