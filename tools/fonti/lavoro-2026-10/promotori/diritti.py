# Posizione di una fonte sulla diffusione dei suoi contenuti, dai frammenti letti sul sito (note legali, termini, piè di pagina),
# dal robots.txt e dalla riserva TDM; più i casi documentati a mano (piattaforme, licenze, Roma Capitale).
import re
RESTR=re.compile(r"vietat[ao]\s+(la\s+|ogni\s+|qualsiasi\s+|qualunque\s+)?(riproduzion|copia|diffusion|pubblicazion|utilizz|duplicazion)|riproduzione\s+(anche\s+parziale\s+|totale\s+e/?o\s+parziale\s+)?(è\s+)?(vietata|riservata|non\s+consentita|proibita)|"
                 r"non\s+(è|e')\s+(consentit[ao]|permess[ao])\s+(la\s+)?(riproduzion|copia|copiare|diffusion|pubblicazion|utilizz)|non\s+(è|e')\s+consentito\s+copiare|divieto\s+di\s+(riproduzion|copia|diffusion)|"
                 r"(previo|preventivo|previa|preventiva)\s+(consenso|autorizzazione)|autorizzazione\s+scritta|non\s+si\s+acconsente|may\s+not\s+be\s+(reproduced|copied|republished)|"
                 r"(reproduction|copying)\s+(is\s+)?(prohibited|forbidden|not\s+permitted)|expressly\s+prohibited\s+from\s+(using|copying)",re.I)
SCRAPE=re.compile(r"(scraping|crawl\w*|robot\w*|spider\w*|estrazione\s+(automatica|sistematica)|text\s+and\s+data\s+mining|\bTDM\b|data\s+mining)",re.I)
SCRAPE_NEG=re.compile(r"vietat|non\s+(è|e')\s+(consentit|necessari|permess)|proibit|riserv|divieto|prohibit|not\s+permitted|opt.?out|esplicitamente",re.I)
OPEN=re.compile(r"creative\s*commons|\bCC[\s-]?(BY|0)\b|copyleft|IODL|liberamente\s+(utilizzabil|riproducibil)|riutilizzo\s+(dei\s+contenuti\s+)?(è\s+)?(consentito|libero)|licenza\s+CC\b",re.I)
GENERIC=re.compile(r"tutti\s+i\s+diritti\s+(sono\s+)?riservati|all\s+rights?\s+reserved|©|&copy;|copyright|i\s+diritti\s+sui\s+contenuti",re.I)
MANUALE={   # casi documentati: host -> (posizione, prova, motivo)
 'facebook.com':('termini della piattaforma','https://www.facebook.com/legal/automated_data_collection_terms','Termini di Meta sulla raccolta automatica di dati: vietata senza permesso scritto; i contenuti delle pagine restano dei titolari'),
 'instagram.com':('termini della piattaforma','https://help.instagram.com/581066165581870','Termini d\'uso di Instagram (Meta): vietata la raccolta automatica senza permesso'),
 'romatoday.it':('licenza richiesta','https://www.romatoday.it','Citynews: lettura regolare solo con licenza (DEC-026)'),
 'culture.roma.it':('diritti riservati (generico)','https://www.comune.roma.it/web/it/note-legali.page','Note legali di Roma Capitale: i diritti sui contenuti appartengono a Roma Capitale; materiale di terzi coperto dai diritti di chi lo ha fornito; nessuna licenza di riuso dichiarata'),
 'comune.roma.it':('diritti riservati (generico)','https://www.comune.roma.it/web/it/note-legali.page','Note legali di Roma Capitale (come sopra)'),
 'bibliotechediroma.it':('nessuna indicazione','https://www.bibliotechediroma.it/opac/news/x/39537','Istituzione Biblioteche di Roma Capitale: il «Copyright» del sito riguarda solo il software del catalogo (Sebina NEXT, Dot Beyond); nessuna clausola sui contenuti delle news; nessun robots.txt'),
 'threads.com':('termini della piattaforma','https://help.instagram.com/581066165581870','Threads usa l\'account Instagram: valgono i termini d\'uso di Instagram (Meta), raccolta automatica vietata senza permesso'),
 'threads.net':('termini della piattaforma','https://help.instagram.com/581066165581870','Threads usa l\'account Instagram: valgono i termini d\'uso di Instagram (Meta), raccolta automatica vietata senza permesso'),
 'feverup.com':('termini della piattaforma','https://feverup.com/legal/terms','Biglietteria commerciale: contenuti promozionali propri (DEC-101: asset commerciali esclusi)'),
}
def snippets(sr):
    out=[]
    for k,lst in (sr.get('clausole') or {}).items():
        for ev in lst: out.append((ev.get('dove') or '',ev.get('testo') or ''))
    return out
def position(sr):
    """-> (posizione, url di prova, frammento o motivo)"""
    if not sr: return None,None,None
    h=sr.get('host','').replace('www.','')
    for k,v in MANUALE.items():
        if h==k or h.endswith('.'+k): return v
    if sr.get('esito')=='robots.txt vieta la lettura': return 'raccolta automatica vietata',f"https://{sr['host']}/robots.txt",'robots.txt vieta la lettura del sito a ogni agente'
    if sr.get('esito')!='letto': return 'non verificabile',None,sr.get('esito')
    sn=snippets(sr)
    def where(d): return d.split(': ',1)[-1] if d.startswith('note legali') else f"https://{sr['host']}/"
    for d,t in sn:
        if RESTR.search(t): return 'riproduzione vietata',where(d),t
    for d,t in sn:
        if SCRAPE.search(t) and SCRAPE_NEG.search(t): return 'raccolta automatica vietata',where(d),t
    if sr.get('vieta_tutto'): return 'raccolta automatica vietata',f"https://{sr['host']}/robots.txt",'robots.txt vieta la lettura del sito'
    if sr.get('tdm_meta')=='1' or sr.get('tdmrep'): return 'raccolta automatica vietata',f"https://{sr['host']}/",'riserva di estrazione TDM dichiarata'
    for d,t in sn:
        if OPEN.search(t): return 'licenza aperta',where(d),t
    for d,t in sn:
        if GENERIC.search(t): return 'diritti riservati (generico)',where(d),t
    return 'nessuna indicazione',f"https://{sr['host']}/",None
