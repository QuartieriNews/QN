# Per ogni evento: è rintracciabile direttamente alla fonte (sito dell'organizzatore o dell'evento) o esiste solo nell'aggregatore che usiamo?
import sys, re, collections, json
import openpyxl
from openpyxl.styles import Font
UNICO = sys.argv[1]
wb = openpyxl.load_workbook(UNICO)
SOCIAL = re.compile(r'(facebook\.com|instagram\.com|tiktok\.com|youtube\.com|youtu\.be|x\.com|twitter\.com|linkedin\.com|t\.me|wa\.me|whatsapp|threads\.net|telegram)', re.I)
TICKET = re.compile(r'(vivaticket|ticketone|ticketmaster|dice\.fm|eventbrite|boxol|ticketsms|clappit|liveticket|ciaotickets|xceed|mailticket|tickettailor|ticketnation|i-ticket|oooh\.events|tiqets|getyourguide|musement|coopculture|museiincomuneroma|biglietteria|tickets?\.)', re.I)
AGGR = re.compile(r'(romatoday|citynews|culture\.roma\.it|060608|comune\.roma\.it|google\.|goo\.gl|maps\.app|forms\.gle|jotform|linktr\.ee|bit\.ly)', re.I)
def classify(links):
    links = [l.strip() for l in links if l and l.strip().startswith('http')]
    own = [l for l in links if not SOCIAL.search(l) and not TICKET.search(l) and not AGGR.search(l)]
    tick = [l for l in links if TICKET.search(l)]; soc = [l for l in links if SOCIAL.search(l)]
    if own: return 'sito dell\'organizzatore o dell\'evento', own[0]
    if tick: return 'solo biglietteria', tick[0]
    if soc: return 'solo social', soc[0]
    return 'nessun riferimento esterno', None
res = {}  # url -> (classe, link)
# Facebook
t = wb['Facebook']; h = [c.value for c in t[1]]; g = lambda r, k: r[h.index(k)] if k in h else None
for r in t.iter_rows(min_row=2, values_only=True):
    links = [x for x in str(g(r, 'externalLinks') or '').split('; ')] + [g(r, 'ticketsInfo.buyUrl')] + [x for x in str(g(r, 'organizators.url') or '').split('; ')]
    res[g(r, 'url')] = classify(links)
# Comune
t = wb['Comune di Roma (culture)']; h = [c.value for c in t[1]]
for r in t.iter_rows(min_row=2, values_only=True):
    links = [x for k in ('contattiLinks', 'ingressoLinks', 'social') for x in str(g(r, k) or '').split(' | ')]
    res[g(r, 'url')] = classify(links)
# Romatoday
t = wb['Romatoday → sorgente']; h = [c.value for c in t[1]]
for r in t.iter_rows(min_row=2, values_only=True):
    links = [g(r, 'link_ufficiale'), g(r, 'link_biglietti'), g(r, 'link_facebook'), g(r, 'link_instagram')]
    sw = g(r, 'sito_web')
    if sw and '://' not in sw: links.append('https://' + sw)
    c = classify(links); res[g(r, 'url_romatoday')] = c
    if g(r, 'link_ufficiale'): res[g(r, 'link_ufficiale')] = c
# Eventi unificati
ws = wb['Eventi unificati']; h = [c.value for c in ws[1]]
for col in ('rintracciabile_alla_fonte', 'link_fonte_diretta'):
    if col not in h: ws.cell(1, len(h) + 1, col).font = Font(bold=True); h.append(col)
stats = collections.Counter()
for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
    f = r[h.index('fonte')].split(':')[0].split(' (')[0].replace(' → sorgente', '')
    if f == 'Fonte locale': c, l = 'letto alla fonte (sito del luogo)', r[h.index('url')]
    else: c, l = res.get(r[h.index('url')], ('nessun riferimento esterno', None))
    ws.cell(i, h.index('rintracciabile_alla_fonte') + 1, c); ws.cell(i, h.index('link_fonte_diretta') + 1, l); stats[(f, c)] += 1
tot = collections.defaultdict(collections.Counter)
for (f, c), v in stats.items(): tot[f][c] = v
wr = wb['Riepilogo']; wr.cell(1, 7, 'Rintracciabilità alla fonte').font = Font(bold=True); wr.column_dimensions['G'].width = 70
for row in wr.iter_rows(min_row=2, max_row=5):
    for f, c in tot.items():
        if str(row[0].value).startswith(f.split(' ')[0]) and (f != 'Fonte locale' or str(row[0].value).startswith('Fonti')):
            n = sum(c.values()); row[6].value = '; '.join(f'{k}: {v}' for k, v in c.most_common()) + f' (su {n})'
wb.save(UNICO)
for f, c in tot.items(): print(f, sum(c.values()), dict(c.most_common()))
