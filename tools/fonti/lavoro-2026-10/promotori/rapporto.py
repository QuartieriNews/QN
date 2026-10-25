# Testo del §1 nonies del rapporto sulle fonti (solo numeri, categorie e nomi di enti: nessun testo, titolo o contatto delle fonti)
import json,collections,os
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
R=json.load(open(f'{P}/promotori_finale.json')); I=json.load(open(f'{P}/idee.json')); D=json.load(open(f'{P}/diffusione_riepilogo.json'))
IM=json.load(open(f'{P}/immagini.json')); E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
n=len(R); f=lambda k: sum(1 for r in R if r.get(k))
def it(x): return f"{x:,}".replace(',','.')
cat=collections.defaultdict(list)
for r in R: cat[r['categoria']].append(r)
rows=[]
for c,rs in sorted(cat.items(),key=lambda kv:-sum(r['n_eventi'] for r in kv[1])):
    ev=sum(r['n_eventi'] for r in rs); evw=sum(r['in_pagine_deboli'] for r in rs)
    rows.append(f"| {c} | {len(rs)} | {ev} | {round(100*evw/ev) if ev else 0}% |")
DC=json.load(open(f'{P}/deboli_categorie.json')); Q=DC['quota_eventi_in_pagine_deboli']
big=[c for c,rs in cat.items() if sum(r['n_eventi'] for r in rs)>=30 and c!='Non classificato']
hi=sorted(big,key=lambda c:-Q.get(c,0))[:3]; lo=sorted(big,key=lambda c:Q.get(c,0))[:3]
lab={'Parrocchie e realtà religiose':'parrocchie e realtà religiose','Associazioni culturali e artistiche':'associazioni','Sport e movimento':'realtà sportive',
     'Comitati di quartiere e reti civiche':'comitati','Centri sociali, centri anziani e spazi di comunità':'centri anziani o sociali'}
ex=[(lab[c],DC['esistenti'].get(c,0),DC['attivi'].get(c,0)) for c in lab]
lettura=(f"le più legate alle periferie sono {', '.join(f'{c.lower()} ({Q[c]}%)' for c in hi)}; le meno {', '.join(f'{c.lower()} ({Q[c]}%)' for c in lo)}. "
         f"Nelle 41 pagine deboli la lista supplementare (§1 octies) ha trovato " + ', '.join(f"{e} {n}" for n,e,a in ex) +
         "; i promotori di quelle categorie con almeno un evento nel calendario in quelle pagine sono " + ', '.join(f"{a} ({round(100*a/e) if e else 0}%)" for n,e,a in ex) +
         ". Il buco non è di soggetti: è di eventi che arrivano online.")
imc=collections.Counter(r['esito'] if not r['esito'].startswith('errore') else 'errore' for r in IM)
NOTE={'Teatro Degli Audaci':"il Teatro degli Audaci vieta riproduzione e diffusione senza autorizzazione scritta, ma ammette un estratto fino al 15% del testo con link all'originale e nome dell'autore",
      'Romaeuropa Festival':'Romaeuropa non consente di usare contenuti e marchi del sito per scopi diversi da quelli del sito',
      'Azione Cattolica Italiana':"Azione Cattolica consente solo usi personali dei contenuti",
      'Indipendente Concerti':'il sito di riferimento è quello di Live Nation, i cui termini vietano di copiare o distribuire parti del sito senza autorizzazione scritta'}
NOTE.update({k:'VignaClaraBlog vieta la riproduzione anche parziale senza approvazione scritta' for k in [r['nome'] for r in R] if k.startswith('VignaClaraBlog')})
txt=f"""## 1 nonies. Promotori degli eventi, categorie, ricerche integrative, immagini e diffusione (M, 25 ottobre 2026)

**Promotori.** Chi organizza i {it(len(E))} eventi futuri della pagina degli eventi di quartiere: host degli
eventi Facebook (con il link alla pagina), pagina che annuncia nel post, «a cura di» di culture.roma.it, la
sede per l'agenda delle Biblioteche di Roma, la fonte per i siti; i co-organizzatori sono separati. {it(n)} promotori; per {it(f('email'))} c'è un'email
({round(100*f('email')/n)}%), per {it(f('sito'))} un sito, per {it(f('facebook'))} una pagina Facebook, per {it(f('instagram'))} un profilo
Instagram, per {it(f('telefono'))} un telefono. Dati da: profili Facebook già letti nei censimenti e 425 letti ora,
RUNTS, censimento associazioni, lista supplementare, contatti per evento di culture.roma.it, siti dei
promotori letti ora (homepage, contatti, chi siamo, note legali; robots.txt rispettato) e una ricerca Google
dei canali per chi non ne aveva. Ogni promotore ha una categoria, un ambito, le attività prevalenti, una
descrizione breve scritta da regole con le nostre etichette e una descrizione lunga che aggiunge, tra
virgolette, come il soggetto si presenta. Il foglio completo (`promotori_eventi.xlsx`) sta su Drive; la wiki
ha la pagina generata `docs/wiki/fonti-eventi/promotori.md` con categoria, descrizione breve, canali, se
esiste un contatto e la posizione sulla diffusione, senza email, telefoni né testi delle fonti (DEC-102,
DEC-109; test T-FE-10).

| Categoria | Promotori | Eventi | Quota nelle 41 pagine deboli |
|---|---|---|---|
""" + "\n".join(rows) + f"""

**Lettura per categoria.** Quota degli eventi di ogni categoria che cade nelle 41 pagine deboli:
""" + lettura + f"""

**Ricerche integrative** (spesa massima approvata 25 dollari):

| Idea | Stato | Costo | Esito |
|---|---|---|---|
""" + "\n".join(f"| {i['idea']} | {i['stato']} | {i['costo']} | {i['esito']} |" for i in I) + f"""

**Correzioni alla lista supplementare.** Un post pubblicato da una pagina diversa dal soggetto non prende
più la zona della sede del soggetto, e i post di pagine non collegate a un soggetto della lista
supplementare sono scartati. Il lettore dei siti aveva seguito come «sito» di un soggetto un articolo di
Roma Today e ne aveva letto anche la home e la pagina degli eventi: contro DEC-026, che fuori dalla lettura
una tantum del 23 ottobre non ammette letture di Roma Today. I tre blocchi datati presi da lì sono tolti
dalla pagina e dal foglio della lista supplementare, e Roma Today è escluso nel lettore dei siti, nel lettore della lista
supplementare e nella raccolta degli eventi. Gli eventi della lista supplementare nella pagina sono ora
{sum(1 for e in E if e['o'].startswith('lista supplementare'))} (88 nel §1 octies).

**Immagini (DEC-101).** Per ogni evento della pagina l'immagine della fonte è scaricata una volta e
salvata a risoluzione da card (lato lungo 800 px), con `source_image_url`, `image_fetched_at`,
`image_local_path`, `image_credit` e `image_removed`: {it(imc.get('scaricata',0))} immagini. Non scaricate: Roma Today
(licenza Citynews, DEC-026), eventi Fever (asset commerciali), blocchi di testo dei siti senza pagina
dell'evento; {it(imc.get('nessuna immagine alla fonte',0))} eventi non hanno immagine alla fonte. Archivio e manifest su Drive
(`immagini_eventi.zip`, `immagini_eventi_manifest.xlsx`), mai nel repository.

**Diffusione.** Posizione di ogni fonte sui propri contenuti, dal sito (note legali, termini, piè di
pagina, robots.txt, riserva di estrazione TDM) o dai termini della piattaforma:

| Posizione | Promotori | Eventi (posizione più restrittiva fra i promotori dell'evento) |
|---|---|---|
""" + "\n".join(f"| {k} | {D['promotori_per_posizione'].get(k,0)} | {D['eventi_per_posizione_piu_restrittiva'].get(k,0)} |" for k in ['riproduzione vietata','raccolta automatica vietata','licenza richiesta','termini della piattaforma','diritti riservati (generico)','licenza aperta','nessuna indicazione','non verificabile']) + f"""

Gli stessi eventi per canale da cui li leggiamo (la posizione del canale vale anche quando il promotore non dice nulla):

| Canale | Posizione | Eventi |
|---|---|---|
""" + "\n".join(f"| {c} | {p} | {n} |" for c,p,n in D['eventi_per_canale']) + f"""

Vietano esplicitamente la riproduzione dei contenuti: {', '.join(f"{a} ({b} event{'o' if b==1 else 'i'})" for a,b,_ in D['promotori_riproduzione_vietata'])}
(clausole rilette una per una: {'; '.join(NOTE[a] for a,_,_ in D['promotori_riproduzione_vietata'] if a in NOTE)}).
Vietano la raccolta automatica (termini o robots.txt): {', '.join(f"{a}" for a,b,_ in D['promotori_raccolta_vietata'])}. Facebook e Instagram
(termini di Meta: raccolta automatica vietata senza permesso) portano {it(D['eventi_da_facebook'])} eventi su {it(D['eventi_totali'])}; Roma Today
richiede licenza (DEC-026); le note legali di Roma Capitale (anche per culture.roma.it) riservano i diritti
sui contenuti senza licenza di riuso; il sito delle Biblioteche di Roma non dice nulla sui contenuti (il suo
«copyright» riguarda il software del catalogo). Nessuna delle clausole lette vieta di dare notizia di un evento: i fatti (cosa,
quando, dove, chi) non sono protetti; lo sono testi e immagini, e la banca dati contro estrazioni
sistematiche. Conseguenza operativa, già nelle regole: scriviamo i nostri testi con credito e link
(DEC-102), e per le fonti che vietano la riproduzione si usa la card generata invece dell'immagine
(DEC-101); la posizione sulla raccolta automatica di Facebook resta quella di DEC-102.

"""
open(f'{P}/rapporto_1nonies.md','w').write(txt); print(txt[:3000])
