export const meta = {
  name: 'qualita-eventi',
  description: 'Controllo di qualità di 155 eventi della pagina, confrontati con la fonte; doppio revisore su un evento su quattro',
  phases: [
    { title: 'Audit', detail: 'ogni evento confrontato con il testo della fonte' },
    { title: 'Secondo revisore', detail: 'un evento su quattro rivisto in modo indipendente' },
  ],
}
const SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' },
  data: { type: 'string', enum: ['giusta', 'sbagliata', 'non verificabile'] },
  ora: { type: 'string', enum: ['giusta', 'sbagliata', 'mancante ma nella fonte', 'assente anche nella fonte', 'non verificabile'] },
  luogo: { type: 'string', enum: ['giusto', 'sbagliato', 'mancante ma nella fonte', 'assente anche nella fonte', 'non verificabile'] },
  pagina_qn: { type: 'string', enum: ['coerente', 'incoerente', 'senza pagina', 'non verificabile'] },
  titolo: { type: 'string', enum: ['nome dell evento', 'frase presa dal testo', 'generico o troncato'] },
  natura: { type: 'string', enum: ['evento', 'corso o attivita ricorrente', 'non e un evento'] },
  stato: { type: 'string', enum: ['valido', 'gia passato alla data di riferimento', 'annullato o rinviato', 'non verificabile'] },
  fuori_roma_o_online: { type: 'boolean' },
  errore_grave: { type: 'boolean' },
  nota: { type: 'string' } },
  required: ['id', 'data', 'ora', 'luogo', 'pagina_qn', 'titolo', 'natura', 'stato', 'fuori_roma_o_online', 'errore_grave', 'nota'] } } }, required: ['items'] }

const ISTR = (path, ids) => `Controllo di qualità della pagina «Eventi dei quartieri» di Quartieri News (Roma, 89 pagine di quartiere). Data di riferimento: 26 ottobre 2026.
Leggi il file ${path} con lo strumento Read (JSONL). Ogni riga è un evento pubblicato (titolo, inizio, fine, ora, luogo, indirizzo, organizzatore,
pagina_qn, municipio, link) con il testo della sua fonte (fonte_testo; fonte_come dice da dove viene). Non cercare nulla sul web e non usare altri strumenti.
Per ognuno degli eventi con id ${ids.join(', ')} confronta la riga con la fonte e giudica:
- data: la data di inizio coincide con quella della fonte? (per un periodo, l'inizio del periodo);
- ora, luogo: giusti, sbagliati, mancanti ma presenti nella fonte, o assenti anche nella fonte;
- pagina_qn: il quartiere QN indicato è coerente con il luogo dell'evento a Roma (usa la tua conoscenza della città; «senza pagina» se manca);
- titolo: è il nome dell'evento, oppure una frase presa dal testo (un invito, l'inizio di un post, una data), oppure generico o troncato;
- natura: un evento puntuale, un corso o attività ricorrente, o non è un evento;
- stato: valido, già passato alla data di riferimento, annullato o rinviato secondo la fonte;
- fuori_roma_o_online: true se si svolge fuori dal Comune di Roma o solo online;
- errore_grave: true se data sbagliata, evento passato o annullato, non è un evento, fuori Roma o online, o pagina QN incoerente;
- nota: una riga in parole tue, senza copiare il testo della fonte.
Se la fonte manca o non basta, scrivi «non verificabile» dove serve e giudica solo ciò che si vede nella riga.`

const res = await pipeline(args,
  (l) => agent(ISTR(l.path, l.ids), { label: `audit ${l.nome}`, phase: 'Audit', schema: SCHEMA, effort: 'high' }),
  async (a, l) => {
    const doppi = l.ids.filter((_, i) => i % 4 === 0)
    const b = await agent(ISTR(l.path, doppi) + '\nSei un secondo revisore indipendente: giudica senza presumere che la pagina sia giusta.',
      { label: `secondo revisore ${l.nome}`, phase: 'Secondo revisore', schema: SCHEMA, effort: 'high' })
    return { lotto: l.nome, n: a ? a.items.length : 0, doppi: b ? b.items.length : 0 }
  })
return { lotti: res.filter(Boolean).length, eventi: res.filter(Boolean).reduce((s, r) => s + r.n, 0), doppi: res.filter(Boolean).reduce((s, r) => s + r.doppi, 0) }
