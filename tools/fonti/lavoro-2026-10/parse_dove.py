import re
VIE = r'(?:Via|Viale|Vle|Piazza|Piazzale|P\.za|Largo|Corso|Lungotevere|Vicolo|Borgo|Circonvallazione|Passeggiata|Salita|Scalo|Strada|Lungomare|Rampa|Clivo|Vialetto|Piazzetta)'
COMUNI = {'Capena','Nemi','Frascati','Velletri','Genzano','Bellegra','Tuscania','Fiumicino','Ostia','Tivoli','Marino','Albano','Ariccia','Castel Gandolfo','Grottaferrata','Monterotondo','Mentana','Ladispoli','Cerveteri','Bracciano','Anguillara','Ciampino','Pomezia','Ardea','Anzio','Nettuno','Subiaco','Palestrina','Zagarolo','Colonna','Rocca di Papa','Rocca Priora','Castelnuovo di Porto','Monteflavio','Camerata Nuova','Fiano Romano','Formello','Sacrofano','Riano','Guidonia','Tivoli','Cave','Olevano','Vallerano','Civita Castellana','Viterbo','Latina','Sabaudia','Terracina','Gaeta','Rieti','Vicovaro','Mazzano','Trevignano','Manziana','Santa Marinella','Civitavecchia','Lanuvio','Lariano','Artena','Valmontone','Segni','Anagni','Fiuggi','Montelibretti','Nerola','Montorio Romano','Poggio Mirteto','Magliano','Roma'}
def clean_street(s):
    s = re.sub(r'\(.*?\)', ' ', s); s = re.sub(r'\b(Vle)\b', 'Viale', s); s = re.sub(r'\bP\.za\b', 'Piazza', s)
    s = re.sub(r'\b(?:\d{5})?\s*Roma\b.*$', '', s); s = re.sub(r'\bRM\b.*$', '', s); s = re.sub(r',?\s*Italia\b.*$', '', s)
    s = re.sub(r'\s+(e|ed|/)\s+' + VIE + r'.*$', '', s)          # due indirizzi: tieni il primo
    s = re.sub(r"\bSan ([AEIOUaeiou])", r"Sant'\1", s); s = re.sub(r"\bSanta ([AEIOUaeiou])", r"Sant'\1", s)
    return re.sub(r'\s+', ' ', s).strip(' ,-')
def parse_dove(s):
    """Ritorna (via con civico, comune, nome del luogo) dalla scheda 'Dove' di Romatoday."""
    s = re.sub(r'\s+', ' ', s or '').replace('Indirizzo non disponibile', ' ').strip()
    m = re.search(r'\b(' + VIE + r'\s+.+)$', s)
    if not m: return None, None, s
    rest = m.group(1); venue = s[:m.start()].strip(' ,-')
    town = 'Roma'
    for c in sorted(COMUNI, key=len, reverse=True):
        if re.search(r'(,\s*\d+[/A-Za-z]*(?:\s*[A-Za-z])?|\b)\s+' + re.escape(c) + r'\s*$', rest) and c != 'Roma':
            town = c; rest = rest[:rest.rfind(c)].strip(' ,'); break
    rest = re.sub(r'\s+Roma\s*$', '', rest)
    street = clean_street(rest)
    m2 = re.match(r'^(' + VIE + r'\s+[^,]+?)(?:,\s*(\d+[/A-Za-z]*(?:\s*[A-Za-z])?))?\s*$', street)
    if m2: street = m2.group(1) + (', ' + m2.group(2) if m2.group(2) else '')
    return street, town, venue
if __name__ == '__main__':
    for t in ["Galleria L'Attico Via del Paradiso, 41", 'Piazza del Campidoglio', 'Via Irina Alberti', 'Largo Dino Frisullo', 'Piazza di San Egidio, 1b', 'Parco del Colle Oppio e delle terme di Traiano, Vle del Monte Oppio, 00184 Roma RM, Italia', 'Viale Fiorello La Guardia, 6 e Viale dell’Aranciera, 4', 'Art Forum Würth Capena Viale della Buona Fortuna, 2 Capena', 'Lungotevere in Augusta (angolo via Tomacelli)', 'Tor Bella Monaca Indirizzo non disponibile', 'Via Badia di Cava, Roma, RM, Italia', 'Piazza Vittorio Veneto, 10 Castelnuovo di Porto']:
        print(t, '->', parse_dove(t))
