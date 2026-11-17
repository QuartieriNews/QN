#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-group.js, part B-R1a: step 1 and the check of the
 * model's schede (docs/pilota/B_RAGGRUPPAMENTO.md, sections 2, 3 and 6; section 8, point 1, lists
 * what this file must cover by the end of B-R1), the copies kept equal to news-identity.js,
 * news-fact.js and news-collect.js, and the n8n adapter evaluated from the exact committed file
 * with stubbed $input/$json. Every URL,
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

console.log(failures ? `\n${failures} FAILED of ${checks}` : `\nALL PASS (${checks} checks)`);
process.exit(failures ? 1 : 0);
