# I numeri del rapporto invecchiano a ogni lotto che rientra, e finora li ho aggiornati a mano,
# cercandoli a occhio. Oggi ne ho trovati quattro vecchi in un colpo solo, dopo averli gia'
# "rinfrescati" due volte. Questo programma li ricalcola dal database e dice quali non tornano.
# Non corregge: dire a un programma di riscrivere il rapporto e' il modo di perdere il controllo di
# che cosa afferma. Stampa le differenze, e le sistemo io.
import csv, json, os, re, collections

NET = os.environ['QN_NET']
RAPPORTO = '/home/user/QN/docs/sources/RICOSTRUZIONE_2026-06_REPORT2.md'
PARLATO = {'A3', 'A4'}

righe = list(csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
doc = list(csv.DictReader(open(NET + '/report1/db/documenti.csv', encoding='utf-8')))
testo = open(RAPPORTO, encoding='utf-8').read()

def classe(v):
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

parl = [r for r in righe if r['fonte'] in PARLATO]
c = collections.Counter(classe(r['gemelli_scritti']) for r in parl)
S, U, D = c['S'], c['U'], c['D']; T = S + U + D
attiF = [d for d in doc if d['fonte'] == 'A2' and d.get('settimana') != '0']
cand_attiF = {r['documento_id'] for r in righe if r['fonte'] == 'A2' and r['documento_id'] in {d['id'] for d in attiF}}

qual = collections.Counter()
for f in sorted(os.listdir(NET + '/report2/out_video')):
    j = json.load(open(NET + '/report2/out_video/' + f, encoding='utf-8'))
    for x in j.get('notizie_candidate', []):
        qual[(x.get('novita_rispetto_agli_atti'), x.get('qualita'))] += 1
def quota_alta(n):
    tot = sum(v for k, v in qual.items() if k[0] == n)
    return 100 * qual[(n, 'alta')] / tot if tot else 0

# (etichetta, valore calcolato, formato, quante volte deve comparire almeno)
ATTESI = [
    ('candidate dal parlato',            len(parl),            '{:d}'),
    ('atti della finestra',              len(attiF),           '{:d}'),
    ('candidate dagli atti in finestra', len(cand_attiF),      '{:d}'),
    ('registrazioni lette',              len([d for d in doc if d['fonte'] in PARLATO]), '{:d}'),
    ('integrazioni al Report 1',         sum(1 for r in righe if r['integra_gemello_id']), '{:d}'),
    ('limite inferiore di novita',       100 * S / T,          '{:.1f}'),
    ('limite superiore di novita',       100 * (S + U) / T,    '{:.1f}'),
    ('quota alta, anche negli atti',     quota_alta('anche negli atti'), '{:.1f}'),
    ('quota alta, solo dal parlato',     quota_alta('solo dal parlato'), '{:.1f}'),
]

print('numeri correnti, e se il rapporto li contiene:\n')
mancanti = 0
for etichetta, valore, fmt in ATTESI:
    s = fmt.format(valore)
    if '.' in s: forme = [s.replace('.', ','), s.replace('.', ',') + '%']
    else: forme = [s, '{:,}'.format(int(valore)).replace(',', '.')]
    dentro = any(f in testo for f in forme)
    if not dentro: mancanti += 1
    print('  %-34s %-10s %s' % (etichetta, s, 'presente' if dentro else '*** NON COMPARE NEL RAPPORTO'))
print()
print('S=%d U=%d D=%d su %d' % (S, U, D, T))
if mancanti:
    print('\n%d valori non compaiono: o il rapporto e\' vecchio, o quel numero non lo cita.' % mancanti)
    print('Il programma non lo sa distinguere: guarda tu, e correggi a mano.')
