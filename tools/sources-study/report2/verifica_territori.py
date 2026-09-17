# Il controllo che l'owner ha chiesto il 17 settembre: che le notizie restino agganciate alla
# mappatura dei quartieri **sua**, cioe' al gazetteer del repository, anche dopo la rigenerazione.
# Non ricalcola l'attribuzione: la rilegge dal database finito e la confronta con il gazetteer.
# Un controllo che rifacesse il calcolo con lo stesso codice direbbe sempre di si'.
import csv, json, os, random, sys, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
G = json.load(open('/home/user/QN/gazetteer/gazetteer.json'))
ROM = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']

PER_NOME = {}
for n in G['neighbourhoods']:
    PER_NOME.setdefault(n['name_display'], []).append(n)


def municipi_di(n):
    out = {n['municipality_code']} if n.get('municipality_code') else set()
    out |= {x.strip() for x in (n.get('spans_municipalities') or '').replace('/', ',').split(',') if x.strip()}
    return {m for m in out if m in ROM}


def main():
    righe = list(csv.DictReader(open(DB + '/notizie_candidate.csv', encoding='utf-8')))
    ignoti, zu_disallineati, mun_incoerenti = [], [], []
    con_q = 0
    quartieri = collections.Counter()
    for r in righe:
        nomi = [x for x in (r.get('quartiere') or '').split(';') if x.strip()]
        if not nomi:
            continue
        con_q += 1
        # Posizionale: zu[i] e' la zona urbanistica di nomi[i], vuota compresa.
        zu = (r.get('quartiere_zu') or '').split(';')
        if zu != [''] and len(zu) != len(nomi):
            zu_disallineati.append((r['id'], 'conteggio', len(zu), len(nomi)))
            zu = []
        mun_gaz = set()
        for i, nome in enumerate(nomi):
            quartieri[nome] += 1
            voci = PER_NOME.get(nome)
            if not voci:
                # Un nome che il gazetteer non conosce vuol dire che l'aggancio si e' rotto.
                ignoti.append((r['id'], nome))
                continue
            for v in voci:
                mun_gaz |= municipi_di(v)
            atteso = {v.get('zu_code') or '' for v in voci}
            if i < len(zu) and zu[i] not in atteso:
                zu_disallineati.append((r['id'], nome, zu[i], sorted(atteso)))
        dichiarati = {m for m in (r.get('municipio') or '').split(';') if m in ROM}
        # Il Municipio della fonte non viene riscritto (regola 4 dello schema): quando non
        # corrisponde al quartiere, quello che si pretende e' che la riga sia marcata da
        # verificare. Una discordanza silenziosa e' il difetto; una dichiarata non lo e'.
        if dichiarati and mun_gaz and not (dichiarati & mun_gaz) \
                and (r.get('territorio_dedotto') or '') != 'misto' \
                and (r.get('toponimo_da_verificare') or '').strip().lower() not in ('sì', 'si'):
            mun_incoerenti.append((r['id'], sorted(dichiarati), sorted(mun_gaz),
                                   r.get('territorio_dedotto')))

    print('righe con quartiere: %d su %d — quartieri distinti: %d'
          % (con_q, len(righe), len(quartieri)))
    print('nomi fuori dal gazetteer: %d' % len(ignoti))
    for x in ignoti[:10]:
        print('   ', x)
    print('zona urbanistica non allineata al quartiere: %d' % len(zu_disallineati))
    for x in zu_disallineati[:10]:
        print('   ', x)
    print('Municipio incoerente col quartiere e non dichiarato: %d' % len(mun_incoerenti))
    for x in mun_incoerenti[:10]:
        print('   ', x)

    # Campione a seme fisso: serve che l'owner possa rifare lo stesso controllo e trovare le
    # stesse righe, non un campione nuovo a ogni esecuzione.
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    rng = random.Random('territori-2026-09-17')
    campione = rng.sample([r for r in righe if (r.get('quartiere') or '').strip()], n)
    fuori = DB + '/campione_territori.csv'
    with open(fuori, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['id', 'fonte', 'titolo', 'luoghi', 'municipio',
                                          'quartiere', 'quartiere_zu', 'territorio_dedotto',
                                          'toponimo_da_verificare'],
                           extrasaction='ignore')
        w.writeheader(); w.writerows(campione)
    print('\ncampione da controllare a mano: %s (%d righe, seme fisso)' % (fuori, n))
    for r in campione[:8]:
        print('  %-6s %-28s | %-4s | %s (%s)%s' % (r['id'], (r.get('luoghi') or '')[:28],
              r.get('municipio'), r.get('quartiere'), r.get('territorio_dedotto'),
              '  DA VERIFICARE' if (r.get('toponimo_da_verificare') or '').lower() in ('sì', 'si') else ''))
    print('\ni dieci quartieri piu' + "'" + ' ricorrenti: %s' % [q for q, _ in quartieri.most_common(10)])
    return 1 if (ignoti or zu_disallineati) else 0


if __name__ == '__main__':
    sys.exit(main())
