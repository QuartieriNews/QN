export const meta = {
  name: 'timeline-quartieri',
  description: 'Ottobre 2026, 9.643 post e notizie dei siti (anche corti): quante brevi da timeline per quartiere, con verifica a campione e doppioni',
  phases: [
    { title: 'Smistamento', detail: 'ogni voce: breve da timeline sì/no, tipo, portata, luogo, validità, titolo', model: 'sonnet' },
    { title: 'Verifica', detail: 'campione delle brevi riguardato da uno scettico' },
    { title: 'Doppioni', detail: 'stesso fatto da fonti diverse', model: 'sonnet' },
  ],
}

const TIPI = ['mini notizia', 'avviso utile', 'dichiarazione politica', 'segnalazione dei residenti', 'evento di oggi o domani', 'altro']
const PORTATA = ['quartiere', 'municipio', 'citta', 'fuori Roma o nazionale']
const CONTESTO = `Contesto: Quartieri News (QN) è un sito iperlocale di Roma con 89 pagine di quartiere. Si valuta una TIMELINE di brevi, come la striscia
«Intanto» del Post: nella pagina del quartiere compaiono i titoli; cliccando si apre una timeline verticale dove ogni voce ha un titolo e una breve
di 2-4 frasi con i dettagli (che cosa, dove, quando, chi). Una voce è una BREVE DA TIMELINE se, da sola, dà abbastanza per quel titolo e quella breve
ed è utile o interessante per chi vive in un quartiere, in un municipio o in città, e attuale (pubblicabile entro 48 ore dalla data della voce).
Tipi: mini notizia (un fatto avvenuto o deciso); avviso utile (chiusure, scadenze, servizi, sanità, trasporti, lavori); dichiarazione politica
(presa di posizione di eletti, assessori, partiti o comitati su un tema locale); segnalazione dei residenti (un problema denunciato con fatti);
evento di oggi o domani (solo se merita una breve: una manifestazione, un'inaugurazione, un grande evento; non corsi, non attività ricorrenti); altro.
NON è una breve: promozione commerciale, corsi, liturgia, auguri, campagne generiche senza luogo né data, notizie nazionali o estere,
il rilancio di un articolo di giornale senza fatti propri, un testo troppo vago per scriverne due frasi.
Le voci sono post Facebook e notizie dei siti di associazioni, comitati, parrocchie, scuole, enti, municipi ed eletti di Roma, già raccolti.
Non cercare nulla sul web e non usare altri strumenti: lavora solo sul file indicato, leggendolo con Read (a più riprese con offset e limit).
Il campo zona_sede è la sede della fonte, non per forza il luogo del fatto.`

const A_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, ok: { type: 'boolean' }, tipo: { type: 'string', enum: TIPI }, portata: { type: 'string', enum: PORTATA },
  luogo: { type: 'string' }, validita: { type: 'string', enum: ['poche ore', '1-3 giorni', 'piu giorni'] }, titolo: { type: 'string' } },
  required: ['id', 'ok', 'tipo', 'portata', 'luogo', 'validita', 'titolo'] } } }, required: ['items'] }
const V_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, confermata: { type: 'boolean' }, tipo: { type: 'string', enum: TIPI }, portata: { type: 'string', enum: PORTATA }, motivo: { type: 'string' } },
  required: ['id', 'confermata', 'tipo', 'portata', 'motivo'] } } }, required: ['items'] }
const D_SCHEMA = { type: 'object', properties: { gruppi: { type: 'array', items: { type: 'object', properties: {
  ids: { type: 'array', items: { type: 'string' } } }, required: ['ids'] } } }, required: ['gruppi'] }

const chunk = (a, n) => { const out = []; for (let i = 0; i < a.length; i += n) out.push(a.slice(i, i + n)); return out }
const tot = { voci: 0, classificate: 0, recuperate: 0, brevi: 0, campione: 0, confermate: 0 }
const brevi = []

const smista = (lotto, gia) => agent(`${CONTESTO}

Leggi il file ${lotto.path} (JSONL, ${lotto.n} voci; leggilo TUTTO). ${gia ? `Queste voci sono già classificate e vanno saltate: ${gia.join(', ')}. Classifica tutte le ALTRE.` : 'Classifica OGNI voce.'}
Per ogni voce: id; ok (true se è una breve da timeline); tipo; portata (quartiere se riguarda un luogo o un quartiere preciso, municipio, città,
oppure fuori Roma o nazionale); luogo (il luogo del fatto: via, piazza, parco, scuola, quartiere; stringa vuota se non c'è); validita;
titolo: solo se ok, al massimo 12 parole, scritto con parole tue (mai copiato dal testo, niente virgolette, niente nomi di privati cittadini); stringa vuota se non ok.${gia ? '' : ` Devono esserci esattamente ${lotto.n} risultati.`}`,
  { label: `smistamento ${lotto.nome}${gia ? ' (recupero)' : ''}`, phase: 'Smistamento', schema: A_SCHEMA, model: 'sonnet', effort: 'low' })

await pipeline(args,
  async (lotto) => {
    tot.voci += lotto.n
    const a = await smista(lotto, null)
    let items = a ? a.items : []
    const visti = new Set(items.map(x => x.id))
    if (visti.size < lotto.n) {
      const b = await smista(lotto, [...visti])
      const extra = (b ? b.items : []).filter(x => !visti.has(x.id))
      tot.recuperate += extra.length; items = items.concat(extra)
      if (visti.size + extra.length < lotto.n) log(`${lotto.nome}: ${lotto.n - visti.size - extra.length} voci non classificate`)
    }
    tot.classificate += items.length
    const ok = items.filter(x => x.ok && x.portata !== 'fuori Roma o nazionale')
    tot.brevi += ok.length
    for (const x of ok) brevi.push({ id: x.id, tipo: x.tipo, portata: x.portata, luogo: x.luogo, titolo: x.titolo, lotto: lotto.nome })
    return ok
  },
  async (ok, lotto) => {
    if (!ok.length) return null
    const passo = Math.max(1, Math.floor(ok.length / 12))
    const camp = ok.filter((_, i) => i % passo === 0).slice(0, 12)   // campione regolare, fino a 12 per lotto
    const v = await agent(`${CONTESTO}

Sei uno scettico. Un primo lettore ha giudicato queste voci brevi da timeline. Leggi il file ${lotto.path}, rileggi il testo originale di ogni voce
con lo stesso id e decidi: confermata=false se non regge (promozione, corso, evento ricorrente, testo troppo vago per due frasi, rilancio di un giornale,
notizia non romana, fatto non attuale alla data della voce); in dubbio, false. Correggi tipo e portata se serve. Motivo in una riga.

Voci:
${JSON.stringify(camp)}`, { label: `verifica ${lotto.nome}`, phase: 'Verifica', schema: V_SCHEMA, effort: 'high' })
    const it = v ? v.items : []
    tot.campione += it.length; tot.confermate += it.filter(x => x.confermata).length
    return it
  })

phase('Doppioni')
const perPortata = {}
for (const b of brevi) (perPortata[b.portata] = perPortata[b.portata] || []).push(b)
const gruppi = (await parallel(Object.entries(perPortata).flatMap(([p, v]) => chunk(v, 250).map((grp, j) => () =>
  agent(`Questi sono titoli di brevi su Roma (portata: ${p}), con id e luogo. Raggruppa SOLO i titoli che parlano dello STESSO fatto o dello stesso avviso
(stesso avvenimento, anche da fonti diverse o in giorni vicini). Restituisci solo i gruppi con almeno due id. Non usare strumenti.

${JSON.stringify(grp.map(b => ({ id: b.id, luogo: b.luogo, titolo: b.titolo })))}`, { label: `doppioni ${p}${j ? '.' + j : ''}`, phase: 'Doppioni', schema: D_SCHEMA, model: 'sonnet', effort: 'low' }))))).filter(Boolean).flatMap(g => g.gruppi)
return { ...tot, gruppi_doppioni: gruppi.length, voci_in_gruppi: gruppi.reduce((n, g) => n + g.ids.length, 0) }