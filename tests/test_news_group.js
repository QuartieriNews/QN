#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-group.js: which records of workstream B tell the
 * same fact (docs/pilota/B_RAGGRUPPAMENTO.md, sections 3, 5 and 6; section 8, point 1, lists
 * what this file must cover), the copies kept equal to news-identity.js, news-fact.js and
 * news-collect.js, what the grouping adds on top of news-fact.js (owner choice 3(b)), and the
 * n8n adapter evaluated from the exact committed file with stubbed $input/$json. Every URL,
 * place and text is invented (DEC-109, DEC-031 point 4); the hosts are the sources of
 * CONTRATTI.md section 7 B, with invented paths. T-B-R1-nn name the cases.
 *
 * Run:  node tests/test_news_group.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'news-group.js');
const g = require(FILE);
const identity = require(path.join(__dirname, '..', 'code-nodes', 'news-identity.js'));
const collect = require(path.join(__dirname, '..', 'code-nodes', 'news-collect.js'));

let failures = 0;
let checks = 0;

function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) {
    console.log(`  ok   ${label}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`);
  }
}

function thrown(fn) {
  try { fn(); return null; } catch (e) { return e.message; }
}

/* ----- invented records and schede ------------------------------------------ */

const READ = {
  faro: { page: 'cdn.ilfaroonline.it', url: (s) => `https://www.ilfaroonline.it/2026/11/${s}/` },
  abit: { page: 'abitarearoma.it', url: (s) => `https://www.abitarearoma.it/${s}/` },
  quest: { page: 'questure.poliziadistato.it', url: (s) => `https://questure.poliziadistato.it/it/Roma/articolo/${s}` },
  cara: { page: 'carabinieri.it', url: (s) => `https://www.carabinieri.it/comunicati/${s}` },
};

/** A raw record as news-parse.js writes it. `published` null means the source gives no time. */
function raw(src, slug, published, retrieved, inizio) {
  const r = READ[src];
  return {
    source_id: r.page,
    page: `originali/notizie_${r.page}_${inizio || '20261111T080000Z'}_1.${src === 'faro' || src === 'abit' ? 'xml' : 'html'}`,
    retrieved_at: retrieved || '2026-11-11T08:00:05.000Z',
    url: r.url(slug),
    title: 'Titolo inventato',
    published_at_utc: published,
    categories: [],
    agency: false,
  };
}

const rec = (src, slug, published, retrieved, inizio, index) =>
  g.prepareRecord(raw(src, slug, published, retrieved, inizio), inizio || '20261111T080000Z', index || 0);

const BASE = { ambito: 'cronaca', tipo: 'furto', data_fatto: null, luoghi: [], dettagli: [], fa_nomi: false, aggiornamento: null,
  sintesi: 'Un fatto inventato.' };

/** The schede of a record, through the same check the flow uses. */
function schede(record, list) {
  const res = g.checkSchede({ schede: list.map((s) => Object.assign({}, BASE, s)) }, record);
  if (!res.ok) throw new Error(`test scheda out of form: ${res.motivo}`);
  return res.schede.map((s) => g.withRecord(s, record, res.schede.length));
}
const one = (record, s) => schede(record, [s])[0];

const NOW = '2026-11-15T10:00:00.000Z';
const VIA = (t) => ({ testo: t, livello: 'via' });
const Q = (t) => ({ testo: t, livello: 'quartiere' });
const ETA = (v) => ({ genere: 'eta', valore: v });
const PERS = (v) => ({ genere: 'persone', valore: v });
const OGG = (v) => ({ genere: 'oggetto', valore: v });

/* ----- T-B-R1-01 the copies ---------------------------------------------------- */

console.log('T-B-R1-01 the copies stay byte-equal to their sources');
/** The text of a top-level function or constant of a source file. */
function chunk(text, name) {
  const fn = text.indexOf(`\nfunction ${name}(`);
  if (fn >= 0) return text.slice(fn + 1, text.indexOf('\n}\n', fn) + 2);
  const line = new RegExp(`^const ${name} = .*$`, 'm').exec(text);
  return line ? line[0] : null;
}
const OWN = fs.readFileSync(FILE, 'utf8');
const ID_SRC = fs.readFileSync(path.join(__dirname, '..', 'code-nodes', 'news-identity.js'), 'utf8');
const FACT_SRC = fs.readFileSync(path.join(__dirname, '..', 'code-nodes', 'news-fact.js'), 'utf8');
for (const name of ['TRACKING_PARAM', 'PATH_ENCODE', 'LONE_SURROGATE', 'formEncode', 'formDecode', 'canonicalUrl']) {
  check(`T-B-R1-01 ${name} is the text of news-identity.js`, chunk(OWN, name) !== null && chunk(OWN, name) === chunk(ID_SRC, name), true);
}
for (const name of ['ISO_INSTANT', 'validInstant']) {
  check(`T-B-R1-01 ${name} is the text of news-fact.js`, chunk(OWN, name) !== null && chunk(OWN, name) === chunk(FACT_SRC, name), true);
}
check('T-B-R1-01 the channels are those of SOURCES in news-collect.js', g.SOURCE_CHANNELS,
  Object.fromEntries(collect.SOURCES.map((s) => [s.source_id, s.channel])));
check('T-B-R1-01 the canonical URL of a record matches news-identity.js',
  g.canonicalUrl('https://WWW.ilfaroonline.it/2026/11/x/?utm_source=a'), identity.canonicalUrl('https://WWW.ilfaroonline.it/2026/11/x/?utm_source=a'));

/* ----- T-B-R1-02 preparation --------------------------------------------------- */

console.log('T-B-R1-02 step 1, preparation');
const I0 = '20261111T080000Z';
{
  const r = rec('faro', 'furto-inventato', '2026-11-11T07:00:00.000Z');
  check('T-B-R1-02 a record of Il Faro Online takes source_id from its URL', r.source_id, 'ilfaroonline.it');
  check('T-B-R1-02 …and the channel from the source read', r.source_channel, 'news_press');
  check('T-B-R1-02 …and the canonical URL as its id', r.record_id, 'https://ilfaroonline.it/2026/11/furto-inventato');
  check('T-B-R1-02 …and the source read stays in page', r.page.startsWith('originali/notizie_cdn.ilfaroonline.it_'), true);
  check('T-B-R1-02 …and the day of Rome', [r.giorno, r.giorno_da_retrieved, r.stato], ['2026-11-11', false, 'pronto']);
  check('T-B-R1-02 preparing a prepared record gives the same', g.prepareRecord(r, r.inizio, r.index), r);
  const c = rec('cara', 'arresto-inventato', '2026-11-11T07:00:00.000Z');
  check('T-B-R1-02 the Carabinieri: www goes, official channel', [c.source_id, c.source_channel], ['carabinieri.it', 'news_official']);
  const q = rec('quest', 'riepilogo-inventato', null);
  check('T-B-R1-02 a record without a time takes the day of retrieved_at', [q.giorno, q.giorno_da_retrieved], ['2026-11-11', true]);

  const other = Object.assign(raw('faro', 'x', '2026-11-11T07:00:00.000Z'), { url: 'https://altrosito.it/x/' });
  check('T-B-R1-02 a URL of another host stops the record', g.prepareRecord(other, I0, 0).motivo, 'host_diverso');
  const bare = Object.assign(raw('faro', 'x', '2026-11-11T07:00:00.000Z'), { url: 'https://it/x/' });
  check('T-B-R1-02 …a one-label host too', g.prepareRecord(bare, I0, 0).motivo, 'host_diverso');
  const sub = Object.assign(raw('abit', 'x', '2026-11-11T07:00:00.000Z'), { url: 'https://foto.abitarearoma.it/x/' });
  check('T-B-R1-02 a subdomain of the source read is the same source', g.prepareRecord(sub, I0, 0).source_id, 'foto.abitarearoma.it');
  const noPage = Object.assign(raw('faro', 'x', '2026-11-11T07:00:00.000Z'), { page: undefined });
  check('T-B-R1-02 a record without its page stops', g.prepareRecord(noPage, I0, 0).motivo, 'pagina_mancante');
  const unknown = Object.assign(raw('faro', 'x', '2026-11-11T07:00:00.000Z'), { page: 'originali/notizie_ilmessaggero.it_20261111T080000Z_1.xml' });
  check('T-B-R1-02 a record read from a host that is not a source stops', g.prepareRecord(unknown, I0, 0).motivo, 'fonte_sconosciuta');
  const chan = Object.assign(raw('faro', 'x', '2026-11-11T07:00:00.000Z'), { source_channel: 'news_official' });
  check('T-B-R1-02 a source_channel other than its source\'s stops', g.prepareRecord(chan, I0, 0).motivo, 'canale_diverso');
  check('T-B-R1-02 a date that does not read stops', g.prepareRecord(raw('faro', 'x', '2026-02-30T07:00:00Z'), I0, 0).motivo, 'data_illeggibile');
  check('T-B-R1-02 …no time and no retrieved_at too', g.prepareRecord(Object.assign(raw('quest', 'x', null), { retrieved_at: null }), I0, 0).motivo,
    'data_illeggibile');
  check('T-B-R1-02 a URL that does not read stops', g.prepareRecord(Object.assign(raw('faro', 'x', null), { url: 'ftp://x' }), I0, 0).motivo,
    'url_illeggibile');
  check('T-B-R1-02 a records file is named notizie_righe_<inizio>.json', thrown(() => g.prepareFile({ name: 'notizie_x.json', records: [] })),
    'not a records file: notizie_x.json');
  check('T-B-R1-02 prepareFile keeps the reading order', g.prepareFile({ name: 'notizie_righe_20261111T080000Z.json',
    records: [raw('faro', 'a', null), raw('abit', 'b', null)] }).map((x) => [x.inizio, x.index]), [['20261111T080000Z', 0], ['20261111T080000Z', 1]]);
  check('T-B-R1-02 a page of another run stops the record', g.prepareRecord(raw('faro', 'x', null, null, '20261111T090000Z'), I0, 0).motivo,
    'pagina_di_altra_corsa');
  const files = [
    { name: 'notizie_righe_20261111T080000Z.json', records: [raw('faro', 'a', null), raw('abit', 'b', null)] },
    { name: 'notizie_righe_20261111T090000Z.json', records: [Object.assign(raw('faro', 'a', null, null, '20261111T090000Z'),
      { url: 'https://www.ilfaroonline.it/2026/11/a/?utm_source=feed' })] },
  ];
  const all = g.prepareFiles(files);
  check('T-B-R1-02 a record id already prepared in the pending files stops the later record', all.map((x) => [x.stato, x.motivo || null]),
    [['pronto', null], ['pronto', null], ['fermo', 'record_ripetuto']]);
  check('T-B-R1-02 …naming the first one', all[2].primo, { inizio: '20261111T080000Z', index: 0 });
  check('T-B-R1-02 …and preparing the files again gives the same', g.prepareFiles([{ name: files[0].name, records: all.slice(0, 2) },
    { name: files[1].name, records: all.slice(2) }]), all);
  const reversed = g.prepareFiles(files.slice().reverse());
  check('T-B-R1-02 …whatever the order of the list of files: the same records, in reading order', reversed, all);
  check('T-B-R1-02 a missing list of files fails', thrown(() => g.prepareFiles(undefined)), 'files_missing');
  check('T-B-R1-02 …an empty one is no work', g.prepareFiles([]), []);
}

/* ----- T-B-R1-03 days of Rome ------------------------------------------------------ */

console.log('T-B-R1-03 days of Rome, across the change of hour');
check('T-B-R1-03 summer time: 22:30 UTC is the next day in Rome', g.romeDay('2026-10-24T22:30:00Z'), '2026-10-25');
check('T-B-R1-03 winter time: 23:30 UTC is the next day in Rome', g.romeDay('2026-10-25T23:30:00Z'), '2026-10-26');
check('T-B-R1-03 winter time: 22:30 UTC is still the same day', g.romeDay('2026-10-25T22:30:00Z'), '2026-10-25');
/* ----- T-B-R1-04 the check of the schede ------------------------------------------- */

console.log('T-B-R1-04 step 2, the check of the model\'s schede');
{
  const r = rec('quest', 'riepilogo', '2026-11-11T07:00:00Z');
  const ok = (s) => g.checkSchede({ schede: [Object.assign({}, BASE, s)] }, r);
  check('T-B-R1-04 a scheda in form passes, with its place n', [ok({}).ok, ok({}).schede[0].n], [true, 1]);
  check('T-B-R1-04 a tipo out of the list is out of form', ok({ tipo: 'scippo' }).motivo, 'scheda_1:tipo');
  check('T-B-R1-04 an impossible date is out of form', ok({ data_fatto: '2026-02-30' }).motivo, 'scheda_1:data_fatto');
  check('T-B-R1-04 a fact after the day of its record is out of form', ok({ data_fatto: '2026-11-12' }).motivo, 'scheda_1:data_fatto');
  check('T-B-R1-04 a record without schede is out of form', g.checkSchede({ schede: [] }, r), { ok: false, motivo: 'nessuna_scheda' });
  check('T-B-R1-04 an answer that is not an object of schede is out of form', g.checkSchede([BASE], r), { ok: false, motivo: 'forma' });
  check('T-B-R1-04 a field the scheda does not have (a name) is out of form', ok({ nome: 'X' }).motivo, 'scheda_1:campo_sconosciuto:nome');
  check('T-B-R1-04 a missing fa_nomi is out of form, never a no', g.checkSchede({ schede: [Object.assign({}, BASE, { fa_nomi: undefined })] }, r).motivo,
    'scheda_1:fa_nomi');
  check('T-B-R1-04 a fa_nomi that is not a yes or a no is out of form', ok({ fa_nomi: 'no' }).motivo, 'scheda_1:fa_nomi');
  check('T-B-R1-04 «due» as a number of people is out of form', ok({ dettagli: [{ genere: 'persone', valore: 'due' }] }).motivo, 'scheda_1:dettagli');
  check('T-B-R1-04 «2 persone» too', ok({ dettagli: [{ genere: 'persone', valore: '2 persone' }] }).motivo, 'scheda_1:dettagli');
  check('T-B-R1-04 an age as an integer passes', ok({ dettagli: [ETA(70)] }).ok, true);
  check('T-B-R1-04 an update on a scheda that is not cronaca is out of form',
    ok({ ambito: 'non_cronaca', tipo: null, aggiornamento: 'sentenza' }).motivo, 'scheda_1:aggiornamento');
  check('T-B-R1-04 an update out of the list is out of form', ok({ aggiornamento: 'appello' }).motivo, 'scheda_1:aggiornamento');
  check('T-B-R1-04 a sintesi of two lines is out of form', ok({ sintesi: 'riga\nriga' }).motivo, 'scheda_1:sintesi');
  check('T-B-R1-04 a place without a known level is out of form', ok({ luoghi: [{ testo: 'x', livello: 'zona' }] }).motivo, 'scheda_1:luoghi');
  check('T-B-R1-04 non_cronaca has no tipo', ok({ ambito: 'non_cronaca', tipo: 'furto' }).motivo, 'scheda_1:tipo');
  check('T-B-R1-04 a record not prepared is refused', thrown(() => g.checkSchede({ schede: [BASE] }, { stato: 'fermo' })), 'record_not_prepared');
  const two = schede(r, [{}, { tipo: 'rapina' }]);
  check('T-B-R1-04 schede carry the record id and their place', two.map((s) => s.scheda_id),
    [`${r.record_id}#1`, `${r.record_id}#2`]);
}

/* ----- T-B-R1-23 texts without letters and closed answers ------------------------- */

console.log('T-B-R1-23 texts without letters, closed answers, no names in the signals');
{
  const r = rec('faro', 'a', '2026-11-10T07:00:00Z');
  const ok = (x) => g.checkSchede({ schede: [Object.assign({}, BASE, x)] }, r);
  check('T-B-R1-23 a place made of punctuation is out of form', [ok({ luoghi: [VIA('?')] }).motivo, ok({ luoghi: [VIA('...')] }).motivo],
    ['scheda_1:luoghi', 'scheda_1:luoghi']);
  check('T-B-R1-23 a detail made of punctuation is out of form', [ok({ dettagli: [OGG('—')] }).motivo, ok({ dettagli: [{ genere: 'mezzo', valore: '-' }] }).motivo],
    ['scheda_1:dettagli', 'scheda_1:dettagli']);
  check('T-B-R1-23 names cannot enter through persone or case_status', [ok({ persone: ['Nome Inventato'] }).motivo, ok({ case_status: 'Nome Inventato' }).motivo,
    ok({ persone: true, case_status: null }).ok], ['scheda_1:persone', 'scheda_1:case_status', true]);
  check('T-B-R1-23 until B-R2 fixes its values, any case_status is out of form', [ok({ case_status: 'arrestato' }).motivo, ok({ case_status: 'rossi' }).motivo],
    ['scheda_1:case_status', 'scheda_1:case_status']);
  check('T-B-R1-23 a field outside the form of the answer is out of form', g.checkSchede({ schede: [BASE], nota: 'x' }, r).motivo, 'forma');
}

/* ----- T-B-R1-25 the copies that are not functions -------------------------------- */

console.log('T-B-R1-25 what the file reads from the other nodes and documents');
{
  const parse = require(path.join(__dirname, '..', 'code-nodes', 'news-parse.js'));
  const feed = '<rss version="2.0"><channel><item><title>Titolo inventato</title><link>https://www.ilfaroonline.it/2026/11/11/inventato/</link>' +
    '<pubDate>Wed, 11 Nov 2026 07:00:00 +0000</pubDate></item></channel></rss>';
  const out = parse.newRecords({ files: [{ name: 'notizie_cdn.ilfaroonline.it_20261111T080000Z_1.xml', body: feed }], seen: [], retrieved_at: '2026-11-11T08:00:05.000Z' });
  const prepared = g.prepareFile({ name: 'notizie_righe_20261111T080000Z.json', records: out.records });
  check('T-B-R1-25 a record as news-parse.js writes it is prepared', prepared.map((x) => [x.stato, x.source_channel, x.source_id]),
    [['pronto', 'news_press', 'ilfaroonline.it']]);
  for (const u of ['https://www.carabinieri.it/x', 'https://questure.poliziadistato.it/it/Roma/articolo/y', 'https://WWW.AbitareARoma.it:443/z?utm_source=a']) {
    const page = /carabinieri/.test(u) ? 'carabinieri.it' : /questure/.test(u) ? 'questure.poliziadistato.it' : 'abitarearoma.it';
    const r = g.prepareRecord({ url: u, page: `originali/notizie_${page}_20261111T080000Z_1.html`, published_at_utc: '2026-11-11T07:00:00Z' }, '20261111T080000Z', 0);
    check(`T-B-R1-25 source_id is sourceIdFromUrl of news-identity.js (${page})`, r.source_id, identity.sourceIdFromUrl(u));
  }
  const md = fs.readFileSync(path.join(__dirname, '..', 'tools', 'cronaca-prova', 'ISTRUZIONI_CHIUSE.md'), 'utf8');
  const tipo = /"tipo": "([^"]+)"/.exec(md.replace(/\s*\n\s*/g, ''))[1].split('|');
  check('T-B-R1-25 TIPI is the list of ISTRUZIONI_CHIUSE.md', g.TIPI, tipo);
}

/* ----- T-B-R1-22 the n8n adapter ------------------------------------------------------- */

console.log('T-B-R1-22 n8n adapter, from the exact committed file');
const SRC = fs.readFileSync(FILE, 'utf8');
/** Runs the committed file as the n8n Code node does, on one item. */
function adapter(json) {
  const item = { json };
  const out = new Function('$input', '$json', 'require', 'module', SRC)({ item }, json, require, { exports: {} });
  return { item, out };
}
{
  const r = rec('quest', 'a', '2026-11-10T07:00:00Z');
  const { item, out } = adapter({ stage: 'check_schede', risposta: { schede: [BASE] }, record: r, other: 'kept' });
  check('T-B-R1-22 the adapter returns the item', out === item, true);
  check('T-B-R1-22 …with the check', item.json.check.ok, true);
  check('T-B-R1-22 …and each scheda with its record id and scheda id', [item.json.check.schede[0].record_id, item.json.check.schede[0].scheda_id],
    [r.record_id, `${r.record_id}#1`]);
  check('T-B-R1-22 …the same as withRecord', item.json.check.schede, schede(r, [{}]));
  check('T-B-R1-22 an answer out of form keeps its motive', adapter({ stage: 'check_schede', risposta: { schede: [] }, record: r }).item.json.check,
    { ok: false, motivo: 'nessuna_scheda' });
  check('T-B-R1-22 …keeping the other fields', item.json.other, 'kept');
  const prep = adapter({ stage: 'prepare', files: [{ name: 'notizie_righe_20261111T080000Z.json', records: [raw('faro', 'x', null)] }] }).item;
  check('T-B-R1-22 the prepare stage', prep.json.records.map((x) => x.source_id), ['ilfaroonline.it']);
  check('T-B-R1-22 a prepare item without files fails', thrown(() => adapter({ stage: 'prepare' })), 'files_missing');
  check('T-B-R1-22 an unknown stage fails', thrown(() => adapter({ stage: 'altro' })), 'stage_unknown: altro');
}

/* ===== steps 3 and 4: comparisons, candidates, the check of a judgment ===== */

/* ----- facts and judgments for the steps after the first two --------------------- */

/** A table of facts, each opened by the given scheda: written here, not by the code under test. */
function open(table, s, stato) {
  const inDoubt = stato === 'in_dubbio';
  return table.concat([{ content_id: g.factId(s), aperto_il: NOW, stato: stato || 'aperto', regola: 'esercizio',
    schede: [Object.assign({}, s, { ruolo: 'apre' })], dubbio: inDoubt ? { candidati: [], motivi: [{ content_id: null, motivo: 'nomi' }] } : null,
    quality: { review_flags: inDoubt ? ['duplicate_doubt'] : [], requires_review: inDoubt } }]);
}
function join(table, s, id, ruolo) {
  return table.map((f) => (f.content_id === id ? Object.assign({}, f, { schede: f.schede.concat([Object.assign({}, s, { ruolo: ruolo || 'stesso_fatto' })]) }) : f));
}

/** A judgment: `verdicts` by content_id, a proof built from the first shown scheda. */
function judge(lista, verdicts) {
  return g.checkGiudizio({ giudizi: lista.candidati.map((c) => {
    const v = verdicts[c.content_id] || { verdetto: 'diverso' };
    if (v.verdetto !== 'stesso') return { content_id: c.content_id, verdetto: v.verdetto };
    return { content_id: c.content_id, verdetto: 'stesso', prove: { scheda_id: v.scheda_id || c.mostrate[0].scheda_id, luogo: v.luogo,
      dettagli: v.dettagli || [] } };
  }) }, lista);
}

/* ----- T-B-R1-03 the window across the change of hour ----------------------------- */

console.log('T-B-R1-03 the window across the change of hour');
{
  // Seven days of Rome apart across the October change, one hour less in UTC.
  const a = one(rec('faro', 'a', '2026-10-21T22:30:00Z'), {}); // 22 October in Rome
  const b = one(rec('abit', 'b', '2026-10-28T23:30:00Z'), {}); // 29 October in Rome
  const c = one(rec('abit', 'c', '2026-10-29T23:30:00Z'), {}); // 30 October in Rome
  check('T-B-R1-03 the window counts days of Rome, not hours', [a.giorno, b.giorno, g.dateWindow(a, b).any, g.dateWindow(a, c).any],
    ['2026-10-22', '2026-10-29', true, false]);
}


/* ----- T-B-R1-05 families ------------------------------------------------------------ */

console.log('T-B-R1-05 families of tipo');
check('T-B-R1-05 the families use only the values of tipo', Object.values(g.FAMIGLIE).flat().every((t) => g.TIPI.includes(t)), true);
check('T-B-R1-05 every tipo but altro is in a family', g.TIPI.filter((t) => t !== 'altro').every((t) => Object.values(g.FAMIGLIE).some((f) => f.includes(t))), true);
check('T-B-R1-05 furto, rapina and truffa are one family', [g.sameFamily('furto', 'rapina'), g.sameFamily('truffa', 'furto')], [true, true]);
check('T-B-R1-05 an arrest goes with the offence', [g.sameFamily('arresto', 'droga'), g.sameFamily('arresto', 'rapina')], [true, true]);
check('T-B-R1-05 a theft is not a fire', g.sameFamily('furto', 'incendio'), false);
check('T-B-R1-05 altro is only its own family', [g.sameFamily('altro', 'altro'), g.sameFamily('altro', 'furto')], [true, false]);

/* ----- T-B-R1-06 details and places ------------------------------------------------- */

console.log('T-B-R1-06 details equal by value, not by form');
{
  const r = rec('faro', 'a', '2026-11-11T07:00:00Z');
  const a = one(r, { luoghi: [VIA('Via dei Mandorli Finti')], dettagli: [ETA(70), OGG('Auto')] });
  const b = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('via dei mandorli finti.')], dettagli: [ETA(70), { genere: 'mezzo', valore: 'auto' }] });
  const c = one(rec('abit', 'c', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via dei Màndorli Finti')], dettagli: [{ genere: 'mezzo', valore: 'vettura' }] });
  check('T-B-R1-06 the same place, without case and punctuation', g.sharedPlaces(a, b, ['via']), ['via dei mandorli finti']);
  check('T-B-R1-06 …and without accents', g.sharedPlaces(a, c, ['via']), ['via dei mandorli finti']);
  check('T-B-R1-06 oggetto and mezzo are one kind; numbers as numbers', g.sharedDetails(a, b), ['eta:70', 'oggetto:auto']);
  check('T-B-R1-06 two words for one thing are not equal', g.sharedDetails(a, c), []);
  check('T-B-R1-06 things equal: the place counts one, each detail one', g.sameThings(a, b), 3);
  const q = one(rec('abit', 'd', '2026-11-11T07:00:00Z'), { luoghi: [Q('Quartiere Inventato')] });
  const q2 = one(rec('faro', 'e', '2026-11-11T07:00:00Z'), { luoghi: [Q('quartiere inventato')] });
  check('T-B-R1-06 a quarter is not a place the code compares', g.sameThings(q, q2), 0);
}

/* ----- T-B-R1-07 the date search ------------------------------------------------------- */

console.log('T-B-R1-07 the date search');
{
  const d = (src, slug, pub, s, ret) => one(rec(src, slug, pub, ret), s);
  const a = d('faro', 'a', '2026-11-11T07:00:00Z', { data_fatto: '2026-11-09' });
  check('T-B-R1-07 both days of the fact: at most 3 days', [g.dateWindow(a, d('abit', 'b', '2026-11-11T07:00:00Z', { data_fatto: '2026-11-06' })).any,
    g.dateWindow(a, d('abit', 'c', '2026-11-11T07:00:00Z', { data_fatto: '2026-11-05' })).any], [true, false]);
  const noDf = d('abit', 'e', '2026-11-16T07:00:00Z', {});
  check('T-B-R1-07 the day of the fact in one only: against the other\'s publication, 7 days', g.dateWindow(a, noDf).any, true);
  const late = d('quest', 'f', '2026-11-25T07:00:00Z', { data_fatto: '2026-11-10' });
  const press = d('faro', 'g', '2026-11-11T07:00:00Z', {});
  check('T-B-R1-07 a late release that gives the day of its fact finds the press', g.dateWindow(late, press).any, true);
  const upd = d('faro', 'h', '2026-11-13T07:00:00Z', { aggiornamento: 'convalida' });
  check('T-B-R1-07 the publication day of an update is not a day of the fact', g.dateWindow(upd, press).any, false);
  const r1 = d('quest', 'i', null, {}, '2026-11-12T08:00:00Z');
  check('T-B-R1-07 a day from retrieved_at is found, but not clean', g.dateWindow(r1, press), { any: true, clean: false });
}

/* ----- T-B-R1-08 the candidates --------------------------------------------------------- */

console.log('T-B-R1-08 candidates found by date, by place, and among all facts');
{
  const old = one(rec('faro', 'vecchio', '2026-06-01T07:00:00Z'), { data_fatto: '2026-05-31', luoghi: [VIA('Via Inventata')] });
  let t = open([], old);
  const byPlace = one(rec('abit', 'nuovo', '2026-11-11T07:00:00Z'), { data_fatto: '2026-11-10', luoghi: [VIA('via inventata')] });
  const l1 = g.candidates(byPlace, t);
  check('T-B-R1-08 the same place finds a fact months before', [l1.candidati.length, l1.candidati[0].trovato.luogo, l1.candidati[0].trovato.data], [1, true, false]);
  const fire = one(rec('abit', 'fuoco', '2026-11-11T07:00:00Z'), { tipo: 'incendio', luoghi: [VIA('via inventata')] });
  check('T-B-R1-08 …only within the family', g.candidates(fire, t).candidati.length, 0);
  const official = one(rec('quest', 'comunicato', '2026-11-11T07:00:00Z'), { tipo: 'rapina' });
  check('T-B-R1-08 a release without the day of its fact looks among all the facts of its family', g.candidates(official, t).candidati[0].trovato.tutti, true);
  const upd = one(rec('faro', 'sentenza', '2026-11-11T07:00:00Z'), { tipo: 'incendio', aggiornamento: 'sentenza' });
  check('T-B-R1-08 an update looks among all facts, of any family', g.candidates(upd, t).candidati.length, 1);
  const press = one(rec('faro', 'altro-furto', '2026-11-11T07:00:00Z'), {});
  check('T-B-R1-08 a press scheda far in time and place finds nothing', g.candidates(press, t).candidati.length, 0);

  // A fact without a date, opened by a release, is found both ways.
  const undated = one(rec('quest', 'senza-data', null, '2026-11-12T08:00:00Z'), { tipo: 'truffa' });
  t = open([], undated);
  const after = one(rec('abit', 'dopo', '2026-11-20T07:00:00Z'), { data_fatto: '2026-11-19' });
  check('T-B-R1-08 a later press scheda finds a fact without a date', g.candidates(after, t).candidati[0].trovato.senza_data, true);
  let t2 = open([], after);
  check('T-B-R1-08 …and the release finds the press scheda that came first', g.candidates(undated, t2).candidati.length, 1);

  check('T-B-R1-08 a fact opened by a press scheda without the day of its fact is not a fact without a date',
    [g.undatedFact(open([], one(rec('faro', 'stampa', '2026-11-11T07:00:00Z'), {}))[0]), g.undatedFact(t[0])], [false, true]);

  const two = schede(rec('quest', 'riepilogo', '2026-11-11T07:00:00Z'), [{ luoghi: [VIA('Via A')] }, { luoghi: [VIA('Via A')] }]);
  t2 = open([], two[0]);
  check('T-B-R1-08 two schede of one record are never the same fact', g.candidates(two[1], t2).candidati.length, 0);

  let t3 = open([], old);
  t3 = t3.map((f) => Object.assign({}, f, { stato: 'unito' }));
  check('T-B-R1-08 a merged fact is never a candidate', g.candidates(byPlace, t3).candidati.length, 0);
  const t4 = open([], old, 'in_dubbio');
  check('T-B-R1-08 a fact in doubt is', g.candidates(byPlace, t4).candidati.length, 1);
  check('T-B-R1-08 a scheda that is not cronaca has no candidates', thrown(() => g.candidates(Object.assign({}, byPlace, { ambito: 'non_cronaca' }), t)),
    'not_cronaca');
}

/* ----- T-B-R1-09 the cap of 10 ------------------------------------------------------- */

console.log('T-B-R1-09 the cap of 10 and the cut list');
{
  // Twelve facts of the days around, and an older one with the same street and the days in place.
  let t = [];
  for (let i = 0; i < 12; i += 1) {
    t = open(t, one(rec('abit', `vicino-${String(i).padStart(2, '0')}`, '2026-11-11T07:00:00Z'), { luoghi: [VIA(`Via ${i}`)] }));
  }
  const proof = one(rec('faro', 'con-prove', '2026-11-05T07:00:00Z'), { luoghi: [VIA('Via dei Pini Finti')], dettagli: [ETA(40)] });
  t = open(t, proof);
  const s = one(rec('quest', 'arrivo', '2026-11-11T09:00:00Z'), { data_fatto: '2026-11-05', luoghi: [VIA('Via dei Pini Finti')], dettagli: [ETA(40)] });
  const l = g.candidates(s, t);
  check('T-B-R1-09 at most 10 candidates', [l.candidati.length, l.esclusi], [10, 3]);
  check('T-B-R1-09 the fact that can be certain comes first', l.candidati[0].content_id, g.factId(proof));
  check('T-B-R1-09 a press scheda with no undated fact left out is not cut', l.tagliata, false);

  // An undated fact of the family left out and in its limit cuts the list of a press scheda.
  const undated = one(rec('quest', 'senza-data', null, '2026-11-10T08:00:00Z'), {});
  const tu = open(t, undated);
  const press = one(rec('abit', 'stampa', '2026-11-11T09:00:00Z'), {});
  const lp = g.candidates(press, tu);
  check('T-B-R1-09 a press scheda with an undated fact in its limit left out goes in doubt',
    [lp.candidati.some((c) => c.content_id === g.factId(undated)), lp.tagliata], [false, true]);
  const farPress = one(rec('abit', 'stampa-dopo', '2026-11-25T09:00:00Z'), { data_fatto: '2026-11-24' });
  // Twelve facts of the 24th fill the list by date; the undated fact opened on the 10th is left out.
  let tf = [];
  for (let i = 0; i < 12; i += 1) {
    tf = open(tf, one(rec('abit', `tardi-${String(i).padStart(2, '0')}`, '2026-11-24T07:00:00Z'), { luoghi: [VIA(`Via ${i}`)] }));
  }
  tf = open(tf, undated);
  const lf = g.candidates(farPress, tf);
  check('T-B-R1-09 …but not one outside its limit (the fact after the first record)', [lf.candidati.some((c) => c.content_id === g.factId(undated)), lf.tagliata],
    [false, false]);
  const upd = one(rec('faro', 'aggiornamento', '2026-11-11T09:00:00Z'), { aggiornamento: 'processo' });
  check('T-B-R1-09 an update that looks among all facts is cut by any fact left out', g.candidates(upd, t).tagliata, true);
}

/* ----- T-B-R1-10 the schede shown ------------------------------------------------------ */

console.log('T-B-R1-10 the model sees three schede of a fact');
{
  const opener = one(rec('quest', 'apre', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  let t = open([], opener);
  const id = g.factId(opener);
  const more = [
    one(rec('abit', 'b1', '2026-11-10T08:00:00Z'), { luoghi: [VIA('Via X')] }),
    one(rec('abit', 'b2', '2026-11-10T09:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30)] }),
    one(rec('faro', 'b3', '2026-11-10T10:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(2)] }),
    one(rec('faro', 'b4', '2026-11-10T11:00:00Z'), {}),
  ];
  for (const s of more) t = join(t, s, id);
  const s = one(rec('abit', 'nuova', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(2)] });
  const shown = g.candidates(s, t).candidati[0].mostrate.map((x) => x.scheda_id);
  check('T-B-R1-10 the opener and the two with more things equal', shown, [opener.scheda_id, more[2].scheda_id, more[1].scheda_id]);
}

/* ----- T-B-R1-11 the check of a judgment ------------------------------------------ */

console.log('T-B-R1-11 step 4, the check of the model\'s judgment');
{
  const a = one(rec('quest', 'a', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const t = open([], a);
  const s = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const l = g.candidates(s, t);
  const id = l.candidati[0].content_id;
  check('T-B-R1-11 a judgment for every candidate passes', g.checkGiudizio({ giudizi: [{ content_id: id, verdetto: 'diverso' }] }, l).ok, true);
  check('T-B-R1-11 a missing candidate is out of form', g.checkGiudizio({ giudizi: [] }, l), { ok: false, motivo: 'candidati' });
  check('T-B-R1-11 a fact that is not a candidate is out of form', g.checkGiudizio({ giudizi: [{ content_id: 'qn:roma:nws:x', verdetto: 'diverso' }] }, l).motivo,
    'candidati');
  check('T-B-R1-11 the same candidate twice is out of form', g.checkGiudizio({ giudizi: [{ content_id: id, verdetto: 'diverso' },
    { content_id: id, verdetto: 'diverso' }] }, l).motivo, 'candidati');
  check('T-B-R1-11 stesso without its proof is out of form', g.checkGiudizio({ giudizi: [{ content_id: id, verdetto: 'stesso' }] }, l).motivo, 'prove');
  check('T-B-R1-11 a verdict out of the list is out of form', g.checkGiudizio({ giudizi: [{ content_id: id, verdetto: 'simile' }] }, l).motivo, 'verdetto');
  check('T-B-R1-11 a detail of the proof out of form is out of form', g.checkGiudizio({ giudizi: [{ content_id: id, verdetto: 'stesso',
    prove: { scheda_id: a.scheda_id, luogo: 'Via X', dettagli: [{ genere: 'eta', valore: 'settanta' }] } }] }, l).motivo, 'prove');
}

/* ----- T-B-R1-27 texts without letters are never the same thing ------------------- */

console.log('T-B-R1-27 texts without letters are never the same thing; closed judgments');
{
  const r = rec('faro', 'a', '2026-11-10T07:00:00Z');
  const empty = Object.assign(one(r, {}), { luoghi: [VIA('?')], dettagli: [OGG('—')] });
  const empty2 = Object.assign(one(rec('abit', 'b', '2026-11-11T07:00:00Z'), {}), { luoghi: [VIA('...')], dettagli: [OGG('-')] });
  check('T-B-R1-27 two texts of punctuation are never the same place or detail', [g.sharedPlaces(empty, empty2, ['via']), g.sharedDetails(empty, empty2)], [[], []]);
  const t = open([], empty);
  const l = g.candidates(empty2, t);
  check('T-B-R1-27 a proof whose place is punctuation is out of form', g.checkGiudizio({ giudizi: l.candidati.map((c) => ({ content_id: c.content_id,
    verdetto: 'stesso', prove: { scheda_id: c.mostrate[0].scheda_id, luogo: '?', dettagli: [] } })) }, l).motivo, 'prove');
  const a = one(rec('quest', 'c', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const ta = open([], a);
  const s2 = one(rec('abit', 'd', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const l2 = g.candidates(s2, ta);
  check('T-B-R1-27 a field outside the form of a judgment is out of form', [g.checkGiudizio({ giudizi: [], nota: 'x' }, l2).motivo,
    g.checkGiudizio({ giudizi: [{ content_id: l2.candidati[0].content_id, verdetto: 'diverso', nota: 'x' }] }, l2).motivo], ['forma', 'forma']);
}

console.log('T-B-R1-01 the identity of a fact is the copy of news-identity.js');
for (const name of ['sha256', 'newsIdentity']) {
  check(`T-B-R1-01 ${name} is the text of news-identity.js`, chunk(OWN, name) !== null && chunk(OWN, name) === chunk(ID_SRC, name), true);
}
check('T-B-R1-01 the content_id of a fact is the one of news-identity.js', g.factId(one(rec('faro', 'x', '2026-11-11T07:00:00Z'), {})),
  identity.newsIdentity({ opening_url: 'https://www.ilfaroonline.it/2026/11/x/' }).content_id);

console.log('T-B-R1-32 the key of a list');
{
  const a = one(rec('quest', 'a', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const t = open([], a);
  const s2 = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const k = g.listKey(g.candidates(s2, t));
  check('T-B-R1-32 the same list has the same key', g.listKey(g.candidates(s2, t)), k);
  const t2 = join(t, one(rec('faro', 'c', '2026-11-10T09:00:00Z'), { luoghi: [VIA('Via X')] }), t[0].content_id);
  check('T-B-R1-32 a candidate whose shown schede changed has another key', g.listKey(g.candidates(s2, t2)) !== k, true);
}

/* ----- T-B-R1-24 more of section 8, point 1: the candidates ----------------------- */

console.log('T-B-R1-24 more of section 8, point 1: the candidates');
{
  let t = [];
  const far = one(rec('faro', 'lontano', '2026-11-01T07:00:00Z'), {});
  const near = one(rec('abit', 'vicino', '2026-11-10T07:00:00Z'), {});
  t = open(open(t, far), near);
  const s = one(rec('faro', 'oggi', '2026-11-08T07:00:00Z'), {});
  check('T-B-R1-24 at equal things, the nearest by date first', g.candidates(s, t).candidati.map((c) => c.content_id), [g.factId(near), g.factId(far)]);
  let many = [];
  for (let d = 1; d <= 12; d += 1) many = open(many, one(rec('abit', `giorno-${d}`, `2026-11-${String(d).padStart(2, '0')}T07:00:00Z`), {}));
  const mid = one(rec('faro', 'meta', '2026-11-08T07:00:00Z'), {});
  const lm = g.candidates(mid, many);
  check('T-B-R1-24 over the cap, the facts of the nearest days stay in the list', [lm.esclusi,
    many.filter((f) => !lm.candidati.some((c) => c.content_id === f.content_id)).map((f) => f.schede[0].giorno)], [2, ['2026-11-01', '2026-11-02']]);
  const undated = open([], one(rec('quest', 'senza-data', null, '2026-11-01T08:00:00Z'), {}))[0];
  const p7 = one(rec('abit', 'sette', '2026-11-08T07:00:00Z'), {});
  const p8 = one(rec('abit', 'otto', '2026-11-09T07:00:00Z'), {});
  check('T-B-R1-24 a press scheda without the day of its fact: an undated fact is in its limit up to 7 days', [g.inLimit(p7, undated), g.inLimit(p8, undated)],
    [true, false]);
  const dated = one(rec('abit', 'datata', '2026-11-20T07:00:00Z'), { data_fatto: '2026-10-31' });
  check('T-B-R1-24 …with the day of its fact, when the fact is not after the first record', [g.inLimit(dated, undated),
    g.inLimit(Object.assign({}, dated, { data_fatto: '2026-11-02' }), undated)], [true, false]);
  let full = [];
  for (let i = 0; i < 11; i += 1) full = open(full, one(rec('abit', `pieno-${String(i).padStart(2, '0')}`, '2026-11-10T07:00:00Z'), {}));
  const release = one(rec('quest', 'comunicato', '2026-11-11T07:00:00Z'), {});
  check('T-B-R1-24 a release without the day of its fact, with facts left out, has a cut list', g.candidates(release, full).tagliata, true);
}

/* ----- T-B-R1-26 the stage check_giudizio of the adapter ------------------------ */

console.log('T-B-R1-26 the stage check_giudizio of the n8n adapter');
{
  const a = one(rec('quest', 'a', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const t = open([], a);
  const l = g.candidates(one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')] }), t);
  check('T-B-R1-26 check_giudizio', adapter({ stage: 'check_giudizio', risposta: { giudizi: [{ content_id: l.candidati[0].content_id, verdetto: 'diverso' }] },
    lista: l }).item.json.check.ok, true);
}

/* ===== step 5, a run, publication ===== */

const factNode = require(path.join(__dirname, '..', 'code-nodes', 'news-fact.js'));

console.log('T-B-R1-31 the facts written by hand in these tests are those the code writes');
{
  const s = one(rec('quest', 'a', '2026-11-10T07:00:00Z'), {});
  check('T-B-R1-31 an open fact', open([], s), g.applyDecision([], s, { azione: 'apri', stato: 'aperto', motivi: [] }, NOW, 'esercizio'));
  check('T-B-R1-31 a fact in doubt', open([], s, 'in_dubbio'), g.applyDecision([], s, { azione: 'apri', stato: 'in_dubbio',
    motivi: [{ content_id: null, motivo: 'nomi' }] }, NOW, 'esercizio'));
  const t = open([], s);
  const s2 = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), {});
  check('T-B-R1-31 a scheda that joins', join(t, s2, t[0].content_id), g.applyDecision(t, s2, { azione: 'unisci', content_id: t[0].content_id,
    ruolo: 'stesso_fatto', motivi: [] }, NOW, 'esercizio'));
}

/* ----- T-B-R1-12 certain: the invented example of section 5 ---------------------- */

console.log('T-B-R1-12 certain, the example of section 5');
{
  const release = rec('quest', 'due-interventi', '2026-11-10T09:00:00Z');
  const [fire, car] = schede(release, [
    { tipo: 'incendio', data_fatto: '2026-11-09', luoghi: [VIA('via dei Mandorli Finti')], dettagli: [PERS(2), ETA(70)] },
    { tipo: 'furto', data_fatto: '2026-11-09', dettagli: [OGG('auto')] },
  ]);
  let t = open([], fire);
  t = open(t, car);
  const press = one(rec('abit', 'incendio-garage', '2026-11-11T07:00:00Z'),
    { tipo: 'incendio', luoghi: [VIA('Via dei Mandorli Finti')], dettagli: [PERS(2), ETA(70)] });
  const l = g.candidates(press, t);
  const id = g.factId(fire);
  const d = g.decide(press, l, judge(l, { [id]: { verdetto: 'stesso', luogo: 'via dei Mandorli Finti', dettagli: [PERS(2), ETA(70)] } }), t, 'esercizio');
  check('T-B-R1-12 the press scheda joins the fact of scheda 1', d, { azione: 'unisci', content_id: id, ruolo: 'stesso_fatto', motivi: [] });
  check('T-B-R1-12 the fact keeps the id of the release, with -f1', id, `${identity.newsIdentity({ opening_url: release.url, fact_index: 1 }).content_id}`);
  check('T-B-R1-12 …which ends in -f1', id.endsWith('-f1'), true);
  t = g.applyDecision(t, press, d, '2026-11-11T08:00:00Z', 'esercizio');
  const f = t.find((x) => x.content_id === id);
  check('T-B-R1-12 the fact has two sources, roles apre and stesso_fatto', f.schede.map((x) => x.ruolo), ['apre', 'stesso_fatto']);
  check('T-B-R1-12 aperto_il does not change when a scheda joins', f.aperto_il, NOW);
  const res = factNode.factSources(g.factRecords(f));
  check('T-B-R1-12 news-fact.js reads the records of the fact as they are', [res.categoria, res.capofila.source_id], ['ufficiale', 'questure.poliziadistato.it']);
  const solo = one(rec('faro', 'solo', '2026-11-11T07:00:00Z'), {});
  check('T-B-R1-12 a record of one fact has no -f', g.factId(solo).endsWith('-f1'), false);
}

/* ----- T-B-R1-13 proofs that do not hold, the two rules ------------------------- */

console.log('T-B-R1-13 proofs that do not hold, and the comparison rule');
{
  const a = one(rec('faro', 'a', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X'), Q('Quartiere Y')], dettagli: [ETA(30), PERS(1)] });
  const t = open([], a);
  const id = g.factId(a);
  const s = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X'), Q('Quartiere Y')], dettagli: [ETA(30), PERS(1)] });
  const l = g.candidates(s, t);
  const dec = (v, rule) => g.decide(s, l, judge(l, { [id]: Object.assign({ verdetto: 'stesso' }, v) }), t, rule || 'esercizio');
  check('T-B-R1-13 place and two details: certain', dec({ luogo: 'Via X', dettagli: [ETA(30), PERS(1)] }).azione, 'unisci');
  check('T-B-R1-13 a cited detail that is not there: doubt, prove', dec({ luogo: 'Via X', dettagli: [ETA(30), PERS(1), ETA(31)] }).motivi,
    [{ content_id: id, motivo: 'prove' }]);
  check('T-B-R1-13 a cited place that is not there: doubt', dec({ luogo: 'Via Z', dettagli: [ETA(30), PERS(1)] }).stato, 'in_dubbio');
  check('T-B-R1-13 a cited scheda the model did not see: doubt', dec({ scheda_id: 'https://x.it/y#1', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] }).stato,
    'in_dubbio');
  check('T-B-R1-13 one detail only (owner choice 2): doubt', dec({ luogo: 'Via X', dettagli: [ETA(30)] }).stato, 'in_dubbio');
  check('T-B-R1-13 the same detail twice counts once', dec({ luogo: 'Via X', dettagli: [ETA(30), ETA(30)] }).stato, 'in_dubbio');
  check('T-B-R1-13 a quarter only: doubt with the rule in use', dec({ luogo: 'Quartiere Y' }).stato, 'in_dubbio');
  check('T-B-R1-13 a quarter only and no detail: certain with the comparison rule', dec({ luogo: 'Quartiere Y' }, 'confronto').azione, 'unisci');
  check('T-B-R1-13 no place at all is never certain, with either rule', [dec({ luogo: null, dettagli: [ETA(30), PERS(1)] }).stato,
    dec({ luogo: null }, 'confronto').stato], ['in_dubbio', 'in_dubbio']);
  check('T-B-R1-13 forse is a doubt', g.decide(s, l, judge(l, { [id]: { verdetto: 'forse' } }), t, 'esercizio').motivi, [{ content_id: id, motivo: 'forse' }]);
  check('T-B-R1-13 diverso opens a fact of its own', g.decide(s, l, judge(l, {}), t, 'esercizio'), { azione: 'apri', stato: 'aperto', motivi: [] });
  check('T-B-R1-13 an unknown rule is refused', thrown(() => g.decide(s, l, judge(l, {}), t, 'larga')), 'regola_unknown');
}

/* ----- T-B-R1-14 days from retrieved_at ------------------------------------------- */

console.log('T-B-R1-14 dates only from retrieved_at are never certain');
{
  const a = one(rec('faro', 'a', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] });
  const t = open([], a);
  const id = g.factId(a);
  const s = one(rec('quest', 'b', null, '2026-11-12T08:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] });
  const l = g.candidates(s, t);
  check('T-B-R1-14 a scheda whose days come from retrieved_at goes in doubt',
    g.decide(s, l, judge(l, { [id]: { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] } }), t, 'esercizio').motivi,
    [{ content_id: id, motivo: 'prove' }]);
  const s2 = one(rec('quest', 'c', null, '2026-11-12T08:00:00Z'), { data_fatto: '2026-11-10', luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] });
  const l2 = g.candidates(s2, t);
  check('T-B-R1-14 …unless it gives the day of its fact and the window holds on it',
    g.decide(s2, l2, judge(l2, { [id]: { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] } }), t, 'esercizio').azione, 'unisci');
}

/* ----- T-B-R1-15 names (owner choice 6) ----------------------------------------- */

console.log('T-B-R1-15 the names of the sixth choice');
{
  const proof = { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] };
  const S = { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] };
  const run = (factNames, mineNames, extraNames, upd) => {
    const a = one(rec('faro', 'a', '2026-11-10T07:00:00Z'), Object.assign({}, S, { fa_nomi: factNames }));
    let t = open([], a);
    const id = g.factId(a);
    if (extraNames !== undefined) t = join(t, one(rec('faro', 'a2', '2026-11-10T09:00:00Z'), Object.assign({}, S, { fa_nomi: extraNames })), id);
    const s = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), Object.assign({}, S, { fa_nomi: mineNames }, upd ? { aggiornamento: 'convalida', data_fatto: '2026-11-10' } : {}));
    const l = g.candidates(s, t);
    return g.decide(s, l, judge(l, { [id]: Object.assign({ scheda_id: a.scheda_id }, proof) }), t, 'esercizio');
  };
  check('T-B-R1-15 names in both: doubt, nomi', run(true, true).motivi.map((m) => m.motivo), ['nomi']);
  check('T-B-R1-15 names in one only: certain', [run(true, false).azione, run(false, true).azione], ['unisci', 'unisci']);
  check('T-B-R1-15 names in a scheda of the fact the model does not cite: doubt', run(false, true, true).motivi.map((m) => m.motivo), ['nomi']);
  check('T-B-R1-15 an update with names, to a fact with names: doubt', run(true, true, undefined, true).motivi.map((m) => m.motivo), ['nomi']);
}

/* ----- T-B-R1-16 bridges ----------------------------------------------------------- */

console.log('T-B-R1-16 a bridge never merges two facts alone');
{
  const S = { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] };
  const proof = { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] };
  const a = one(rec('faro', 'a', '2026-11-10T07:00:00Z'), Object.assign({ fa_nomi: true }, S));
  const b = one(rec('abit', 'b', '2026-11-10T08:00:00Z'), Object.assign({ fa_nomi: true }, S));
  let t = open([], a);
  t = open(t, b, 'in_dubbio'); // in doubt for the names
  const [ia, ib] = [g.factId(a), g.factId(b)];
  const release = one(rec('quest', 'c', '2026-11-11T07:00:00Z'), Object.assign({ data_fatto: '2026-11-10' }, S));
  const l = g.candidates(release, t);
  const both = g.decide(release, l, judge(l, { [ia]: proof, [ib]: proof }), t, 'esercizio');
  check('T-B-R1-16 certain with two facts, one in doubt for the names: doubt, certa twice', both.motivi.map((m) => m.motivo), ['certa', 'certa']);
  const mixed = g.decide(release, l, judge(l, { [ia]: proof, [ib]: { verdetto: 'forse' } }), t, 'esercizio');
  check('T-B-R1-16 certain with one, forse with another: doubt', [mixed.stato, mixed.motivi.map((m) => m.motivo).sort()], ['in_dubbio', ['certa', 'forse']]);
  const t2 = g.applyDecision(t, release, mixed, NOW, 'esercizio');
  const f = t2[t2.length - 1];
  check('T-B-R1-16 the scheda in doubt opens its fact with the candidates and the signals of the events',
    [f.stato, f.dubbio.candidati.length, f.quality], ['in_dubbio', 2, { review_flags: ['duplicate_doubt'], requires_review: true }]);
  check('T-B-R1-16 the candidates go on: the dubious scheda touches no other fact', t2.slice(0, 2).map((x) => x.schede.length), [1, 1]);
}

/* ----- T-B-R1-17 updates --------------------------------------------------------- */

console.log('T-B-R1-17 updates');
{
  const S = { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] };
  const proof = { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] };
  const a = one(rec('faro', 'a', '2026-03-10T07:00:00Z'), Object.assign({ tipo: 'rapina', data_fatto: '2026-03-09' }, S));
  const t = open([], a);
  const id = g.factId(a);
  const upd = one(rec('abit', 'sentenza', '2026-11-11T07:00:00Z'), Object.assign({ tipo: 'rapina', aggiornamento: 'sentenza' }, S));
  const l = g.candidates(upd, t);
  check('T-B-R1-17 an update attaches to its fact months after, as aggiornamento', g.decide(upd, l, judge(l, { [id]: proof }), t, 'esercizio'),
    { azione: 'unisci', content_id: id, ruolo: 'aggiornamento', motivi: [] });
  const other = one(rec('abit', 'sentenza-altra', '2026-11-11T07:00:00Z'), Object.assign({ tipo: 'droga', aggiornamento: 'sentenza' }, S));
  const lo = g.candidates(other, t);
  check('T-B-R1-17 an update of another family is a candidate, never certain', [lo.candidati.length,
    g.decide(other, lo, judge(lo, { [id]: proof }), t, 'esercizio').stato], [1, 'in_dubbio']);
  const fire = one(rec('abit', 'sentenza-fuoco', '2026-11-11T07:00:00Z'), { tipo: 'incendio', aggiornamento: 'sentenza' });
  const lf = g.candidates(fire, t);
  check('T-B-R1-17 an update that does not find its fact opens it in doubt', g.decide(fire, lf, judge(lf, {}), t, 'esercizio'),
    { azione: 'apri', stato: 'in_dubbio', motivi: [{ content_id: null, motivo: 'aggiornamento_senza_fatto' }] });
  check('T-B-R1-17 …also with no candidate at all', g.decide(fire, g.candidates(fire, []), null, [], 'esercizio').motivi[0].motivo, 'aggiornamento_senza_fatto');
  const dated = one(rec('abit', 'convalida', '2026-11-11T07:00:00Z'), Object.assign({ tipo: 'rapina', aggiornamento: 'convalida', data_fatto: '2026-11-01' }, S));
  const ld = g.candidates(dated, t);
  check('T-B-R1-17 an update that gives the day of its fact counts the window', g.decide(dated, ld, judge(ld, { [id]: proof }), t, 'esercizio').stato, 'in_dubbio');
  // The cited scheda comes after the update: not in place.
  const later = one(rec('faro', 'dopo', '2026-11-20T07:00:00Z'), Object.assign({ tipo: 'rapina' }, S));
  const tl = open([], later);
  const early = one(rec('abit', 'prima', '2026-11-11T07:00:00Z'), Object.assign({ tipo: 'rapina', aggiornamento: 'indagini' }, S));
  const le = g.candidates(early, tl);
  check('T-B-R1-17 an update before its cited scheda is not in place', g.decide(early, le, judge(le, { [g.factId(later)]: proof }), tl, 'esercizio').stato,
    'in_dubbio');
  // The cited scheda is an update without the day of its fact.
  const tu = open([], one(rec('faro', 'agg-vecchio', '2026-10-01T07:00:00Z'), Object.assign({ tipo: 'rapina', aggiornamento: 'convalida' }, S)));
  check('T-B-R1-17 a cited update without the day of its fact is never in place', g.datesInPlace(upd, tu[0].schede[0]), false);
}

/* ----- T-B-R1-18 releases without the day of the fact ---------------------------- */

console.log('T-B-R1-18 releases without the day of the fact');
{
  const S = { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] };
  const proof = { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] };
  const a = one(rec('faro', 'a', '2026-10-01T07:00:00Z'), Object.assign({ data_fatto: '2026-09-30' }, S));
  const t = open([], a);
  const late = one(rec('quest', 'tardi', '2026-11-11T07:00:00Z'), S);
  const l = g.candidates(late, t);
  check('T-B-R1-18 a release without the day of its fact, more than 7 days after: found, but in doubt',
    [l.candidati.length, g.decide(late, l, judge(l, { [g.factId(a)]: proof }), t, 'esercizio').stato], [1, 'in_dubbio']);
  const near = one(rec('quest', 'vicino', '2026-10-03T07:00:00Z'), S);
  const ln = g.candidates(near, t);
  check('T-B-R1-18 …within 7 days of the day of the fact it is certain', g.decide(near, ln, judge(ln, { [g.factId(a)]: proof }), t, 'esercizio').azione, 'unisci');
}

/* ----- T-B-R1-19 a run: order, ids, resumption ---------------------------------- */

console.log('T-B-R1-19 a run: the reading order, stable ids, resumption');
{
  const F1 = '20261111T080000Z';
  const F2 = '20261111T090000Z';
  const S = { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] };
  const recs = [
    rec('abit', 'secondo', '2026-11-11T08:30:00Z', '2026-11-11T09:00:05Z', F2, 0),
    rec('quest', 'primo', '2026-11-11T07:30:00Z', '2026-11-11T08:00:05Z', F1, 0),
    rec('faro', 'terzo', '2026-11-11T08:40:00Z', '2026-11-11T09:00:05Z', F2, 1),
  ];
  const [r2, r1, r3] = recs;
  const answers = {
    [r1.record_id]: { risposta: { schede: [Object.assign({}, BASE, S, { data_fatto: '2026-11-10' }), Object.assign({}, BASE, { tipo: 'incendio' })] } },
    [r2.record_id]: { risposta: { schede: [Object.assign({}, BASE, S)] } },
    [r3.record_id]: { risposta: { schede: [Object.assign({}, BASE, { ambito: 'non_cronaca', tipo: null })] } },
  };
  const first = g.placeAll({ records: recs, schede: { [r2.record_id]: answers[r2.record_id] }, giudizi: {}, facts: [], now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 nothing takes its place before the first record without schede', [first.posti.length, first.facts.length], [0, 0]);
  check('T-B-R1-19 …the requests follow the reading order', first.richieste_schede, [r1.record_id, r3.record_id]);
  check('T-B-R1-19 …and the bookmark is the oldest file with pending work', first.segnalibro, F1);

  const second = g.placeAll({ records: recs, schede: answers, giudizi: {}, facts: [], now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 the two facts of the first record open, then a judgment is asked for the second',
    [second.posti.map((p) => p.content_id), second.richiesta_giudizio.scheda_id],
    [[`${identity.newsIdentity({ opening_url: r1.url, fact_index: 1 }).content_id}`, `${identity.newsIdentity({ opening_url: r1.url, fact_index: 2 }).content_id}`],
      `${r2.record_id}#1`]);
  check('T-B-R1-19 …the bookmark moves to the file that waits', second.segnalibro, F2);

  const req = second.richiesta_giudizio;
  const fid = req.lista.candidati[0].content_id;
  const giudizi = { [req.scheda_id]: { lista: req.lista_key, risposta: { giudizi: [{ content_id: fid, verdetto: 'stesso',
    prove: { scheda_id: req.lista.candidati[0].mostrate[0].scheda_id, luogo: 'Via X', dettagli: [ETA(30), PERS(1)] } }] } } };
  const done = g.placeAll({ records: recs, schede: answers, giudizi, facts: second.facts, now: '2026-11-15T11:00:00Z', regola: 'esercizio' });
  check('T-B-R1-19 with the judgment saved the scheda joins its fact', done.posti.map((p) => [p.azione, p.content_id]), [['unisci', fid]]);
  check('T-B-R1-19 a scheda that is not cronaca takes no place and is not pending', [done.segnalibro, done.richieste_schede], [null, []]);

  const clean = g.placeAll({ records: recs, schede: answers, giudizi, facts: [], now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 a run with every answer saved gives the same facts as the interrupted one',
    clean.facts, done.facts);
  const again = g.placeAll({ records: recs, schede: answers, giudizi, facts: done.facts, now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 run again on the same records: no request, the same facts', [again.posti.length, again.richiesta_giudizio, JSON.stringify(again.facts) ===
    JSON.stringify(done.facts)], [0, null, true]);

  // A stopped record holds no one; restarted by hand it takes its place out of order.
  const stopped = g.placeAll({ records: recs, schede: Object.assign({}, answers, { [r1.record_id]: { fermo: true, motivo: 'schede_mancate' } }), giudizi: {},
    facts: [], now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 a stopped record does not hold the others', [stopped.fermi.map((x) => x.motivo), stopped.posti.map((p) => p.scheda_id)],
    [['schede_mancate'], [`${r2.record_id}#1`]]);
  const restarted = Object.assign({}, r1, { ripartito: true });
  const back = g.placeAll({ records: [r2, restarted, r3], schede: answers, giudizi: {}, facts: stopped.facts, now: NOW, regola: 'esercizio' });
  const r2Fact = identity.newsIdentity({ opening_url: r2.url }).content_id;
  check('T-B-R1-19 restarted, it is asked about the fact a later record opened',
    [back.richiesta_giudizio.scheda_id, back.richiesta_giudizio.lista.candidati.map((c) => c.content_id)], [`${r1.record_id}#1`, [r2Fact]]);
  const rq = back.richiesta_giudizio;
  const joined = g.placeAll({ records: [r2, restarted, r3], schede: answers, giudizi: { [rq.scheda_id]: { lista: rq.lista_key, risposta: { giudizi: [
    { content_id: r2Fact, verdetto: 'stesso', prove: { scheda_id: `${r2.record_id}#1`, luogo: 'Via X', dettagli: [ETA(30), PERS(1)] } }] } } },
    facts: stopped.facts, now: NOW, regola: 'esercizio' });
  const kept = joined.facts.find((f) => f.content_id === r2Fact);
  check('T-B-R1-19 …joins it, and the fact keeps the id it was given by the later record',
    [kept.schede.map((t) => [t.scheda_id, t.ruolo]), joined.facts.some((f) => f.content_id === g.factId(back.richiesta_giudizio.scheda))],
    [[[`${r2.record_id}#1`, 'apre'], [`${r1.record_id}#1`, 'stesso_fatto']], false]);

  // A saved judgment counts only for the same list: a candidate whose shown schede changed asks again.
  const changed = second.facts.map((f) => (f.content_id === fid ? Object.assign({}, f, { schede: [...f.schede,
    Object.assign({}, f.schede[0], { scheda_id: 'https://altro.it/x#1', record_id: 'https://altro.it/x', ruolo: 'stesso_fatto' })] }) : f));
  const asked = g.placeAll({ records: recs, schede: answers, giudizi, facts: changed, now: NOW, regola: 'esercizio' });
  check('T-B-R1-19 a list whose shown schede changed is not the same list', [asked.posti.length, asked.richiesta_giudizio.scheda_id], [0, `${r2.record_id}#1`]);
  check('T-B-R1-19 a saved answer out of form is a fault, never placed', thrown(() => g.placeAll({ records: [r1], schede: { [r1.record_id]: { risposta: { schede: [] } } },
    giudizi: {}, facts: [], now: NOW, regola: 'esercizio' })), `saved_schede_invalid: ${r1.record_id} nessuna_scheda`);
  check('T-B-R1-19 an identity already given is never given again', thrown(() => g.applyDecision(done.facts, done.facts[0].schede[0],
    { azione: 'apri', stato: 'aperto', motivi: [] }, NOW, 'esercizio')), `content_id_taken: ${done.facts[0].content_id}`);
}

/* ----- T-B-R1-20 answers that do not come ---------------------------------------- */

console.log('T-B-R1-20 answers that do not come');
check('T-B-R1-20 the first two misses retry, the third stops', [g.missedAnswer(0).esito, g.missedAnswer(1).esito, g.missedAnswer(2)],
  ['riprova', 'riprova', { tentativi: 3, esito: 'ferma' }]);
check('T-B-R1-20 five misses in a row stop steps 2 and 4', [g.stepsHalted(4), g.stepsHalted(5)], [false, true]);
{
  const a = one(rec('faro', 'a', '2026-11-10T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const t = open([], a);
  const s = one(rec('abit', 'b', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')] });
  const l = g.candidates(s, t);
  check('T-B-R1-20 a judgment missed three times sends the scheda in doubt', g.decide(s, l, { mancato: true }, t, 'esercizio').motivi,
    [{ content_id: g.factId(a), motivo: 'risposta' }]);
  const run = g.placeAll({ records: [rec('abit', 'b', '2026-11-11T07:00:00Z')], schede: { [s.record_id]: { risposta: { schede: [Object.assign({}, BASE, { luoghi: [VIA('Via X')] })] } } },
    giudizi: { [s.scheda_id]: { lista: g.listKey(l), mancato: true } }, facts: t, now: NOW, regola: 'esercizio' });
  check('T-B-R1-20 …also in a run', run.posti.map((p) => [p.stato, p.motivi[0].motivo]), [['in_dubbio', 'risposta']]);
}

/* ----- T-B-R1-21 on top of news-fact.js -------------------------------------------- */

console.log('T-B-R1-21 publication and the day\'s doubts (owner choice 3(b))');
{
  const a = one(rec('quest', 'a', '2026-11-10T07:00:00Z'), {});
  const t = open([], a);
  const pub = factNode.factSources(g.factRecords(t[0]));
  check('T-B-R1-21 an open official fact may be published', g.groupingAllows(t[0], pub), { pubblicabile: true, motivo: null });
  check('T-B-R1-21 a fact in doubt never', g.groupingAllows(Object.assign({}, t[0], { stato: 'in_dubbio' }), pub).motivo, 'in_dubbio');
  check('T-B-R1-21 a merged fact never', g.groupingAllows(Object.assign({}, t[0], { stato: 'unito' }), pub).motivo, 'unito');
  check('T-B-R1-21 a fact of the comparison rule never', g.groupingAllows(Object.assign({}, t[0], { regola: 'confronto' }), pub).motivo, 'regola_confronto');
  const press = open([], one(rec('faro', 'b', '2026-11-10T07:00:00Z'), {}));
  check('T-B-R1-21 a press fact of one source: what news-fact.js says', g.groupingAllows(press[0], factNode.factSources(g.factRecords(press[0]))).motivo, 'fonti');
  const d1 = g.applyDecision([], one(rec('abit', 'c', '2026-11-10T07:00:00Z'), {}), { azione: 'apri', stato: 'in_dubbio',
    motivi: [{ content_id: null, motivo: 'lista_tagliata' }] }, '2026-11-15T22:30:00Z', 'esercizio');
  const d2 = g.applyDecision(d1, one(rec('abit', 'd', '2026-11-10T07:00:00Z'), {}), { azione: 'apri', stato: 'in_dubbio',
    motivi: [{ content_id: null, motivo: 'forse' }] }, '2026-11-15T23:30:00Z', 'confronto');
  const list = g.doubtsOfDay(d2.concat(t), '2026-11-15');
  check('T-B-R1-21 the day\'s doubts: the day of Rome, the rule in use, no texts', [list.length, Object.keys(list[0])],
    [1, ['content_id', 'aperto_il', 'motivi', 'candidati', 'record']]);
  check('T-B-R1-21 …a doubt of 23:30 UTC is of the next day in Rome', g.doubtsOfDay(d1, '2026-11-15').length + g.doubtsOfDay(d1, '2026-11-16').length, 1);
  check('T-B-R1-21 the counts for the report', g.counts(d2), { fatti: 2, schede: 2, stati: { in_dubbio: 2 }, motivi: { lista_tagliata: 1, forse: 1 }, ruoli: { apre: 2 } });
}

/* ----- T-B-R1-29 more of section 8, point 1: the place -------------------------- */

console.log('T-B-R1-29 more of section 8, point 1: the place');
{
  let full = [];
  for (let i = 0; i < 11; i += 1) full = open(full, one(rec('abit', `pieno-${String(i).padStart(2, '0')}`, '2026-11-10T07:00:00Z'), {}));
  const release = one(rec('quest', 'comunicato', '2026-11-11T07:00:00Z'), {});
  const lr = g.candidates(release, full);
  check('T-B-R1-29 a release without the day of its fact, with a cut list, all diverso: doubt, lista_tagliata',
    g.decide(release, lr, judge(lr, {}), full, 'esercizio').motivi, [{ content_id: null, motivo: 'lista_tagliata' }]);
  const id0 = lr.candidati[0].content_id;
  check('T-B-R1-29 …a forse among the ten is a doubt about it, not about the cut',
    g.decide(release, lr, judge(lr, { [id0]: { verdetto: 'forse' } }), full, 'esercizio').motivi, [{ content_id: id0, motivo: 'forse' }]);
  const cited = one(rec('quest', 'citata', null, '2026-11-10T08:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] });
  const tc = open([], cited);
  const incoming = one(rec('faro', 'arriva', '2026-11-11T07:00:00Z'), { luoghi: [VIA('Via X')], dettagli: [ETA(30), PERS(1)] });
  const lc = g.candidates(incoming, tc);
  check('T-B-R1-29 a scheda citing one dated only by retrieved_at is never certain',
    g.decide(incoming, lc, judge(lc, { [g.factId(cited)]: { verdetto: 'stesso', luogo: 'Via X', dettagli: [ETA(30), PERS(1)] } }), tc, 'esercizio').stato, 'in_dubbio');
}

/* ----- T-B-R1-30 the two rules and the order of writing --------------------------- */

console.log('T-B-R1-30 the two rules of the trial, the order of writing');
{
  // The two rules of the trial ask one scheda about different lists: both judgments are kept.
  const F = '20261111T080000Z';
  const S = { luoghi: [VIA('Via X'), Q('Quartiere Y')], dettagli: [ETA(30), PERS(1)] };
  const r1 = rec('faro', 'uno', '2026-11-11T07:00:00Z', null, F, 0);
  const r2 = rec('abit', 'due', '2026-11-11T07:10:00Z', null, F, 1);
  const r3 = rec('abit', 'tre', '2026-11-11T07:20:00Z', null, F, 2);
  const answers = {
    [r1.record_id]: { risposta: { schede: [Object.assign({}, BASE, S)] } },
    [r2.record_id]: { risposta: { schede: [Object.assign({}, BASE, { luoghi: [Q('Quartiere Y')] })] } },
    [r3.record_id]: { risposta: { schede: [Object.assign({}, BASE, S)] } },
  };
  const recs = [r1, r2, r3];
  // The model cites what the two schede share: the street when there is one, else the quarter.
  const answer = (req) => ({ lista: req.lista_key, risposta: { giudizi: req.lista.candidati.map((c) => {
    const t = c.mostrate[0];
    const street = g.sharedPlaces(req.scheda, t, ['via']).length > 0;
    return { content_id: c.content_id, verdetto: 'stesso', prove: { scheda_id: t.scheda_id, luogo: street ? 'Via X' : 'Quartiere Y',
      dettagli: street ? [ETA(30), PERS(1)] : [] } };
  }) } });
  const replay = (rule, saved) => {
    let facts = [];
    const giudizi = Object.assign({}, saved);
    let calls = 0;
    for (let i = 0; i < 10; i += 1) {
      const res = g.placeAll({ records: recs, schede: answers, giudizi, facts, now: NOW, regola: rule });
      facts = res.facts;
      if (!res.richiesta_giudizio) return { facts, calls, giudizi };
      calls += 1;
      const id = res.richiesta_giudizio.scheda_id;
      giudizi[id] = [].concat(giudizi[id] || [], [answer(res.richiesta_giudizio)]);
    }
    throw new Error('replay did not end');
  };
  // A replay is a later run: its facts are the same, written at the instants of that run.
  const sansTime = (facts) => facts.map((f) => Object.assign({}, f, { aperto_il: null }));
  const first = replay('esercizio', {});
  const both = replay('confronto', first.giudizi);
  const again = replay('esercizio', both.giudizi);
  const againWide = replay('confronto', both.giudizi);
  check('T-B-R1-30 the two rules give different facts on the same records: the quarter merges only with the comparison rule',
    [first.facts.map((f) => f.stato), both.facts.map((f) => f.schede.length)], [['aperto', 'in_dubbio', 'in_dubbio'], [3]]);
  check('T-B-R1-30 the comparison rule reused the judgments whose list is the same', both.calls, 1);
  check('T-B-R1-30 a replay of either rule after both makes no call and gives the same facts',
    [again.calls, againWide.calls, JSON.stringify(sansTime(again.facts)) === JSON.stringify(sansTime(first.facts)),
      JSON.stringify(sansTime(againWide.facts)) === JSON.stringify(sansTime(both.facts))],
    [0, 0, true, true]);
  check('T-B-R1-30 the facts of the comparison rule say so, and are never published',
    [both.facts.every((f) => f.regola === 'confronto'), g.groupingAllows(both.facts[0], { pubblicabile: true }).motivo], [true, 'regola_confronto']);
  const oneRun = g.placeAll({ records: recs, schede: answers, giudizi: again.giudizi, facts: [], now: NOW, regola: 'esercizio' });
  const written = [...first.facts, ...both.facts];
  check('T-B-R1-30 every state, role and motive written is in its list', [
    written.every((f) => g.STATI.includes(f.stato)),
    written.every((f) => f.schede.every((t) => g.RUOLI.includes(t.ruolo))),
    written.every((f) => !f.dubbio || f.dubbio.motivi.every((m) => g.MOTIVI.includes(m.motivo)))], [true, true, true]);
  check('T-B-R1-30 facts opened in one run are older in reading order', oneRun.facts.map((f) => f.aperto_il),
    ['2026-11-15T10:00:00.000Z', '2026-11-15T10:00:00.001Z', '2026-11-15T10:00:00.002Z']);
}


/* ----- T-B-R1-28 the stages of the run in the adapter ---------------------------- */

console.log('T-B-R1-28 the stages place, publication and doubts of the n8n adapter');
{
  const r = rec('quest', 'a', '2026-11-10T07:00:00Z');
  const place = adapter({ stage: 'place', records: [r], schede: { [r.record_id]: { risposta: { schede: [BASE] } } }, giudizi: {}, facts: [], now: NOW,
    regola: 'esercizio' }).item;
  check('T-B-R1-28 the place stage', place.json.result.posti.length, 1);
  const t = place.json.result.facts;
  check('T-B-R1-28 publication', adapter({ stage: 'publication', fact: t[0], pubblicazione: { pubblicabile: true } }).item.json.raggruppamento,
    { pubblicabile: true, motivo: null });
  check('T-B-R1-28 doubts', adapter({ stage: 'doubts', facts: t, day: '2026-11-15' }).item.json.dubbi, []);
}

console.log(failures ? `\n${failures} FAILED of ${checks}` : `\nALL PASS (${checks} checks)`);
process.exit(failures ? 1 : 0);
