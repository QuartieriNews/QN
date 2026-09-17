# Applica al database i patch della passata di ripristino (DEC-105).
# I lettori consegnano patch invece di scrivere sui CSV: due che scrivono lo stesso file lo
# corrompono, e un passo unico si rivede. Qui si controlla tutto prima di toccare qualcosa.
import csv, glob, os, re, shutil, sys, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
PATCH = NET + '/report2/ripristino'
TABELLE = {'notizie': 'notizie_candidate.csv', 'documenti': 'documenti.csv'}
# I patch sono stati scritti quando la colonna si chiamava ancora `titolo_anonimizzato`.
# Il nome cambia (DEC-105), i patch no: la corrispondenza sta qui e non nei dati.
ALIAS = {'titolo_anonimizzato': 'titolo'}

# La sostituzione lascia residui di spaziatura ("Alfonsi , con"): il lettore corregge il nome,
# la punteggiatura la sistema una regola, non una rilettura.
def ripulisci(s):
    s = re.sub(r"\s+([,;.:!?])", r"\1", s)
    s = re.sub(r"([«(])\s+", r"\1", s)
    s = re.sub(r"\s+([»)])", r"\1", s)
    return re.sub(r"[ \t]{2,}", " ", s).strip()


# Una passata di revisione torna apposta su campi gia' lavorati, e il suo valore vince su quello
# della prima lettura: `patch_incerti` e' il riscontro sull'audio e sulle altre fonti della stessa
# seduta; i lotti `F` sono la passata finale e `M` la misura del residuo, che leggono il database
# **dopo** i patch precedenti e quindi portano quello che c'era piu' quello che hanno trovato.
# La differenza con un conflitto sta tutta qui: la revisione e' dichiarata in anticipo, il conflitto
# no. Due letture indipendenti che divergono restano un errore e fermano tutto.
REVISIONI = ('patch_incerti.csv', 'patch_F', 'patch_M')


def revisione(nome):
    return nome.startswith(REVISIONI)


# Una revisione che perde un nome che c'era gia' e' quasi sempre una correzione (cognome -> nome e
# cognome, «Grande» -> «Grant», «Paschio» -> «Fassio»), ma e' anche la forma che avrebbe un ritorno
# indietro silenzioso. Si stampa, non si blocca: il giudizio su quale delle due sia resta a chi legge.
NOME_PROPRIO = re.compile(r"\b[A-ZÀ-Ú][a-zà-ú']{2,}(?:\s+[A-ZÀ-Ú][a-zà-ú']{2,})*")
NON_NOMI = {'Roma', 'Capitale', 'Municipio', 'Consiglio', 'Commissione', 'Assemblea', 'Regione',
            'Lazio', 'Presidente', 'Assessore', 'Consigliere', 'Consigliera'}


def nomi_propri(s):
    return {x for x in NOME_PROPRIO.findall(s or '') if x not in NON_NOMI and len(x) > 3}


def carica_patch():
    righe, visti = [], {}
    prima = [f for f in sorted(glob.glob(PATCH + '/patch_*.csv'))
             if not revisione(os.path.basename(f))]
    poi = [f for f in sorted(glob.glob(PATCH + '/patch_*.csv'))
           if revisione(os.path.basename(f))]
    riviste = 0
    for f in prima + poi:
        nome = os.path.basename(f)
        for r in csv.DictReader(open(f, encoding='utf-8')):
            r['_file'] = nome
            chiave = (r['riga'], r['campo'])
            # «invariato» senza valore non e' una revisione del testo: e' un riscontro che non ha
            # trovato niente. Il campo resta come la passata precedente lo ha lasciato, e di questa
            # riga valgono solo la ragione e i flag. Trattarla come superamento cancellerebbe un
            # nome gia' ripristinato con la sua prova.
            rivede = revisione(nome) and (r.get('valore_nuovo') or '').strip() \
                and r['esito'] in ('ripristinato', 'corretto', 'fuori_seduta')
            if chiave in visti and visti[chiave][0] != r.get('valore_nuovo', '') and (
                    not revisione(nome) or rivede):
                if not rivede:
                    print('CONFLITTO su %s %s: %s (%s) e %s (%s) divergono'
                          % (r['riga'], r['campo'], visti[chiave][0][:40], visti[chiave][1],
                             r.get('valore_nuovo', '')[:40], nome))
                    sys.exit(1)
                # La riga superata esce dall'elenco: applicarle entrambe farebbe dipendere il
                # risultato dall'ordine di scrittura, che e' il modo peggiore di decidere.
                persi = nomi_propri(visti[chiave][0]) - nomi_propri(r.get('valore_nuovo', ''))
                if persi:
                    print('rivisto %s %s (%s -> %s): non c\'e\' piu\' %s'
                          % (r['riga'], r['campo'], visti[chiave][1], nome, sorted(persi)))
                righe = [x for x in righe if (x['riga'], x['campo']) != chiave]
                riviste += 1
            if chiave not in visti or rivede:
                visti[chiave] = (r.get('valore_nuovo', ''), nome)
            righe.append(r)
    if riviste:
        print('campi rivisti da una passata di riscontro: %d' % riviste)
    return righe


def main():
    patch = carica_patch()
    esiti = collections.Counter(r['esito'] for r in patch)
    per_tab = collections.defaultdict(list)
    for r in patch:
        per_tab[r['tabella']].append(r)

    fuori = [r for r in patch if r['esito'] == 'fuori_seduta']
    applicati = mancanti = spostati = 0
    # Un patch puo' sbagliare la tabella: l'identificativo e' univoco fra le due, quindi la riga
    # si ritrova invece di perderla. Si dichiara, perche' e' un errore che vale la pena vedere.
    indici = {}
    for tab, nome in TABELLE.items():
        indici[tab] = {r['id'] for r in csv.DictReader(open(DB + '/' + nome, encoding='utf-8'))}
    for p in patch:
        if p['riga'] not in indici.get(p['tabella'], set()):
            altra = next((k for k in TABELLE if p['riga'] in indici[k]), None)
            if altra:
                print('tabella corretta: %s dichiarata %s, e\' in %s (%s)'
                      % (p['riga'], p['tabella'], altra, p['_file']))
                p['tabella'] = altra
                spostati += 1
    per_tab = collections.defaultdict(list)
    for r in patch:
        per_tab[r['tabella']].append(r)
    for tab, elenco in per_tab.items():
        percorso = DB + '/' + TABELLE[tab]
        righe = list(csv.DictReader(open(percorso, encoding='utf-8')))
        campi = list(righe[0])
        indice = {r['id']: r for r in righe}
        for p in elenco:
            campo = p['campo'] if p['campo'] in campi else ALIAS.get(p['campo'], p['campo'])
            if campo not in campi:
                print('colonna assente:', p['campo'], p['_file']); mancanti += 1; continue
            r = indice.get(p['riga'])
            if r is None:
                print('riga assente:', p['riga'], p['_file']); mancanti += 1; continue
            if p['esito'] in ('ripristinato', 'corretto') and p.get('valore_nuovo'):
                r[campo] = ripulisci(p['valore_nuovo']); applicati += 1
            # La ragione si conserva sempre, non solo quando il nome resta fuori: un'attribuzione
            # fatta con un dubbio dichiarato deve portarsi dietro il dubbio, o il dubbio sparisce.
            nota = (p.get('ragione') or '').strip()
            if nota and 'note' in campi:
                r['note'] = ((r.get('note') or '') + ' | ' if r.get('note') else '') + \
                    ('%s: %s' % (p['esito'], nota))
            # I primi patch non avevano la colonna del flag: la ragione lo dice a parole.
            incerta = (p.get('trascrizione_incerta') or '').strip().lower() in ('sì', 'si') \
                or bool(re.search(r'trascri\w*\s+incert|forma udita|oscilla|mal trascritt', nota, re.I))
            if p['esito'] == 'fuori_seduta':
                # DEC-105 §2: il materiale fuori seduta non resta nei file, nemmeno riassunto.
                for c in ('titolo', 'titolo_anonimizzato', 'sintesi'):
                    if c in campi:
                        r[c] = ''
                if 'fuori_perimetro' in campi:
                    r['fuori_perimetro'] = 'sì'
            if (p.get('attribuzione_incerta') or '').strip().lower() in ('sì', 'si') \
                    and 'attribuzione_incerta' in campi:
                r['attribuzione_incerta'] = 'sì'
            if incerta:
                if 'trascrizione_incerta' in campi:
                    r['trascrizione_incerta'] = 'sì'
                elif 'note' in campi:
                    r['note'] = ((r.get('note') or '') + ' | ' if r.get('note') else '') + \
                        'trascrizione incerta sul nome'
        shutil.copy(percorso, percorso + '.prima_del_ripristino')
        with open(percorso, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore')
            w.writeheader(); w.writerows(righe)
        print('%s: %d righe riscritte' % (TABELLE[tab], len(righe)))

    print('patch: %s' % dict(esiti))
    print('campi sostituiti: %d, righe non trovate: %d, tabella corretta: %d'
          % (applicati, mancanti, spostati))
    if fuori:
        print('da escludere perche fuori seduta: %d' % len(fuori))
        for r in fuori:
            print('   %s %s %s' % (r['riga'], r['campo'], r.get('minutaggio', '')))


if __name__ == '__main__':
    main()
