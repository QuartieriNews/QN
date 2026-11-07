# Is this response the page we asked for? Shared by report1/fetch_items.py and report1/retry_c1.py
# so the rule lives in one place: two copies of a validation rule drift apart.
#
# Written after both Cronaca sources answered 200 to every request and served no article - the
# Questura an "Accesso negato" block page, the Carabinieri their listing shell. Validating on
# status code and byte size accepted 99 empty pages as a corpus, and only a reader noticed.
import re

BLOCCHI = ('accesso negato', 'access denied', 'richiesta bloccata', 'are you a robot', 'captcha')
TITOLI_GENERICI = ('comunicati stampa', '404', 'not found', 'errore')

def rifiuto(body):
    """Why this response is not the requested article, or '' when it looks like one."""
    low = body[:4000].lower()
    for b in BLOCCHI:
        if b in low: return b
    m = re.search(r'<title>([^<]*)', body, re.I)
    tit = (m.group(1).strip() if m else '')
    if tit and tit.lower() in TITOLI_GENERICI: return f'titolo generico: {tit}'
    if len(re.sub(r'<[^>]+>', ' ', body)) < 400: return 'corpo troppo corto'
    return ''
