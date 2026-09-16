# La risposta del rapporto, calcolata invece che ricopiata.
# Finora l'ho ricalcolata a mano a ogni lotto che rientrava, e a mano si sbaglia: e' il numero che
# il §7-bis promette riproducibile, quindi deve venire da qui.
#   quota di novita' = (S + U*(1-p)) / N
# dove p e' la quota di candidate incerte che un lettore, aprendo i testi, ha giudicato gemelle
# vere. p si legge dai file dell'audit, **contata per candidata**: una candidata e' gemella vera se
# almeno uno dei suoi accostamenti lo e'. Dove una candidata e' stata rigiudicata sul campione
# rifatto (STATO §105), **vale il rigiudizio**, non il giudizio dato su un campione che non le
# mostrava gli accostamenti.
import csv, collections, math, os

NET = os.environ['QN_NET']
PARLATO = {'A3', 'A4'}

righe = [r for r in csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8'))
         if r['fonte'] in PARLATO]
def classe(v):
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')
c = collections.Counter(classe(r['gemelli_scritti']) for r in righe)
S, U, D = c['S'], c['U'], c['D']; N = S + U + D

def per_candidata(nome, idcol, sezione):
    p = NET + '/report2/out/' + nome
    out = {}
    if not os.path.exists(p): return out
    for r in csv.DictReader(open(p, encoding='utf-8')):
        if sezione(r) != 'C': continue
        out[r[idcol]] = out.get(r[idcol], False) or r['giudizio'].strip() == 'stesso fatto'
    return out

giudizi = {}
giudizi.update(per_candidata('AUDIT_dubbi.csv', 'id_parlata', lambda r: r['caso'][0]))
giudizi.update(per_candidata('AUDIT2_dedup.csv', 'id_parlata', lambda r: r['sezione']))
rig = per_candidata('AUDIT3_rigiudizio.csv', 'id_parlata', lambda r: r['sezione'])
sostituite = len(set(giudizi) & set(rig))
giudizi.update(rig)

n = len(giudizi); veri = sum(giudizi.values())
p = veri / n

def wilson(k, n, z=1.96):
    if not n: return (0.0, 1.0)
    f = k / n; d = 1 + z * z / n
    centro = (f + z * z / (2 * n)) / d
    mezzo = z * math.sqrt(f * (1 - f) / n + z * z / (4 * n * n)) / d
    return (centro - mezzo, centro + mezzo)

lo, hi = wilson(veri, n)
def quota(x): return 100 * (S + U * (1 - x)) / N

print('classi (confronto esaustivo parlato-contro-scritto): S=%d U=%d D=%d  N=%d' % (S, U, D, N))
print('intervallo grezzo: [%.1f%% , %.1f%%]' % (100 * S / N, 100 * (S + U) / N))
print('candidate incerte giudicate: %d, gemelle vere %d  ->  p = %.1f%%  (IC 95%% Wilson [%.1f%% , %.1f%%])'
      % (n, veri, 100 * p, 100 * lo, 100 * hi))
if rig: print('  di cui rigiudicate sul campione rifatto: %d (il rigiudizio sostituisce il giudizio vecchio)' % sostituite)
print('RISPOSTA: %.1f%%   banda [%.1f%% , %.1f%%]' % (quota(p), quota(hi), quota(lo)))

# --- la novita' **certa** (classe S) corretta con precisione e richiamo misurati ----------------
# S sovrastima chi non ha gemelli, perche' il confronto ne manca (richiamo), e D sovrastima chi ne
# ha, perche' accosta a sproposito (precisione). La correzione, scritta per esteso invece che
# ricopiata da una versione precedente del rapporto:
#     S corretta = S * (1 - richiamo_perso) + D * (1 - precisione_forti)
# dove `richiamo_perso` e' la quota di candidate date per nuove che un lettore ha trovato gemelle
# (sezione B) e `precisione_forti` la quota di accostamenti forti giudicati stesso fatto.
def coppie_giudicate(nome, idcol, idscr, sezione):
    p = NET + '/report2/out/' + nome
    out = {}
    if not os.path.exists(p): return out
    for r in csv.DictReader(open(p, encoding='utf-8')):
        if sezione(r) != 'A': continue
        out[(r[idcol], r[idscr])] = r['giudizio'].strip() == 'stesso fatto'
    return out

forza = {}
for c in csv.DictReader(open(NET + '/report2/coppie_parlato_scritto.csv', encoding='utf-8')):
    forza[(c['parlata'], c['scritta'])] = c['forza']

coppie = {}
coppie.update(coppie_giudicate('AUDIT_dedup.csv', 'id_a', 'id_b', lambda r: r['sezione']))
coppie.update(coppie_giudicate('AUDIT2_dedup.csv', 'id_parlata', 'id_scritta', lambda r: r['sezione']))
coppie.update(coppie_giudicate('AUDIT3_rigiudizio.csv', 'id_parlata', 'id_scritta', lambda r: r['sezione']))
forti = {k: v for k, v in coppie.items() if forza.get(k) == 'forte'}

richiamo = {}
for nome, idcol, sez in (('AUDIT_dedup.csv', 'id_a', lambda r: r['sezione']),
                         ('AUDIT2_dedup.csv', 'id_parlata', lambda r: r['sezione'])):
    p = NET + '/report2/out/' + nome
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p, encoding='utf-8')):
        if sez(r) != 'B': continue
        richiamo[r[idcol]] = richiamo.get(r[idcol], False) or r['giudizio'].strip() == 'stesso fatto'

if forti and richiamo:
    prec = sum(forti.values()) / len(forti)
    perso = sum(richiamo.values()) / len(richiamo)
    S_corr = S * (1 - perso) + D * (1 - prec)
    print()
    print('precisione degli accostamenti forti: %d su %d = %.1f%%' % (sum(forti.values()), len(forti), 100 * prec))
    print('richiamo: %d gemelli veri su %d candidate date per nuove = %.1f%% perso'
          % (sum(richiamo.values()), len(richiamo), 100 * perso))
    print('novita certa corretta: %.1f%% (grezza %.1f%%)' % (100 * S_corr / N, 100 * S / N))
