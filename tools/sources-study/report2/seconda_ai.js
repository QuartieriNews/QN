#!/usr/bin/env node
// Prova T4 del metodo: una seconda AI, di un'altra famiglia, rivede candidate gia' classificate da
// Claude Opus 5 e dice se e' d'accordo. Serve a misurare quanto il giudizio dipenda dal modello.
//
// Che cosa le si manda, e perche' proprio quello. Per le candidate che vengono dalle registrazioni
// le si manda **anche il tratto di trascrizione** attorno al marcatore citato: quell'audio e' gia'
// stato mandato alla stessa API per essere trascritto, quindi il materiale non esce da dove era
// gia' uscito. Per le candidate che vengono dagli atti si manda la sola riga anonimizzata: i testi
// degli atti alla API non sono mai stati mandati, e alcuni contengono dati personali che lo studio
// ha gia' documentato. L'asimmetria e' voluta e va dichiarata nel rapporto.
// La chiave non si stampa e non si registra da nessuna parte.
'use strict';
const fs = require('fs');
const MODEL = 'gpt-5.3-codex';
const ENDPOINT = 'https://api.openai.com/v1/responses';

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i === -1 ? d : process.argv[i + 1]; };
const casi = JSON.parse(fs.readFileSync(arg('input'), 'utf8'));
const out = arg('out');
const dryRun = process.argv.includes('--dry-run');
// Limiti chiusi (AGENTS.md, costo): oltre la soglia ci si ferma, non si spende.
const MAX_CASI = Number(arg('max-casi', 60));
const MAX_EVIDENZA = Number(arg('max-evidenza', 6000));      // caratteri per caso
const MAX_INPUT = Number(arg('max-input', 400000));          // caratteri in tutto
const MAX_OUTPUT_TOKENS = Number(arg('max-output-tokens', 4000));
if (casi.length > MAX_CASI) {
  console.error(`${casi.length} casi: oltre il tetto di ${MAX_CASI} per chiamata (--max-casi). Dividi l'input.`);
  process.exit(2);
}

if (!dryRun && !process.env.OPENAI_API_KEY) {
  console.error('OPENAI_API_KEY non impostata: mi rifiuto di chiamare, perche\' una chiave mancante non deve somigliare a una verifica che non ha trovato nulla');
  process.exit(2);
}

const MANDATO = `Sei la seconda AI di verifica di uno studio sulle fonti locali di Roma.
Un primo modello ha letto la fonte e ne ha estratto delle notizie candidate. Il tuo compito non e'
riestrarre: e' dire, per ciascuna, se sei d'accordo con la classificazione.

Per ogni caso rispondi con UNA riga, in questo formato esatto e senza altro testo:

CASO <id> | <concorde|discorde> | <campo contestato o "-"> | <motivo in massimo 20 parole>

Scrivi "discorde" quando almeno una di queste cose e' falsa:
- la notizia non e' sostenuta dall'evidenza allegata (dove l'evidenza c'e');
- il tipo dichiarato e' sbagliato;
- i luoghi elencati non sono luoghi, o non sono a Roma, o non c'entrano con il fatto;
- il titolo dice qualcosa che la sintesi non sostiene.
Non contestare la mancanza di dettagli, ne' il fatto che manchino nomi di persona: sono tolti
apposta. Se il caso non ha evidenza allegata dillo nel motivo e giudica solo la coerenza interna.`;

const blocchi = casi.map(c => {
  const righe = [`--- CASO ${c.id}`,
    `titolo: ${c.titolo}`, `sintesi: ${c.sintesi}`, `tipo dichiarato: ${c.tipo}`,
    `luoghi: ${c.luoghi}`, `data del fatto: ${c.data}`, `qualita dichiarata: ${c.qualita}`];
  if (c.evidenza) {
    const ev = String(c.evidenza);
    righe.push(`evidenza (trascrizione automatica, puo' contenere errori${ev.length > MAX_EVIDENZA ? `; troncata a ${MAX_EVIDENZA} caratteri` : ''}):\n${ev.slice(0, MAX_EVIDENZA)}`);
  }
  else righe.push('evidenza: non allegata (candidata da un atto)');
  return righe.join('\n');
});
const input = MANDATO + '\n\n' + blocchi.join('\n\n');
if (input.length > MAX_INPUT) {
  console.error(`${input.length} caratteri: oltre il tetto di ${MAX_INPUT} per chiamata (--max-input). Dividi l'input o riduci --max-evidenza.`);
  process.exit(2);
}
const body = { model: MODEL, input, reasoning: { effort: 'medium' }, store: false, max_output_tokens: MAX_OUTPUT_TOKENS };

if (dryRun) {
  console.log(`[${casi.length} casi, ${input.length} caratteri]`);
  console.log(blocchi[0].slice(0, 600));
  process.exit(0);
}

(async () => {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 900000);
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    body: JSON.stringify(body), signal: controller.signal,
  }).finally(() => clearTimeout(timer));
  if (!res.ok) { console.error('HTTP', res.status, (await res.text()).slice(0, 400)); process.exit(1); }
  const j = await res.json();
  const testo = (j.output || []).flatMap(o => (o.content || []).map(c => c.text || '')).join('\n').trim();
  const u = j.usage || {};
  const riga = `\n---\nProva T4, modello ${MODEL}, ${casi.length} casi, token ${u.input_tokens} in / ${u.output_tokens} out, ${new Date().toISOString()}\n`;
  if (out) { fs.writeFileSync(out, testo + riga); console.error('scritto', out); }
  console.log(testo + riga);
})();
