export const meta = {
  name: 'notizie-dai-dati-completo',
  description: 'Rilettura a ritroso di 14.779 post e notizie dei siti già raccolti: notizie di quartiere per gli altri blocchi, verificate e fuse',
  phases: [
    { title: 'Smistamento', detail: 'tutte le voci: utile sì/no, blocco, punteggio', model: 'sonnet' },
    { title: 'Scheda', detail: 'le utili: tema, luogo, origine, attualità, sintesi in parole nostre' },
    { title: 'Verifica', detail: 'le migliori riguardate da uno scettico' },
    { title: 'Fusione', detail: 'stesso fatto da fonti diverse: un gruppo per fatto' },
  ],
}

const BLOCCHI = ['notizia di quartiere', 'istituzionale', 'servizio o avviso utile', 'segnalazione o tema dei residenti',
  'solo evento', 'promozione o altro', 'non locale', 'rilancio di una testata']
const UTILI = BLOCCHI.slice(0, 4)
const TEMI = ['lavori e cantieri', 'mobilita e trasporti', 'rifiuti e decoro', 'sicurezza e emergenze', 'municipio e istituzioni',
  'servizi, bandi e scadenze', 'scuola', 'sanita e salute', 'attivismo e partecipazione', 'aperture e chiusure',
  'solidarieta e sociale', 'lutti e ricordi', 'premi e storie', 'ambiente e verde', 'casa e urbanistica', 'commercio e lavoro', 'altro']

const CONTESTO = `Contesto: Quartieri News (QN) è un sito iperlocale di Roma con 89 pagine di quartiere. Ogni pagina è fatta di blocchi:
Eventi (già coperto), Notizie di quartiere, Istituzionale (municipio, commissioni, consigli, delibere, assemblee pubbliche),
Servizi e avvisi utili (scadenze, bandi, sportelli, chiusure di uffici, campagne sanitarie con date e luoghi), Segnalazioni e temi
dei residenti (problemi sollevati da comitati e cittadini: degrado, sicurezza, traffico, verde, raccolte firme).
Le voci da valutare sono post Facebook e notizie dei siti di associazioni, comitati, parrocchie, scuole, enti e luoghi di Roma,
raccolti nei giorni scorsi per cercare eventi. Le testate giornalistiche sono escluse. Non cercare nulla sul web e non usare altri
strumenti: lavora solo sul file indicato, leggendolo con lo strumento Read (a più riprese con offset e limit se è lungo).
Il campo zona_sede è la sede della fonte, non per forza il luogo della notizia.
Una NOTIZIA è un fatto o un'informazione concreta che cambia o tocca la vita di chi abita in un luogo di Roma: un cantiere, una chiusura,
una riapertura, un nuovo servizio, una decisione del municipio, un problema segnalato con fatti, una raccolta firme, un'emergenza,
un traguardo di una realtà del quartiere, una scadenza utile. NON è notizia: la promozione di corsi o attività commerciali, la liturgia,
gli auguri, le campagne generiche senza luogo, le notizie nazionali o di altre città, il semplice annuncio di un evento (va nel blocco Eventi),
salvo che l'evento sia in sé un fatto per il quartiere (inaugurazione di uno spazio pubblico, riapertura di un parco, prima edizione rilevante).
Un post che si limita a rilanciare l'articolo di un giornale senza aggiungere fatti o posizioni proprie è un «rilancio di una testata».`

const RUBRICA = `Punteggio (0-5): 5 = fatto concreto e recente, con un luogo preciso, che tocca chi ci vive (chiusura di una strada, cantiere, nuovo servizio,
problema documentato, decisione del municipio); 4 = notizia locale chiara ma meno urgente o meno precisa; 3 = informazione utile o tema del quartiere
senza un fatto nuovo; 2 = debole o quasi promozionale; 1 = quasi nulla; 0 = niente.`

const A_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, utile: { type: 'boolean' }, blocco: { type: 'string', enum: BLOCCHI }, punteggio: { type: 'integer', minimum: 0, maximum: 5 } },
  required: ['id', 'utile', 'blocco', 'punteggio'] } } }, required: ['items'] }

const B_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, blocco: { type: 'string', enum: UTILI.concat(['scarta']) }, tema: { type: 'string', enum: TEMI },
  origine: { type: 'string', enum: ['fatto o posizione della fonte', 'rilancio di un ente pubblico', 'rilancio di una testata con aggiunte', 'altro'] },
  livello_geo: { type: 'string', enum: ['via o luogo preciso', 'quartiere', 'municipio', 'citta', 'non dichiarato'] },
  luogo: { type: 'string' }, attualita: { type: 'string', enum: ['fatto recente', 'avviso con scadenza', 'tema aperto o ricorrente', 'storia o ricordo'] },
  punteggio: { type: 'integer', minimum: 1, maximum: 5 }, sensibile: { type: 'boolean' }, motivo_sensibile: { type: 'string' }, sintesi: { type: 'string' } },
  required: ['id', 'blocco', 'tema', 'origine', 'livello_geo', 'luogo', 'attualita', 'punteggio', 'sensibile', 'motivo_sensibile', 'sintesi'] } } }, required: ['items'] }

const C_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, confermata: { type: 'boolean' }, motivo: { type: 'string' }, blocco_finale: { type: 'string', enum: UTILI.concat(['scarta']) },
  punteggio_finale: { type: 'integer', minimum: 0, maximum: 5 }, sintesi_finale: { type: 'string' } },
  required: ['id', 'confermata', 'motivo', 'blocco_finale', 'punteggio_finale', 'sintesi_finale'] } } }, required: ['items'] }

const D_SCHEMA = { type: 'object', properties: { gruppi: { type: 'array', items: { type: 'object', properties: {
  ids: { type: 'array', items: { type: 'string' } }, rappresentante: { type: 'string' }, fatto: { type: 'string' } },
  required: ['ids', 'rappresentante', 'fatto'] } } }, required: ['gruppi'] }

const chunk = (a, n) => { const out = []; for (let i = 0; i < a.length; i += n) out.push(a.slice(i, i + n)); return out }
const lotti = args
const tot = { voci: 0, smistati: 0, recuperati: 0, utili: 0, schede: 0, verificate: 0, confermate: 0 }
const confermate = []

const smista = (lotto, gia) => agent(`${CONTESTO}

${RUBRICA}

Leggi il file ${lotto.path} (JSONL, ${lotto.n} voci; leggilo TUTTO, a più riprese con offset e limit). ${gia ? `Queste voci sono già state classificate e vanno saltate: ${gia.join(', ')}. Classifica tutte le ALTRE.` : `Classifica OGNI voce.`}
Per ogni voce restituisci id, utile (true se è una notizia o un'informazione utile per uno dei blocchi Notizie, Istituzionale, Servizi e avvisi,
Segnalazioni dei residenti, con punteggio almeno 3), blocco e punteggio.${gia ? '' : ` Devono esserci esattamente ${lotto.n} risultati, uno per id.`}`,
  { label: `smistamento ${lotto.nome}${gia ? ' (recupero)' : ''}`, phase: 'Smistamento', schema: A_SCHEMA, model: 'sonnet', effort: 'low' })

const res = await pipeline(lotti,
  async (lotto) => {
    tot.voci += lotto.n
    const a = await smista(lotto, null)
    let items = a ? a.items : []
    const visti = new Set(items.map(x => x.id))
    if (visti.size < lotto.n) {   // copertura: le voci mancanti tornano a un secondo lettore
      const b = await smista(lotto, [...visti])
      const extra = (b ? b.items : []).filter(x => !visti.has(x.id))
      tot.recuperati += extra.length
      items = items.concat(extra)
      if (visti.size + extra.length < lotto.n) log(`${lotto.nome}: ${lotto.n - visti.size - extra.length} voci non classificate dopo il recupero`)
    }
    tot.smistati += items.length
    return items
  },
  async (items, lotto) => {
    const ok = items.filter(x => x.utile && x.punteggio >= 3 && UTILI.includes(x.blocco)).map(x => x.id)
    tot.utili += ok.length
    if (!ok.length) return []
    const parti = await parallel(chunk(ok, 60).map((ids, j) => () => agent(`${CONTESTO}

${RUBRICA}

Leggi il file ${lotto.path} e considera SOLO le voci con questi id: ${ids.join(', ')}.
Per ognuna compila la scheda:
- blocco (o "scarta" se a una lettura attenta non è una notizia utile o è un semplice rilancio di un giornale);
- tema; origine (fatto o posizione della fonte stessa; rilancio di un comunicato di un ente pubblico; rilancio di una testata con aggiunte proprie; altro);
- livello_geo e luogo (il luogo del fatto: via, piazza, parco, scuola, ufficio, quartiere; stringa vuota se non c'è);
- attualita; punteggio con la rubrica;
- sensibile=true se tocca minori, salute di persone identificabili, vittime di reati, persone decedute o privati cittadini nominati, con il motivo;
- sintesi: una frase di al massimo 30 parole, scritta con parole tue (mai frasi copiate dal testo, niente virgolette), senza nomi di privati cittadini,
  senza numeri di telefono né email; nomi di enti, associazioni, luoghi e cariche pubbliche sono ammessi.
Restituisci una scheda per ogni id indicato.`, { label: `scheda ${lotto.nome}.${j}`, phase: 'Scheda', schema: B_SCHEMA, effort: 'medium' })))
    const schede = parti.filter(Boolean).flatMap(p => p.items)
    tot.schede += schede.length
    return schede
  },
  async (schede, lotto) => {
    const top = schede.filter(s => s.blocco !== 'scarta' && s.punteggio >= 4)
    if (!top.length) return { lotto: lotto.nome, schede: schede.length, verificate: 0 }
    const parti = await parallel(chunk(top, 40).map((grp, j) => () => agent(`${CONTESTO}

Sei uno scettico. Un primo lettore ha giudicato queste voci notizie di quartiere di buon livello. Il tuo compito è smontarle quando non reggono.
Leggi il file ${lotto.path} e, per ogni scheda qui sotto, rileggi il testo originale della voce con lo stesso id e decidi:
- confermata=false se è in realtà promozione, un semplice annuncio di evento, un rilancio di un giornale senza fatti propri, una notizia non locale
  o nazionale, un fatto già superato alla data della voce, o se la scheda travisa il testo; in dubbio, confermata=false;
- blocco_finale e punteggio_finale corretti secondo la rubrica;
- sintesi_finale: fedele al testo e scritta con parole proprie, al massimo 30 parole, senza nomi di privati, telefoni o email
  (riscrivila se la sintesi del primo lettore copia frasi del testo o aggiunge fatti che il testo non dice);
- motivo: una riga.

${RUBRICA}

Schede da verificare:
${JSON.stringify(grp)}`, { label: `verifica ${lotto.nome}.${j}`, phase: 'Verifica', schema: C_SCHEMA, effort: 'high' })))
    const ver = parti.filter(Boolean).flatMap(p => p.items)
    tot.verificate += ver.length
    const byId = new Map(top.map(s => [s.id, s]))
    for (const v of ver.filter(v => v.confermata)) {
      const s = byId.get(v.id) || {}
      confermate.push({ id: v.id, tema: s.tema, luogo: s.luogo, sintesi: v.sintesi_finale, lotto: lotto.nome })
    }
    tot.confermate = confermate.length
    log(`${lotto.nome}: ${schede.length} schede, ${ver.filter(v => v.confermata).length}/${ver.length} confermate`)
    return { lotto: lotto.nome, schede: schede.length, verificate: ver.length }
  })

// fusione: lo stesso fatto letto da fonti diverse (serve l'insieme intero delle confermate)
phase('Fusione')
const perTema = {}
for (const c of confermate) (perTema[c.tema] = perTema[c.tema] || []).push(c)
const fusi = await parallel(Object.entries(perTema).filter(([, v]) => v.length > 1).flatMap(([tema, v]) => chunk(v, 120).map((grp, j) => () =>
  agent(`Queste sono notizie di quartiere di Roma confermate, tutte del tema «${tema}», ognuna con id, luogo e una sintesi.
Raggruppa le voci che parlano dello STESSO fatto (stesso avvenimento o stesso avviso, anche da fonti diverse o in giorni vicini).
Restituisci SOLO i gruppi con almeno due voci: ids, il rappresentante (la voce più completa) e il fatto in una riga con parole tue.
Voci diverse che trattano lo stesso tema generale ma fatti distinti NON vanno raggruppate. Non usare strumenti.

${JSON.stringify(grp.map(c => ({ id: c.id, luogo: c.luogo, sintesi: c.sintesi })))}`, { label: `fusione ${tema}${j ? '.' + j : ''}`, phase: 'Fusione', schema: D_SCHEMA, effort: 'medium' }))))
const gruppi = fusi.filter(Boolean).flatMap(f => f.gruppi)
return { ...tot, lotti_ok: res.filter(Boolean).length, lotti_persi: lotti.length - res.filter(Boolean).length, gruppi_di_doppioni: gruppi.length,
  voci_in_gruppi: gruppi.reduce((n, g) => n + g.ids.length, 0) }