# Gli accenti resi con l'apostrofo ("citta'", "piu'", "sara'") arrivano dai file dei lettori e
# toccano un terzo del corpus. Si sistemano qui, dopo il ripristino, perche' e' una correzione
# meccanica e non una rilettura.
#
# Il criterio e' la certezza, non la copertura: si correggono **solo** le forme elencate, dove
# l'accento e' l'unica lettura possibile. Le troncature legittime dell'italiano - po', mo', be',
# un', dell' - non sono in elenco e restano intatte, che e' il motivo per cui l'elenco esiste
# invece di una regola generale su "vocale + apostrofo".
import csv, os, re, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
TABELLE = ('notizie_candidate.csv', 'documenti.csv', 'vicende.csv')
CAMPI = ('titolo', 'sintesi', 'evidenza_locale', 'note', 'ragione_dedup', 'luoghi')

A = ('citta attivita societa disabilita mobilita opportunita localita modalita qualita realta '
     'universita liberta novita eta meta unita comunita autorita priorita necessita possibilita '
     'capacita identita specificita particolarita continuita gratuita meta sara verra andra '
     'fara dara stara avra potra sapra vivibilita accessibilita sostenibilita pubblicita '
     'velocita criticita difficolta volonta poverta papa gia').split()
E_ACUTO = 'perche poiche benche affinche ne se giacche purche anziche finche ventitre'.split()
E_GRAVE = 'e cioe caffe ahime'.split()  # "e'" non e' una troncatura: in italiano vale sempre "e'" -> e grave
I = 'cosi lunedi martedi mercoledi giovedi venerdi si'.split()
O = 'puo pero cio'.split()
U = 'piu giu virtu tribu'.split()

# Seconda tornata, ricavata dalle forme davvero presenti nel corpus e vagliata a mano una per una.
# Il vaglio serve perche' l'apostrofo diritto fa anche da virgoletta di chiusura: nel residuo
# "terra'", "assessora'", "municipio'", "umberto'" non sono accenti mancati ma citazioni chiuse.
# "prego'" resta fuori per lo stesso motivo: in una seduta "prego" e' la parola comune, "prego'"
# passato remoto no. Restano fuori anche "uscita" e "auleta", che sono parole piane, e "da'",
# "sta'", "de'", troncature legittime.
A += ('abusivita affettivita agibilita ambiguita annualita attrattivita austerita biodiversita '
      'brevita calamita cavita ciclabilita circolarita collaudabilita collettivita conflittualita '
      'conformita conoscibilita contiguita contrarieta creativita criminalita densita difformita '
      'disponibilita diversita elettricita entita eseguibilita fattibilita federsolidarieta '
      'femminilita finalita fragilita genitorialita identificabilita impossibilita incidentalita '
      'inclusivita incolumita insalubrita intensita interattivita irregolarita legalita '
      'legittimita maternita micromobilita modatita morosita multimprenditorialita nazionalita '
      'normalita occupabilita operativita parita paternita pedonalita pericolosita personalita '
      'potabilita potenzialita premialita probabilita profondita proprieta prossimita quantita '
      'regolarita responsabilita sanabilita sanita socialita solidarieta specialita stabilita '
      'staticita storicita territorialita totalita tracciabilita trinita unanimita validita '
      'varieta verita viabilita visibilita vocalita facolta pieta cinecitta videocitta agora '
      # futuri e condizionali: la forma piana non esiste, quindi l'apostrofo e' sempre accento.
      'accogliera accorpera acquisira affianchera aggiungera animera approvera aprira arrivera '
      'assegnera attivera bisognera cerchera chiedera chiudera coinvolgera comportera concludera '
      'consentira continuera convochera costruira diventera durera effettuera eleggera entrera '
      'eseguira esibira estendera fermera garantira immettera inaugurera insistera interpellera '
      'mettera occupera ospitera parlera partecipera partira passera permettera portera '
      'predisporrera prendera privilegera procedera proseguira realizzera registrera restera '
      'riaprira ricevera richiedera rifara riferira ripetera riprendera rispondera riunira '
      'salvera seguira servira sollecitera sorgera suonera svolgera telefonera tornera '
      'trasmettera valutera vietera dovra vorra rimarra interverra condurra rifa').split()
I += 'altresi bensi'.split()
O += 'percio niccolo dovro andro daro concordero'.split()
U += 'gesu gioventu servitu matemu'.split()

MAPPA = {}
for w in A:
    MAPPA[w] = w[:-1] + 'à'
for w in E_ACUTO:
    MAPPA[w] = w[:-1] + 'é'
for w in E_GRAVE:
    MAPPA[w] = w[:-1] + 'è'
for w in I:
    MAPPA[w] = w[:-1] + 'ì'
for w in O:
    MAPPA[w] = w[:-1] + 'ò'
for w in U:
    MAPPA[w] = w[:-1] + 'ù'

RE = re.compile(r"\b(" + "|".join(sorted(MAPPA, key=len, reverse=True)) + r")'", re.I)
RESTA = re.compile(r"\b\w+[aeiou]'(?=\s|$|[,.;:!?»)])")
# Le troncature in cui l'apostrofo e' giusto: non vanno contate come residuo da sistemare.
LEGITTIME = re.compile(r"\b(po|mo|be|un|dell|nell|all|dall|sull|quell|bell|sant|grand|"
                       r"l|d|c|n|s|v|gl|qualcos|tutt|cert|quest|quall)'", re.I)


def accenta(s):
    def sost(m):
        # Si sostituisce **solo** l'ultima lettera: le maiuscole interne dei nomi propri
        # ("MaTeMu'") sono come le scrive la fonte e non vanno normalizzate per strada.
        p = m.group(1)
        accentata = MAPPA[p.lower()][-1]
        return p[:-1] + (accentata.upper() if p.isupper() else accentata)
    return RE.sub(sost, s or '')


def main():
    corretti = collections.Counter()
    residui = collections.Counter()
    for tab in TABELLE:
        percorso = DB + '/' + tab
        if not os.path.exists(percorso):
            continue
        righe = list(csv.DictReader(open(percorso, encoding='utf-8')))
        if not righe:
            continue
        campi = list(righe[0])
        for r in righe:
            for c in CAMPI:
                if c in campi and r[c]:
                    nuovo = accenta(r[c])
                    if nuovo != r[c]:
                        corretti[tab] += 1
                        r[c] = nuovo
                    for m in RESTA.finditer(r[c]):
                        if not LEGITTIME.match(m.group(0)):
                            residui[m.group(0).lower()] += 1
        with open(percorso, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore')
            w.writeheader(); w.writerows(righe)
    print('accenti ripristinati: %s' % (dict(corretti) or 'nessuno'))
    if residui:
        print('apostrofi non in elenco, lasciati intatti: %d forme, %d occorrenze'
              % (len(residui), sum(residui.values())))
        print('   le piu\' frequenti: %s' % [w for w, _ in residui.most_common(10)])


if __name__ == '__main__':
    main()
