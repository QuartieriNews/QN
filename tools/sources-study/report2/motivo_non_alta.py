# Il settimo emendamento chiede che ogni candidata che non arriva a `qualita: alta` dica in una
# parola perche': `data`, `luogo`, `non compiuto`, `trascrizione`. Serve a misurare la scala invece
# di cambiarla: se una candidata e' compiuta e localizzata e manca solo il quando, la nostra regola
# la declassa per una proprieta' che in aula la porta quasi sempre **l'atto letto ad alta voce** —
# cioe' il requisito «datato» funziona come un test sull'esistenza dell'atto travestito da test sul
# fatto.
# I lotti letti prima dell'emendamento non hanno la parola: si contano a parte, non si indovinano.
import json, os, re, collections

NET = os.environ['QN_NET']
MOTIVI = ('data', 'luogo', 'non compiuto', 'trascrizione')

c = collections.Counter()
per_motivo_novita = collections.Counter()
lotti_con = set()
for f in sorted(os.listdir(NET + '/report2/out_video')):
    j = json.load(open(NET + '/report2/out_video/' + f, encoding='utf-8'))
    for x in j.get('notizie_candidate', []):
        if x.get('qualita') == 'alta':
            c['alta'] += 1; continue
        nota = (x.get('nota') or '').lower()
        trovati = [m for m in MOTIVI if re.search(r'\b' + m.replace(' ', r'\s'), nota)]
        if not trovati:
            c['senza motivo dichiarato'] += 1; continue
        lotti_con.add(f[:6])
        if len(trovati) > 1:
            c['piu di un motivo'] += 1
        else:
            c['motivo: ' + trovati[0]] += 1
            if trovati[0] == 'data':
                per_motivo_novita[x.get('novita_rispetto_agli_atti', '?')] += 1

dichiarate = sum(v for k, v in c.items() if k.startswith('motivo:')) + c['piu di un motivo']
print('candidate di qualita alta: %d' % c['alta'])
print('candidate non-alta con il motivo dichiarato: %d (senza: %d)'
      % (dichiarate, c['senza motivo dichiarato']))
for k in sorted(k for k in c if k.startswith('motivo:')):
    print('   %-26s %d' % (k, c[k]))
print('   %-26s %d' % ('piu di un motivo', c['piu di un motivo']))
sol = c['motivo: data']
if dichiarate:
    print('\nmancano l\'alta **solo** per la data: %d su %d dichiarate (%.0f%%)'
          % (sol, dichiarate, 100 * sol / dichiarate))
if sol:
    print('di quelle, per novita:')
    for k, v in per_motivo_novita.most_common():
        print('   %-22s %3d  (%.0f%%)' % (k, v, 100 * v / sol))
print('\nlotti che hanno applicato l\'emendamento: %d' % len(lotti_con))
print('Le candidate senza motivo vengono dai lotti letti prima: non si contano nelle proporzioni.')
