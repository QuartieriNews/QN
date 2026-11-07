# Un ripristino puo' fermarsi a meta': la nota cita come prova una frase della fonte che nomina due
# persone, nel campo ne e' tornata una sola. Nessun conteggio di formule lo vede - nel campo non e'
# rimasta una formula, e' rimasto il nome sbagliato al posto giusto - ma si trova a costo zero
# confrontando la nota con il campo. Non e' una misura: e' un elenco di candidate, e i falsi positivi
# ci sono per costruzione, perche' la nota cita la fonte e la fonte nomina anche chi non c'entra.
import csv, os, re, sys

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
# Nomi di almeno due parole: un nome solo ("Petracca") nella nota e' quasi sempre gia' nel campo o
# parte di una citazione, e l'elenco si riempirebbe di rumore.
NOME = re.compile(r"\b[A-ZÀ-Ú][a-zà-ù']{2,}(?:\s+(?:d[ei]'?\s+|de[ligl]{1,3}a?\s+)?[A-ZÀ-Ú][a-zà-ù']{2,})+")
ORGANI = re.compile(r"^(Roma|Municipio|Consiglio|Commissione|Assemblea|Regione|Lazio|Dipartimento|"
                    r"Ufficio|Il |La |Lo |Nel |Nella |Dal |Del )")


def main():
    righe = list(csv.DictReader(open(DB + '/notizie_candidate.csv', encoding='utf-8')))
    fuori = DB + '/ripristino_a_meta.csv'
    trovate = []
    con_nota = 0
    for r in righe:
        nota = r.get('note') or ''
        if 'ripristinato:' not in nota and 'corretto:' not in nota:
            continue
        con_nota += 1
        campo = ' '.join([r.get('titolo', ''), r.get('sintesi', ''), r.get('evidenza_locale', '')])
        manca = sorted({m.group(0) for m in NOME.finditer(nota)
                        if not ORGANI.match(m.group(0)) and len(m.group(0).split()) <= 3
                        and m.group(0) not in campo})
        if manca:
            trovate.append({'id': r['id'], 'fonte': r['fonte'], 'nomi_nella_nota': ' | '.join(manca),
                            'titolo': r.get('titolo', '')})
    with open(fuori, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['id', 'fonte', 'nomi_nella_nota', 'titolo'])
        w.writeheader(); w.writerows(trovate)
    print('righe con una nota di ripristino: %d' % con_nota)
    print('di queste, la nota nomina qualcuno che il campo non contiene: %d -> %s'
          % (len(trovate), os.path.basename(fuori)))
    for r in trovate[:8]:
        print('   %-6s %s' % (r['id'], r['nomi_nella_nota'][:80]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
