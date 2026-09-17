# Prepara i lotti della passata di ripristino dei nomi (DEC-105).
# Seleziona le righe in cui un nome e' stato sostituito da una formula di ruolo, aggancia a
# ognuna il file della fonte gia' scaricato, e scrive lotti pronti per i lettori.
# La regola di lettura e' SPECIFICA_NOMI_E_TERRITORIO.md; qui si decide solo *che cosa* guardare.
import csv, glob, os, re, sys, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
FUORI = NET + '/report2/ripristino'
PER_LOTTO = int(os.environ.get('PER_LOTTO', 35))
PREFISSO = os.environ.get('PREFISSO', 'R')

# Una sostituzione ha la forma "articolo + ruolo": e' cosi' che un lettore rende un nome tolto.
RUOLI = (r"consiglier[ae]|assessor[ae]|funzionari[oa]|dirigente|referente|relator[ae]|"
         r"cittadin[oa]|rappresentante|portavoce|richiedente|titolare|"
         r"attor[ei]|attrice|cantautor[ei]|cantautrice|cantante|regista|artista|"
         r"drammaturg[oa]|curator[ae]|moderator[ae]|scrittor[ei]|scrittrice|musicista|"
         r"ditta individuale|professionista|avvocat[oa]|architett[oa]|ingegner[ea]|"
         r"present(?:atore|atrice)|direttor[ei]|direttrice")
FORMULA = re.compile(r"\b(un|una|un'|il|lo|la|l')\s*(" + RUOLI + r")\b", re.I)
CAMPI_N = ['titolo_anonimizzato', 'sintesi', 'evidenza_locale']
CAMPI_D = ['titolo_anonimizzato']


def leggi(nome):
    return list(csv.DictReader(open(DB + '/' + nome, encoding='utf-8')))


def sorgenti(documenti):
    """documento_id -> percorso del testo gia' scaricato, per ciascuna delle quattro famiglie."""
    p = {}
    testi = {os.path.basename(f)[:-4] for f in glob.glob(NET + '/report1/texts/*.txt')}
    caption = {os.path.basename(f)[:-4] for f in glob.glob(NET + '/video/caps_txt/*.txt')}
    rtv = {r['url']: r['file'] for r in csv.DictReader(
        open(NET + '/report2/manifest_video_rtv.csv', encoding='utf-8'))}
    # A2: gli atti stanno nei file di lotto, nello stesso ordine dei documenti dello stesso lotto.
    atti = collections.defaultdict(list)
    for f in glob.glob(NET + '/report2/out/*_atti.csv'):
        if 'prima_del_fix' in f:
            continue
        lotto = os.path.basename(f).split('_')[0]
        atti[lotto] = [r['name'] for r in csv.DictReader(open(f, encoding='utf-8'))]
    per_lotto = collections.defaultdict(list)
    for d in documenti:
        if d['fonte'] == 'A2':
            per_lotto[d['letto_da']].append(d['id'])
    for lotto, ids in per_lotto.items():
        for i, doc_id in enumerate(ids):
            if i < len(atti.get(lotto, [])):
                p[doc_id] = 'A2_text/%s.txt' % atti[lotto][i]

    for d in documenti:
        i, f, u = d['id'], d['fonte'], d['url']
        if i in p:
            continue
        if f == 'A3' and u in rtv:
            p[i] = rtv[u]if rtv[u].startswith('video/') else 'video/' + rtv[u]
        elif f == 'A4' and u.split('v=')[-1] in caption:
            p[i] = 'video/caps_txt/%s.txt' % u.split('v=')[-1]
        elif i in testi:
            p[i] = 'report1/texts/%s.txt' % i
    return p


def formule_in(riga, campi):
    """Ogni campo e ogni occorrenza. La prima versione si fermava alla prima formula trovata:
    le successive nello stesso campo non entravano in lavorazione e restavano nel dato."""
    out = []
    for c in campi:
        trovate = [m.group(0) for m in FORMULA.finditer(riga.get(c) or '')]
        if trovate:
            out.append((c, trovate))
    return out


def gia_fatte():
    """(riga, campo) gia' chiusi da un patch consegnato: una passata non rifa' il lavoro fatto."""
    out = set()
    for f in glob.glob(FUORI + '/patch_*.csv'):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            out.add((r['riga'], r['campo']))
    return out


def main():
    documenti = leggi('documenti.csv')
    notizie = leggi('notizie_candidate.csv')
    fonte_di = {d['id']: d for d in documenti}
    percorso = sorgenti(documenti)

    fatte = gia_fatte()
    lavoro = []
    for n in notizie:
        for campo, formule in formule_in(n, CAMPI_N):
            if (n['id'], campo) in fatte:
                continue
            lavoro.append(dict(riga=n['id'], tabella='notizie', documento=n['documento_id'],
                               fonte=n['fonte'], campo=campo, formula=' | '.join(formule),
                               occorrenze=len(formule),
                               sorgente=percorso.get(n['documento_id'], ''),
                               letto_da=fonte_di.get(n['documento_id'], {}).get('letto_da', '')))
    for d in documenti:
        for campo, formule in formule_in(d, CAMPI_D):
            if (d['id'], campo) in fatte:
                continue
            lavoro.append(dict(riga=d['id'], tabella='documenti', documento=d['id'],
                               fonte=d['fonte'], campo=campo, formula=' | '.join(formule),
                               occorrenze=len(formule),
                               sorgente=percorso.get(d['id'], ''), letto_da=d['letto_da']))

    senza = [x for x in lavoro if not x['sorgente']]
    # Un lotto tiene insieme righe della stessa fonte: cosi' il lettore apre un tipo di file solo.
    lavoro.sort(key=lambda x: (x['fonte'], x['documento'], x['riga']))
    os.makedirs(FUORI, exist_ok=True)
    for v in glob.glob(FUORI + '/%s[0-9][0-9].csv' % PREFISSO):
        os.remove(v)
    campi = ['riga', 'tabella', 'documento', 'fonte', 'campo', 'formula', 'occorrenze',
             'sorgente', 'letto_da']
    n = 0
    for i in range(0, len(lavoro), PER_LOTTO):
        n += 1
        with open('%s/%s%02d.csv' % (FUORI, PREFISSO, n), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, campi)
            w.writeheader()
            w.writerows(lavoro[i:i + PER_LOTTO])
    per_fonte = collections.Counter(x['fonte'] for x in lavoro)
    print('righe da ripristinare: %d (%s)' % (len(lavoro), dict(per_fonte.most_common())))
    print('lotti scritti: %d da %d righe, in %s' % (n, PER_LOTTO, FUORI))
    if senza:
        print('SENZA FONTE LOCALE: %d — vanno lette dall\'URL o dichiarate' % len(senza))
        for x in senza[:5]:
            print('   ', x['riga'], x['fonte'], x['documento'])


if __name__ == '__main__':
    main()
