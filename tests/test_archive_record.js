#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/archive-record.js: the form of `archive_id`, the
 * values of `tipo`, idempotency and normalization (docs/pilota/CONTRATTI.md, «Lo
 * storico»), the perimeter of DEC-033 rule 1, Rome days (Spec v2.5 T17), and the n8n
 * adapter evaluated from the exact committed file with stubbed $input/$json/require.
 * Every row is invented (DEC-109) except the PDF link of the source study, which is
 * already in docs/sources/SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md.
 *
 * Run:  node tests/test_archive_record.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'archive-record.js');
const m = require(FILE);

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

function row(overrides) {
  return Object.assign({
    tipologia: 'CMD', idDoc: 4242, dtRpr: '2026-03-10', dtSeduta: null,
    dscStrOrg: 'Municipio Roma X - Ufficio inventato',
  }, overrides || {});
}

const SHA_A = 'a'.repeat(64);
const SHA_B = 'b'.repeat(64);
const DL = { sha256: SHA_A, retrieved_at: '2026-11-10T09:00:00Z', workflow: 'staging_D_attiweb_read', workflow_version: '1',
  elenco: 'originali/attiweb_elenco_2026-11-10_CMD_0.json' };

console.log('archive_id: form and identity (CONTRATTI «Lo storico»)');
check('form: prefix, source_id, tipologia, idDoc', m.archiveId('CMD', '4242'), 'qn:roma:arc:comune.roma.it:CMD:4242');
check('a JSON number and its decimal string are one key', m.archiveId('CMD', 4242), m.archiveId('CMD', '4242'));
check('spaces at the edges are dropped', m.archiveId(' CMD ', ' 4242\t'), 'qn:roma:arc:comune.roma.it:CMD:4242');
check('a no-break space counts as a space', m.archiveId('CMD ', ' 4242'), 'qn:roma:arc:comune.roma.it:CMD:4242');
check('the same idDoc under another tipologia is another document', m.archiveId('GMD', '4242') !== m.archiveId('CMD', '4242'), true);
check('geography takes no part: the same row under another Municipio keeps its id',
  m.describeRow(row({ dscStrOrg: 'Municipio Roma V' }), '2026-11-10').archive_id,
  m.describeRow(row(), '2026-11-10').archive_id);
check('describing the same row twice gives the same result (idempotent)',
  m.describeRow(row(), '2026-11-10'), m.describeRow(JSON.parse(JSON.stringify(row())), '2026-11-10'));
check('a tipologia outside tipo stops the run', /is not a value of tipo/.test(thrown(() => m.archiveId('ZZZ', '1')) || ''), true);
check('a central tipologia is a tipo too: municipal structures file acts there (DEC-033)', m.archiveId('ACD', '1'), 'qn:roma:arc:comune.roma.it:ACD:1');
check('tipo values are the 48 of the portal menu', [m.TIPI.length, new Set(m.TIPI).size], [48, 48]);
check('tipo values match the table of the source study, section 3', (() => {
  const sec = fs.readFileSync(path.join(__dirname, '..', 'docs', 'sources', 'A2_ATTIWEB_TIPOLOGIE.md'), 'utf8').split('## 3.')[1].split('## 4.')[0];
  return [...sec.matchAll(/^\| *([A-Z][A-Z0-9]{1,4}) *\|/gm)].map((x) => x[1]).sort();
})(), [...m.TIPI].sort());
check('the menu read at the start gives the order of the reading', m.planTipologie([...m.TIPI].reverse().concat(' CMC ')), [...m.TIPI]);
check('a menu without a known tipologia stops the reading: it would not be complete',
  /menu without known tipologie: DDS/.test(thrown(() => m.planTipologie(m.TIPI.filter((c) => c !== 'DDS'))) || ''), true);
check('a menu that did not read stops the reading before it starts', /does not start/.test(thrown(() => m.planTipologie([])) || ''), true);
check('a menu that is not a list stops it too', /does not start/.test(thrown(() => m.planTipologie(null)) || ''), true);
check('a new code in the menu stops the reading until a PR adds it', /not in tipo: NEW/.test(thrown(() => m.planTipologie([...m.TIPI, 'NEW'])) || ''), true);
check('an idDoc with a delimiter never becomes an id', /numeric key/.test(thrown(() => m.archiveId('CMD', '12:3')) || ''), true);
check('an idDoc that is not a number never becomes an id', /numeric key/.test(thrown(() => m.archiveId('CMD', '12a')) || ''), true);
check('an empty idDoc never becomes an id', /numeric key/.test(thrown(() => m.archiveId('CMD', '  ')) || ''), true);
check('a fractional number is not a key', /numeric key/.test(thrown(() => m.archiveId('CMD', 12.5)) || ''), true);
check('file stem', m.fileStem('qn:roma:arc:comune.roma.it:CMD:4242'), 'roma__arc__comune.roma.it__CMD__4242');
check('the PDF link is the one the source study read (CMD, 10165)', m.pdfUrl('CMD', 10165),
  'https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/showPdfDoc?fun=deliberazioniAtti&par1=Q01E&par2=MTAxNjU=');

console.log('passes over a tipologia, DEC-033 rule 1 (late publication)');
{
  const p = (total, ids) => ({ total, rows: ids.map((idDoc) => ({ idDoc })) });
  check('one pass is never enough', [m.mergePasses([p(2, [1, 2])]).complete, m.mergePasses([p(2, [1, 2])]).needs_another_pass], [false, true]);
  check('two equal passes complete the tipologia', m.mergePasses([p(2, [1, 2]), p(2, [2, 1])]).complete, true);
  check('a late act changes the total: another pass', m.mergePasses([p(2, [1, 2]), p(3, [1, 2, 3])]).needs_another_pass, true);
  check('the same total with another set of idDoc is not stable', m.mergePasses([p(2, [1, 2]), p(2, [1, 3])]).complete, false);
  const three = m.mergePasses([p(2, [1, 2]), p(3, [1, 2, 3]), p(4, [1, 2, 3, 4])]);
  check('three passes still moving: incomplete, no fourth pass', [three.complete, three.needs_another_pass], [false, false]);
  check('rows of all passes are kept once each, by idDoc', three.rows.map((r) => r.idDoc).sort(), [1, 2, 3, 4]);
  const truncated = { total: 600, rows: Array.from({ length: 500 }, (_, i) => ({ idDoc: i + 1 })) };
  check('two equal passes that hold fewer rows than declared are not complete', m.mergePasses([truncated, truncated]).complete, false);
  check('a pass with a malformed idDoc is not whole', m.mergePasses([p(2, [1, 'x']), p(2, [1, 'x'])]).complete, false);
  const empty = (historical_total) => ({ total: 0, rows: [], historical_total });
  check('two empty passes of a tipologia with acts in the historical interval: empty and complete',
    m.mergePasses([empty(226), empty(226)]).complete, true);
  const xmo = m.mergePasses([empty(0)]);
  check('an empty response with no acts in the historical interval is missing data: incomplete, no other pass',
    [xmo.complete, xmo.needs_another_pass], [false, false]);
  check('nor does a later pass make it complete', m.mergePasses([empty(0), empty(5), empty(5)]).complete, false);
  check('an empty pass without the historical check is a workflow error',
    /historical_total/.test(thrown(() => m.mergePasses([p(0, []), p(0, [])])) || ''), true);
  const extra = { total: 1, rows: [{ idDoc: 1 }, { idDoc: 'bad' }] };
  check('a pass with a malformed row besides the declared ones is not whole', m.mergePasses([extra, extra]).complete, false);
  const oddEmpty = { total: 0, rows: [{ idDoc: 'bad' }], historical_total: 5 };
  check('nor is an empty pass that holds an unreadable row', m.mergePasses([oddEmpty, oddEmpty]).complete, false);
  const twice = { total: 2, rows: [{ idDoc: 1 }, { idDoc: 1 }, { idDoc: 2 }] };
  check('nor one with a repeated idDoc', m.mergePasses([twice, twice]).complete, false);
  check('more than three passes is a workflow error', /one to three passes/.test(thrown(() => m.mergePasses([p(1, [1]), p(1, [1]), p(1, [1]), p(1, [1])])) || ''), true);
}

console.log('dates: a day as written, an instant as its Rome day (T17)');
check('ISO day', m.sourceDay('2026-03-10', 'f'), '2026-03-10');
check('Italian day', m.sourceDay('10/03/2026', 'f'), '2026-03-10');
check('Italian day with one-digit parts', m.sourceDay('1/3/2026', 'f'), '2026-03-01');
check('local date-time without offset keeps its day', m.sourceDay('2026-03-10T23:30:00', 'f'), '2026-03-10');
check('a UTC instant late in the evening is the next Rome day', m.sourceDay('2026-03-10T23:30:00Z', 'f'), '2026-03-11');
check('an offset without a colon is read', m.sourceDay('2026-10-24T22:30:00+0000', 'f'), '2026-10-25');
check('epoch milliseconds are an instant', m.sourceDay(Date.parse('2026-06-30T22:15:00Z'), 'f'), '2026-07-01');
check('empty is null', [m.sourceDay('', 'f'), m.sourceDay(null, 'f'), m.sourceDay('  ', 'f')], [null, null, null]);
check('31 February stops the run naming the field', /dtRpr: unreadable date/.test(thrown(() => m.sourceDay('31/02/2026', 'dtRpr')) || ''), true);
check('month 13 stops the run', thrown(() => m.sourceDay('2026-13-01', 'f')) !== null, true);
check('hour 24 stops the run', thrown(() => m.sourceDay('2026-03-10T24:00:00', 'f')) !== null, true);
check('a word stops the run', thrown(() => m.sourceDay('ieri', 'f')) !== null, true);
check('a small number is not epoch milliseconds', thrown(() => m.sourceDay(20260310, 'f')) !== null, true);
check('data_documento: dtSeduta when there is one', m.dataDocumento(row({ dtSeduta: '2026-03-20' })), { day: '2026-03-20', from: 'dtSeduta' });
check('data_documento: dtRpr otherwise', m.dataDocumento(row()), { day: '2026-03-10', from: 'dtRpr' });
check('a row without dtRpr stops the run', /dtRpr missing/.test(thrown(() => m.dataDocumento(row({ dtRpr: null }))) || ''), true);

console.log('Municipio from dscStrOrg');
check('Municipio Roma X', m.municipalityCode('Municipio Roma X - Ufficio inventato'), 'X');
check('MUNICIPIO V', m.municipalityCode('MUNICIPIO V'), 'V');
check('Municipio Roma I Centro', m.municipalityCode('Municipio Roma I Centro'), 'I');
check('IX is not I', m.municipalityCode('Municipio Roma IX'), 'IX');
check('XV is read whole', m.municipalityCode('Municipio Roma XV'), 'XV');
check('two different Municipi: none', m.municipalityCode('Municipio Roma I e Municipio Roma II'), null);
check('no Municipio: none', m.municipalityCode('Dipartimento inventato'), null);
check('a roman number outside I-XV: none', m.municipalityCode('Municipio XL'), null);
check('the short form of the source study: MUNIC. ROMA X', m.municipalityCode('MUNIC. ROMA X - Ufficio inventato'), 'X');
check('MUNICIPIO without ROMA', m.municipalityCode('MUNICIPIO X DIREZIONE INVENTATA'), 'X');
check('a word after ROMA is not a numeral', m.municipalityCode('Municipio Roma Via Inventata'), null);
check('the former Municipio in brackets is not a second issuer', m.municipalityCode('MUNICIPIO ROMA X (EX MUNICIPIO XIII)'), 'X');
check('nor when the former one is a Municipio of the pilot', m.municipalityCode('Municipio Roma IV (ex Municipio V)'), 'IV');
check('a Polizia Locale group is not a Municipio structure', m.municipalityCode('P.L. - X GRUPPO MARE'), null);
check('and its rows are left out with their own reason', m.describeRow(row({ tipologia: 'DDS', dscStrOrg: 'P.L. - X GRUPPO MARE' }), '2026-11-10').reason, 'polizia_locale');

console.log('perimeter, DEC-033 rule 1');
const today = '2026-11-10';
check('a row of Municipio X in the period is kept', m.describeRow(row(), today).keep, true);
check('another Municipio is left out', m.describeRow(row({ dscStrOrg: 'Municipio Roma IX' }), today).reason, 'fuori_dai_municipi');
check('an unreadable Municipio is left out and named', m.describeRow(row({ dscStrOrg: 'Ufficio inventato' }), today).reason, 'municipio_non_letto');
check('December 2025 is before the period', m.describeRow(row({ dtRpr: '2025-12-15' }), today).reason, 'prima_del_periodo');
check('1 January 2026 is in', m.describeRow(row({ dtRpr: '2026-01-01' }), today).keep, true);
check('a December convocation for a January sitting is in',
  m.describeRow(row({ tipologia: 'CMC', dtRpr: '2025-12-22', dtSeduta: '2026-01-08' }), today).keep, true);
check('the reading day itself is in', m.describeRow(row({ dtRpr: today }), today).keep, true);
check('a convocation for a sitting after the reading day waits', m.describeRow(row({ tipologia: 'CMC', dtRpr: '2026-11-09', dtSeduta: '2026-11-19' }), today).reason, 'data_futura');
check('the record keeps which field gave the date', m.describeRow(row({ tipologia: 'CMC', dtSeduta: '2026-03-12' }), today).data_documento_da, 'dtSeduta');
check('a malformed reading day stops the run', /reading_day/.test(thrown(() => m.describeRow(row(), '2026-02-30')) || ''), true);

console.log('records: versions, same original, no overwrite (CONTRATTI «Lo storico»)');
const arc = m.describeRow(row(), today);
const r1 = m.archiveRecord(arc, DL, []);
check('first reading: version 1', r1.versione, 1);
check('first reading: no motivo', 'motivo' in r1, false);
check('the original sits in originali/ under the stem and the hash', r1.originale, `originali/roma__arc__comune.roma.it__CMD__4242__${'a'.repeat(16)}.pdf`);
check('a record has neither block nor content_id', ['block' in r1, 'content_id' in r1], [false, false]);
check('the record carries the canonical Municipio and tipo', [r1.municipality_code, r1.tipo, r1.source_id], ['X', 'CMD', 'comune.roma.it']);
check('record file name', m.recordFileName(r1), 'roma__arc__comune.roma.it__CMD__4242__v1.json');
check('the same original read again adds no row', m.archiveRecord(arc, DL, [r1]), null);
const r2 = m.archiveRecord(arc, Object.assign({}, DL, { sha256: SHA_B }), [r1]);
check('a changed original is version 2 with a motivo', [r2.versione, r2.motivo], [2, 'originale cambiato alla fonte']);
check('the latest version decides, in any order', m.archiveRecord(arc, DL, [r2, r1]).versione, 3);
check('the same original as the latest version adds no row', m.archiveRecord(arc, Object.assign({}, DL, { sha256: SHA_B }), [r1, r2]), null);
check('a correction with the same original is the latest version: no row',
  m.archiveRecord(arc, Object.assign({}, DL, { sha256: SHA_B }), [r1, r2, Object.assign({}, r2, { versione: 3, motivo: 'correzione' })]), null);
check('a row left out never becomes a record', /only a kept row/.test(thrown(() => m.archiveRecord(m.describeRow(row({ dtRpr: '2025-12-15' }), today), DL, [])) || ''), true);
check('a hash that is not SHA-256 stops the run', /sha256/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { sha256: 'abc' }), [])) || ''), true);
check('30 February is not a retrieval time', /retrieved_at/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { retrieved_at: '2026-02-30T09:00:00Z' }), [])) || ''), true);
check('nor is hour 25', /retrieved_at/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { retrieved_at: '2026-11-10T25:00:00Z' }), [])) || ''), true);
check('a non-UTC retrieved_at stops the run', /retrieved_at/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { retrieved_at: '2026-11-10 10:00' }), [])) || ''), true);
check('only a staging_ workflow writes records', /staging_/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { workflow: 'D_attiweb_read' }), [])) || ''), true);
check('a record without the workflow version is not written', /workflow_version/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { workflow_version: undefined }), [])) || ''), true);
check('nor with an empty one', /workflow_version/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { workflow_version: '  ' }), [])) || ''), true);
check('existing versions of another id stop the run', /another archive_id/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { archive_id: 'qn:roma:arc:comune.roma.it:CMD:1' })])) || ''), true);

check('existing left out stops the run instead of writing a second v1', /existing must list/.test(thrown(() => m.archiveRecord(arc, DL, undefined)) || ''), true);
check('a repeated versione is found in any order', /two existing records with versione 1/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { versione: 2, originale_sha256: SHA_B }), r1, r1])) || ''), true);
check('a gap in the existing versions stops the run: the listing is incomplete',
  /not 1 to 3/.test(thrown(() => m.archiveRecord(arc, DL, [r1, Object.assign({}, r1, { versione: 3, originale_sha256: SHA_B })])) || ''), true);
check('so does a history without its v1', /not 1 to 2/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { versione: 2 })])) || ''), true);
check('an existing record without its hash stops the run instead of inventing a change',
  /without a valid originale_sha256/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { originale_sha256: undefined })])) || ''), true);
check('so does a hash that is not 64 lowercase hex digits',
  /without a valid originale_sha256/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { originale_sha256: SHA_A.toUpperCase() })])) || ''), true);
check('nor is a hash wrapped in a list', /without a valid originale_sha256/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { originale_sha256: [SHA_A] })])) || ''), true);
check('and a downloaded hash wrapped in a list stops the run too', /sha256/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { sha256: [SHA_A] }), [])) || ''), true);
check('two existing records with one versione stop the run', /two existing records/.test(thrown(() => m.archiveRecord(arc, DL, [r1, r1])) || ''), true);
check('an existing versione that is not a whole number stops the run', /versione/.test(thrown(() => m.archiveRecord(arc, DL, [Object.assign({}, r1, { versione: '1' })])) || ''), true);
check('the record points at the saved search page its row came from', r1.provenienza.elenco, 'originali/attiweb_elenco_2026-11-10_CMD_0.json');
check('a search page outside originali/ stops the run', /elenco/.test(thrown(() => m.archiveRecord(arc, Object.assign({}, DL, { elenco: 'tmp/x.json' }), [])) || ''), true);

console.log('n8n adapter branch — exact committed file, stubbed $input/$json/require');
const src = fs.readFileSync(FILE, 'utf8');
function runNode(json) {
  const item = { json };
  return new Function('$input', '$json', 'require', src)({ item }, json, require);
}
{
  const out = runNode(Object.assign(row(), { reading_day: today }));
  check('stage 1 adds archive equal to the module result', out.json.archive, m.describeRow(row(), today));
  check('stage 1 leaves the row fields untouched', [out.json.idDoc, out.json.dtRpr], [4242, '2026-03-10']);
  const two = runNode(Object.assign(row(), { reading_day: today, archive: out.json.archive, download: DL, existing: [] }));
  check('stage 2 adds the record', two.json.record, r1);
  check('stage 2 names the record file', two.json.record_file_name, 'roma__arc__comune.roma.it__CMD__4242__v1.json');
  const again = runNode(Object.assign(row(), { reading_day: today, archive: out.json.archive, download: DL, existing: [r1] }));
  check('stage 2 on the same original: record null, no file', [again.json.record, again.json.record_file_name], [null, null]);
}

console.log('the double date of the convocations (dtRpr with the sitting date in brackets)');
check('the first date is the repertorio date', m.sourceDay('01/12/2025<br>(04/12/2025)<br>', 'dtRpr'), '2025-12-01');
check('without the last break too', m.sourceDay('09/03/2026<br>(12/03/2026)', 'dtRpr'), '2026-03-09');
check('a convocation keeps its repertorio day as data_documento',
  m.dataDocumento({ dtRpr: '09/03/2026<br>(12/03/2026)<br>', dtSeduta: null }), { day: '2026-03-09', from: 'dtRpr' });
check('other markup stays unreadable', /unreadable date/.test(thrown(() => m.sourceDay('09/03/2026<br>altro', 'dtRpr')) || ''), true);
check('a bracketed date that is not a date stays unreadable', /unreadable date/.test(thrown(() => m.sourceDay('09/03/2026<br>(ieri)<br>', 'dtRpr')) || ''), true);

console.log('the reading: menu, answers, passes (CONTRATTI «Lo storico», DEC-033 rules 2, 4, 5)');
const DAY = '2026-11-10';
const ok = (body) => ({ statusCode: 200, headers: {}, body: typeof body === 'string' ? body : JSON.stringify(body) });
const STRUTS = '<html><body>Struts Problem Report: Index: 0, Size: 0</body></html>';
const act = (idDoc, extra) => Object.assign({ idDoc, dtRpr: '2026-03-10', dtSeduta: null, dscStrOrg: 'Municipio Roma X - Ufficio inventato' }, extra || {});
const page = (total, ids, extra) => ok({ total, elencoAtti: ids.map((i) => act(i, extra)) });
{
  check('the menu gives its codes, combined ones left out',
    m.menuCodes({ listaTipologie: [{ codice: 'CMD', descrizione: 'inventata' }, { codice: 'CMD,CMC', descrizione: 'inventata' }] }), ['CMD']);
  check('the menu also reads as text', m.menuCodes(JSON.stringify({ x: 1, lista: [{ codice: 'GMD' }] })), ['GMD']);
  check('a menu without a list stops the reading', /did not read/.test(thrown(() => m.menuCodes({ errore: 'x' })) || ''), true);
  check('a menu that is not JSON stops it too', /did not read/.test(thrown(() => m.menuCodes('<html>')) || ''), true);

  check('403 stops the reading', m.blockSignal({ statusCode: 403, body: '' }), 'HTTP 403');
  check('429 stops it', m.blockSignal({ statusCode: 429, body: '' }), 'HTTP 429');
  check('401 stops it', m.blockSignal({ statusCode: 401, body: '' }), 'HTTP 401');
  check('a redirect stops it: the login page is one', m.blockSignal({ statusCode: 302, headers: { location: 'https://x.invalid/login' }, body: '' }),
    'redirect to https://x.invalid/login');
  check('a captcha stops it', m.blockSignal(ok('<div class="g-recaptcha">')), 'captcha');
  check('a password field stops it', m.blockSignal(ok('<form><input type="password" name="p"></form>')), 'login page');
  check('the empty answer is not a block', m.blockSignal({ statusCode: 500, body: STRUTS }), null);
  check('rows are not a block', m.blockSignal(page(1, [1])), null);
  const CHECK = '<html>\n<head></head>\n<body>\n<script type="text/javascript">/* a check of the browser */</script>\n</body>\n</html>';
  check('a 200 HTML page in place of data is a block: a script that checks the browser names no captcha',
    m.htmlInstead(ok(CHECK), 'the answer'), 'an HTML page instead of the answer');
  check('the empty answer is not that block', m.htmlInstead({ statusCode: 200, body: STRUTS }, 'the answer'), null);
  check('an HTML error page is not that block', m.htmlInstead({ statusCode: 500, body: '<html>altro</html>' }, 'the answer'), null);
  check('JSON is not that block', m.htmlInstead(page(1, [1]), 'the answer'), null);

  check('an answer with rows', m.parseSearch(page(2, [1, 2])).kind, 'rows');
  check('the empty answer', m.parseSearch({ statusCode: 500, body: STRUTS }), { kind: 'empty' });
  check('another HTML page is an error', m.parseSearch(ok('<html>altro</html>')).kind, 'error');
  check('JSON without the list is an error', m.parseSearch(ok({ total: 3 })).kind, 'error');

  const RS = '2026-11-10T20:15:00Z'; // the start of the reading, in the names of its pages
  const one = m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(2, [1, 2])] });
  check('one page: a whole pass', [one.needs_historical, one.pass_result.total, one.pass_result.rows.length], [false, 2, 2]);
  check('the pages are saved under the reading day and start, tipologia, pass and page', one.files.map((f) => f.name), ['attiweb_elenco_2026-11-10_20261110T201500Z_CMD_p1_0.json']);
  check('each row carries its tipologia and its saved page', [one.pass_result.rows[0].tipologia, one.pass_result.rows[0].elenco],
    ['CMD', 'originali/attiweb_elenco_2026-11-10_20261110T201500Z_CMD_p1_0.json']);
  const big = m.searchPass({ tipologia: 'MMC', reading_day: DAY, started_at: RS, pass: 2,
    pages: [page(501, Array.from({ length: 500 }, (_, i) => i + 1)), page(501, [501])] });
  check('two pages: all rows, each from its own page', [big.pass_result.rows.length, big.pass_result.rows[500].elenco],
    [501, 'originali/attiweb_elenco_2026-11-10_20261110T201500Z_MMC_p2_1.json']);
  const full = m.searchPass({ tipologia: 'MMC', reading_day: DAY, started_at: RS, pass: 1,
    pages: [page(500, Array.from({ length: 500 }, (_, i) => i + 1)), { statusCode: 500, body: STRUTS }] });
  check('the empty answer after a full page ends the pass', [full.pass_result.total, full.pass_result.rows.length, full.files.length], [500, 500, 2]);
  check('a moving total between pages leaves the pass incomplete',
    m.searchPass({ tipologia: 'MMC', reading_day: DAY, started_at: RS, pass: 1, pages: [page(501, [1]), page(502, [2])] }).pass_result.error,
    'the declared total changed between pages');
  check('an error page leaves the pass incomplete',
    m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(2, [1]), { statusCode: 500, body: '<html>altro</html>' }] }).pass_result.total, null);
  check('a 200 HTML page in place of a page of rows stops the reading (DEC-033, rule 4)',
    /blocked \(an HTML page instead of the answer\)/.test(thrown(() => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(2, [1]), ok(CHECK)] })) || ''), true);
  check('a 200 HTML page in place of the historical check stops it too',
    /blocked \(an HTML page/.test(thrown(() => m.searchPass({ tipologia: 'KD', reading_day: DAY, started_at: RS, pass: 1, pages: [{ statusCode: 500, body: STRUTS }], historical: ok(CHECK) })) || ''), true);
  const empty = m.searchPass({ tipologia: 'KD', reading_day: DAY, started_at: RS, pass: 1, pages: [{ statusCode: 500, body: STRUTS }] });
  check('an empty first answer asks for the historical check', [empty.needs_historical, empty.pass_result], [true, null]);
  check('with acts in the historical interval the pass is empty',
    m.searchPass({ tipologia: 'KD', reading_day: DAY, started_at: RS, pass: 1, pages: [{ statusCode: 500, body: STRUTS }], historical: page(226, [9]) }).pass_result,
    { total: 0, rows: [], historical_total: 226 });
  check('with none it is missing data',
    m.searchPass({ tipologia: 'XMO', reading_day: DAY, started_at: RS, pass: 1, pages: [{ statusCode: 500, body: STRUTS }],
      historical: { statusCode: 500, body: STRUTS } }).pass_result.historical_total, 0);
  check('a block on a page stops the reading',
    /blocked \(HTTP 429\)/.test(thrown(() => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(1, [1]), { statusCode: 429, body: '' }] })) || ''), true);
  check('a block on the historical check stops it too',
    /blocked/.test(thrown(() => m.searchPass({ tipologia: 'KD', reading_day: DAY, started_at: RS, pass: 1, pages: [{ statusCode: 500, body: STRUTS }],
      historical: { statusCode: 403, body: '' } })) || ''), true);
  check('a fourth pass is a workflow error', /pass is 1, 2 or 3/.test(thrown(() => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 4, pages: [page(1, [1])] })) || ''), true);
  check('a tipologia out of tipo is a workflow error', /not a value of tipo/.test(thrown(() => m.searchPass({ tipologia: 'NEW', reading_day: DAY, started_at: RS, pass: 1, pages: [page(1, [1])] })) || ''), true);
  const p1 = m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(2, [1, 2])] }).pass_result;
  const p2 = m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 2, pages: [page(2, [2, 1])] }).pass_result;
  check('two equal passes from the answers complete the tipologia', m.mergePasses([p1, p2]).complete, true);

  const mixed = (pass) => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass, pages: [ok({ total: 5, elencoAtti: [
    act(1), act(2, { dscStrOrg: 'Municipio Roma II' }), act(3, { dscStrOrg: 'P.L. - X GRUPPO MARE' }),
    act(4, { dtRpr: '2025-12-10' }), act(5, { dtRpr: 'ieri' })] })] }).pass_result;
  const closed = m.closeTipologia({ tipologia: 'CMD', reading_day: DAY, started_at: RS, passes: [mixed(1), mixed(2)] });
  check('closing: two equal passes with an unreadable row leave the tipologia incomplete (DEC-033, rule 5)', [closed.complete, closed.passes, closed.total], [false, 2, 5]);
  const noIds = (pass) => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass, pages: [ok({ total: 4, elencoAtti: [
    act(1), act(null), act(undefined), act('x')] })] }).pass_result;
  check('closing: rows without a valid idDoc are each counted, not merged under one empty key (DEC-033, rule 5)',
    m.closeTipologia({ tipologia: 'CMD', reading_day: DAY, started_at: RS, passes: [noIds(1), noIds(2)] }).left_out, { riga_illeggibile: 3 });
  check('closing: the same unreadable rows in two passes are counted once, by the pass that holds the most',
    m.closeTipologia({ tipologia: 'CMD', reading_day: DAY, started_at: RS, passes: [noIds(1), m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 2,
      pages: [ok({ total: 2, elencoAtti: [act(1), act(null)] })] }).pass_result] }).left_out, { riga_illeggibile: 3 });
  const clean = (pass) => m.searchPass({ tipologia: 'CMD', reading_day: DAY, started_at: RS, pass, pages: [ok({ total: 2, elencoAtti: [act(1), act(2, { dscStrOrg: 'Municipio Roma II' })] })] }).pass_result;
  check('closing: two equal passes where every row reads complete the tipologia',
    m.closeTipologia({ tipologia: 'CMD', reading_day: DAY, passes: [clean(1), clean(2)] }).complete, true);
  check('two readings of a day never share a page name',
    m.elencoFileName(DAY, '2026-11-10T20:15:00Z', 'CMD', 1, 0) === m.elencoFileName(DAY, '2026-11-10T23:40:00Z', 'CMD', 1, 0), false);
  check('a page name without the start of its reading is a workflow error',
    /started_at/.test(thrown(() => m.elencoFileName(DAY, undefined, 'CMD', 1, 0)) || ''), true);
  check('closing: the kept row with its archive and its saved page',
    closed.kept.map((k) => [k.archive.archive_id, k.elenco]), [['qn:roma:arc:comune.roma.it:CMD:1', 'originali/attiweb_elenco_2026-11-10_20261110T201500Z_CMD_p2_0.json']]);
  check('closing: every other row is counted by reason, an unreadable one too', closed.left_out,
    { fuori_dai_municipi: 1, polizia_locale: 1, prima_del_periodo: 1, riga_illeggibile: 1 });
  const xmo = m.closeTipologia({ tipologia: 'XMO', reading_day: DAY, started_at: RS, passes: [{ total: 0, rows: [], historical_total: 0 }] });
  check('closing the missing-data case: incomplete, no other pass, said so', [xmo.complete, xmo.needs_another_pass, xmo.missing_data], [false, false, true]);
  check('closing keeps the errors of the passes',
    m.closeTipologia({ tipologia: 'CMD', reading_day: DAY, started_at: RS, passes: [{ total: null, rows: [], error: 'x' }] }).errors, ['x']);

  {
    // A tipologia of the real size (ten thousand rows and more) closes in well under the time
    // n8n gives a Code node: the passes are compared through one set of ids each.
    const big = (n) => ({ total: n, rows: Array.from({ length: n }, (_, i) => ({ idDoc: String(i + 1) })) });
    const t0 = Date.now();
    const merged = m.mergePasses([big(20000), big(20000)]);
    check('two passes of 20000 rows compare in under two seconds', [merged.complete, Date.now() - t0 < 2000], [true, true]);
  }

  const START = '2026-11-10T20:15:00Z';
  const END = '2026-11-10T20:40:00Z';
  // CMD as a closed tipologia whose rows all read: the unreadable one is the next check.
  const closeAll = (except) => m.TIPI.filter((c) => c !== except).map((c) => (c === 'CMD' ? Object.assign({}, closed, { complete: true })
    : { tipologia: c, complete: true, passes: 2, total: 0, missing_data: false, errors: [], kept: [], left_out: {} }));
  const lg = m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1', tipologie: closeAll() });
  check('a tipologia with an unreadable row makes the reading incomplete (DEC-033, rule 5)',
    m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1',
      tipologie: closeAll('CMD').concat([closed]) }).log.incomplete, ['CMD']);
  check('every tipologia read and complete: a complete reading', [lg.log.complete, lg.log.incomplete, lg.log.kept_total], [true, [], 1]);
  check('the register and the kept rows are named after the start of the reading', [lg.log_file_name, lg.righe_file_name],
    ['attiweb_lettura_20261110T201500Z.json', 'attiweb_righe_20261110T201500Z.json']);
  check('the register says the period it read', lg.log.periodo, { dtRpr_da: '2025-12-01', dtRpr_a: DAY, data_documento_da: '2026-01-01' });
  check('the register keeps the counts, never the rows', Object.keys(lg.log.tipologie.find((r) => r.tipologia === 'CMD')).sort(),
    ['complete', 'errors', 'kept', 'left_out', 'missing_data', 'passes', 'tipologia', 'total']);
  const unreadLog = m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1', tipologie: closeAll('GD') });
  check('a tipologia not closed makes the reading incomplete', [unreadLog.log.complete, unreadLog.log.unread, unreadLog.log.incomplete], [false, ['GD'], ['GD']]);
  const withXmo = closeAll('XMO').concat([xmo]);
  check('a missing-data tipologia makes it incomplete',
    m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1', tipologie: withXmo }).log.incomplete, ['XMO']);
  check('a tipologia closed twice is a workflow error',
    /closed twice/.test(thrown(() => m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1', tipologie: closeAll().concat([closed]) })) || ''), true);
  check('only a staging_ workflow writes the register',
    /staging_/.test(thrown(() => m.readingLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'D_attiweb_list', workflow_version: '1', tipologie: [] })) || ''), true);

  const righe = [closed.kept[0],
    { archive: m.describeRow(Object.assign(act(7), { tipologia: 'CMD' }), DAY), elenco: 'originali/x.json' },
    { archive: m.describeRow(Object.assign(act(8), { tipologia: 'CMD' }), DAY), elenco: 'originali/x.json' }];
  const stems = righe.map((r) => r.archive.file_stem);
  check('downloads: those without a record yet',
    m.selectDownloads({ righe, existing_names: [`${stems[0]}__v1.json`, 'altro.json'], downloaded_today: 0, cap: 300 }).map((r) => r.archive.file_stem), stems.slice(1));
  check('downloads: within what is left of the day',
    m.selectDownloads({ righe, existing_names: [], downloaded_today: 299, cap: 300 }).length, 1);
  check('downloads: none once the day is used', m.selectDownloads({ righe, existing_names: [], downloaded_today: 300, cap: 300 }), []);
  check('downloads: a row listed twice is read once', m.selectDownloads({ righe: [righe[1], righe[1]], existing_names: [], downloaded_today: 0, cap: 300 }).length, 1);
  check('downloads: the run limit holds too', m.selectDownloads({ righe, existing_names: [], downloaded_today: 0, cap: 300, run_limit: 1 }).length, 1);
  check('the reservation of a download run names its day and count', m.downloadLogName(DAY, 50, '2026-11-11T07:00:00.000Z'),
    'attiweb_download_2026-11-10_n50_20261111T070000Z.json');
  check('today\'s downloads are summed from the registers of the day, others ignored',
    m.downloadedToday([m.downloadLogName(DAY, 50, START), m.downloadLogName(DAY, 20, END), m.downloadLogName('2026-11-09', 300, START), 'altro.json'], DAY), 70);
  check('a cap above the rule is refused', /cap must be/.test(thrown(() => m.selectDownloads({ righe, existing_names: [], downloaded_today: 0, cap: 301 })) || ''), true);

  check('a captcha served with 200 in place of a PDF stops the reading',
    /blocked \(captcha\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 200, headers: {}, body: '<html><div class="g-recaptcha"></div></html>' }, mime: 'text/html', has_content: true })) || ''), true);
  check('a login page served with 200 in place of a PDF stops it too',
    /blocked \(login page\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 200, headers: {}, body: '<form><input type="password" name="p"></form>' }, mime: 'text/html', has_content: true })) || ''), true);
  check('the outcome of a run is not counted toward the cap: its reservation is',
    m.downloadedToday([m.downloadLogName(DAY, 50, START), m.downloadResultName(DAY, 12, START, 'r1')], DAY), 50);
  check('a PDF to hash', m.checkPdf({ response: { statusCode: 200, headers: {} }, mime: 'application/pdf', has_content: true }), { ok: true, reason: null });
  check('a block on a PDF stops the reading', /blocked \(HTTP 403\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 403 }, mime: 'text/html', has_content: true })) || ''), true);
  check('a redirect on a PDF stops it too', /blocked \(redirect/.test(thrown(() => m.checkPdf({ response: { statusCode: 302, headers: {} }, mime: '', has_content: false })) || ''), true);
  check('the portal\'s PDF, sent as octet-stream with a .pdf name, is an original',
    m.checkPdf({ response: { statusCode: 200, headers: {} }, mime: 'application/octet-stream', file_extension: 'pdf', has_content: true }).ok, true);
  check('octet-stream without a .pdf name is not', m.checkPdf({ response: { statusCode: 200 }, mime: 'application/octet-stream', file_extension: 'html', has_content: true }).ok, false);
  check('a missing PDF is counted, not written', m.checkPdf({ response: { statusCode: 404 }, mime: 'text/html', has_content: true }).ok, false);
  check('an HTML page served with 200 in place of a PDF stops the reading (DEC-033, rule 4)',
    /blocked \(an HTML page instead of the PDF\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 200 }, mime: 'text/html', has_content: true })) || ''), true);
  check('a page that checks the browser with a script, served with 200, stops it too',
    /blocked \(an HTML page instead of the PDF\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 200, headers: { 'content-type': 'text/html' }, body: CHECK }, mime: 'text/html; charset=utf-8', has_content: true })) || ''), true);
  check('an HTML body under another MIME type stops it as well',
    /blocked \(an HTML page instead of the PDF\)/.test(thrown(() => m.checkPdf({ response: { statusCode: 200, body: CHECK }, mime: 'application/octet-stream', file_extension: 'bin', has_content: true })) || ''), true);
  check('a plain text answer is not an original, and is counted', m.checkPdf({ response: { statusCode: 200, body: 'testo' }, mime: 'text/plain', has_content: true }).reason, 'not a PDF: text/plain');
  check('an empty file is not an original', m.checkPdf({ response: { statusCode: 200 }, mime: 'application/pdf', has_content: false }).reason, 'empty file');

  console.log('n8n adapter, reading stages — exact committed file');
  const runWith = (json, binary) => new Function('$input', '$json', 'require', src)({ item: { json, binary } }, json, require);
  const menu = { lista: m.TIPI.slice().reverse().map((c) => ({ codice: c })).concat([{ codice: 'CMD,CMC' }]) };
  const planned = runWith({ stage: 'plan', response: ok(menu) });
  check('plan: the tipologie in the fixed order, the answer dropped', [planned.json.tipologie, planned.json.response], [m.TIPI.slice(), undefined]);
  check('plan: a block on the menu stops the reading before it starts',
    /blocked \(HTTP 403\)/.test(thrown(() => runWith({ stage: 'plan', response: { statusCode: 403, body: '' } })) || ''), true);
  const passed = runWith({ stage: 'pass', tipologia: 'CMD', reading_day: DAY, started_at: RS, pass: 1, pages: [page(2, [1, 2])] });
  check('pass: the pass and the files, the answers dropped, the number kept', [passed.json.pass_result.total, passed.json.files.length, passed.json.pages, passed.json.pass], [2, 1, undefined, 1]);
  const closedNode = runWith({ stage: 'close', tipologia: 'CMD', reading_day: DAY, started_at: RS, passes: [mixed(1), mixed(2)] });
  check('close: the result equal to the module, the passes dropped', [closedNode.json.result, closedNode.json.passes], [closed, undefined]);
  const logged = runWith({ stage: 'log', reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_list', workflow_version: '1', tipologie: closeAll() });
  check('log: the register and the rows, the closed tipologie dropped', [logged.json.log.complete, logged.json.righe.length, logged.json.tipologie], [true, 1, undefined]);
  const selected = runWith({ stage: 'select', reading_day: DAY, started_at: START, righe, existing_names: [null], download_log_names: [null], cap: 2 });
  check('select: the downloads within the cap', [selected.json.downloads.length, selected.json.downloaded_today], [2, 0]);
  check('select: the reservation, named by the documents the run will ask for, before any request',
    [selected.json.reservation_name, selected.json.reservation.documents.length, selected.json.reservation.downloaded_today_before],
    [m.downloadLogName(DAY, 2, START), 2, 0]);
  const later = runWith({ stage: 'select', reading_day: DAY, started_at: START, righe, existing_names: [],
    download_log_names: [m.downloadLogName(DAY, 299, START)], cap: 300 });
  check('select: the earlier runs of the day count against the cap', [later.json.downloaded_today, later.json.downloads.length], [299, 1]);
  const RA = m.downloadLogName(DAY, 250, '2026-11-11T01:00:00Z');
  const RB = m.downloadLogName(DAY, 50, '2026-11-11T02:00:00Z');
  const RC = m.downloadLogName(DAY, 50, '2026-11-11T02:00:05Z');
  const OA = m.downloadResultName(DAY, 250, '2026-11-11T01:00:00Z', 'a');
  const day = [{ id: 'a', name: RA, createdTime: '2026-11-11T01:00:03.000Z' }, { id: 'oa', name: OA, createdTime: '2026-11-11T01:40:00.000Z' },
    { id: 'b', name: RB, createdTime: '2026-11-11T02:00:04.000Z' }, { id: 'c', name: RC, createdTime: '2026-11-11T02:00:06.000Z' }];
  check('confirm: the first of two overlapping runs goes on, an earlier finished run counts but does not hold it',
    m.reservationHolds({ reservations: day, mine: 'b', reading_day: DAY, cap: 300 }), { holds: true, used: 300, cap: 300, busy: [] });
  check('confirm: the second stops before any request, over the cap and behind a run without its outcome',
    m.reservationHolds({ reservations: day, mine: 'c', reading_day: DAY, cap: 300 }), { holds: false, used: 350, cap: 300, busy: [RB] });
  check('confirm: under the cap, a run still waits for an earlier run that has no outcome, so no record is written twice',
    m.reservationHolds({ reservations: day, mine: 'c', reading_day: DAY, cap: 300 }).busy.length > 0 &&
    m.reservationHolds({ reservations: [day[2], Object.assign({}, day[3], { name: m.downloadLogName(DAY, 1, '2026-11-11T02:00:05Z') })], mine: 'c', reading_day: DAY, cap: 300 }).holds === false, true);
  check('confirm: an earlier reservation of zero documents never holds a run',
    m.reservationHolds({ reservations: [{ id: 'z', name: m.downloadLogName(DAY, 0, '2026-11-11T00:00:00Z'), createdTime: '2026-11-11T00:00:01Z' }, day[2]], mine: 'b', reading_day: DAY, cap: 300 }).holds, true);
  check('confirm: two runs started in the same second are told apart by the id of their file',
    m.reservationHolds({ reservations: [{ id: 'x1', name: RB, createdTime: '2026-11-11T02:00:04.000Z' }, { id: 'x2', name: RB, createdTime: '2026-11-11T02:00:05.000Z' }],
      mine: 'x2', reading_day: DAY, cap: 300 }), { holds: false, used: 100, cap: 300, busy: [RB] });
  check('confirm: the order is the time Drive wrote them, not the start in the name',
    m.reservationHolds({ reservations: [{ id: 'c', name: RC, createdTime: '2026-11-11T02:00:06.000Z' }, { id: 'b', name: RB, createdTime: '2026-11-11T02:00:09.000Z' }],
      mine: 'b', reading_day: DAY, cap: 300 }).busy, [RC]);
  check('confirm: a reservation Drive does not show yet is a workflow error',
    /is not among the day/.test(thrown(() => m.reservationHolds({ reservations: [day[0]], mine: 'b', reading_day: DAY, cap: 300 })) || ''), true);
  const stop = runWith({ stage: 'confirm', reading_day: DAY, started_at: '2026-11-11T02:00:05Z', cap: 300, count: 50, reservation_id: 'c', reservations: day.concat([{}]) });
  check('confirm in n8n: a run that stops writes an outcome of zero documents, with the reason',
    [stop.json.confirm.holds, stop.json.stop_name, stop.json.stop_log.read, stop.json.stop_log.stopped, stop.json.reservations],
    [false, 'attiweb_scaricati_2026-11-10_n0_20261111T020005Z_c.json', 0, 'an earlier run of the day has no outcome yet', undefined]);
  const go = runWith({ stage: 'confirm', reading_day: DAY, started_at: '2026-11-11T02:00:00Z', cap: 300, count: 50, reservation_id: 'b', reservations: day });
  check('confirm in n8n: a run that holds has no outcome to write yet', [go.json.confirm.holds, go.json.stop_name], [true, undefined]);
  const none = runWith({ stage: 'confirm', reading_day: DAY, started_at: '2026-11-11T02:00:00Z', cap: 300, count: 0, reservation_id: 'b', reservations: day });
  check('confirm in n8n: a run with nothing to download writes its outcome of zero documents',
    [none.json.stop_name, none.json.stop_log.stopped], ['attiweb_scaricati_2026-11-10_n0_20261111T020000Z_b.json', 'nothing to download']);
  const dlog = m.downloadLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_download', workflow_version: '1', reservation_id: 'r1',
    esiti: [{ archive_id: 'a', written: true }, { archive_id: 'b', written: false, reason: 'not a PDF: text/html' }] });
  check('download register: named by day and count, outcomes kept', [dlog.name, dlog.log.read, dlog.log.written, dlog.log.not_written],
    ['attiweb_scaricati_2026-11-10_n2_20261110T201500Z_r1.json', 2, 1, [{ archive_id: 'b', reason: 'not a PDF: text/html' }]]);
  check('download register: an outcome without its id is a workflow error',
    /without its archive_id/.test(thrown(() => m.downloadLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_download', workflow_version: '1', esiti: [{}] })) || ''), true);
  const dl = runWith({ stage: 'download_log', reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_download', workflow_version: '1', reservation_id: 'r1', esiti: [{ archive_id: 'a', written: true }] });
  check('download_log: the register, the outcomes dropped', [dl.json.name, dl.json.esiti], ['attiweb_scaricati_2026-11-10_n1_20261110T201500Z_r1.json', undefined]);
  const late = m.downloadLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_download', workflow_version: '1', reservation_id: 'r1',
    esiti: [{ archive_id: 'a', written: true }, { archive_id: 'b', written: false, requested: false, reason: 'the Rome day changed: left for the next run' }] });
  check('download register: a document left unasked when the Rome day changed is not read, and is listed apart',
    [late.name, late.log.read, late.log.not_requested], ['attiweb_scaricati_2026-11-10_n1_20261110T201500Z_r1.json', 1, ['b']]);
  check('download register: an outcome without its reservation is a workflow error',
    /reservation_id/.test(thrown(() => m.downloadLog({ reading_day: DAY, started_at: START, finished_at: END, workflow: 'staging_D_attiweb_download', workflow_version: '1', esiti: [] })) || ''), true);
  const same = [{ id: 'p1', name: RB, createdTime: '2026-11-11T02:00:04.000Z' }, { id: 'p2', name: RB, createdTime: '2026-11-11T02:00:05.000Z' },
    { id: 'p3', name: RB, createdTime: '2026-11-11T02:00:06.000Z' }, { id: 'o2', name: m.downloadResultName(DAY, 0, '2026-11-11T02:00:00Z', 'p2'), createdTime: '2026-11-11T02:00:12.000Z' }];
  check('confirm: three runs in the same second: the outcome of the second never frees the first, still running',
    m.reservationHolds({ reservations: same, mine: 'p3', reading_day: DAY, cap: 300 }).busy, [RB]);
  check('confirm: an outcome written before outcomes carried the id is still matched by the start',
    m.reservationHolds({ reservations: [{ id: 'q1', name: RB, createdTime: '2026-11-11T02:00:04.000Z' }, { id: 'q0', name: 'attiweb_scaricati_2026-11-10_n50_20261111T020000Z.json', createdTime: '2026-11-11T02:30:00Z' },
      { id: 'q2', name: RC, createdTime: '2026-11-11T03:00:00Z' }], mine: 'q2', reading_day: DAY, cap: 300 }).busy, []);
  const arcItem = m.describeRow(Object.assign(act(7), { tipologia: 'CMD' }), DAY);
  const rec = runWith({ stage: 'record', archive: arcItem, download: DL, existing: [] });
  check('record: the stage name gives the record too', rec.json.record_file_name, 'roma__arc__comune.roma.it__CMD__7__v1.json');
  const pdfItem = runWith({ stage: 'pdf', response: { statusCode: 200, headers: {} } }, { data: { mimeType: 'application/pdf', fileSize: '45.3 kB' } });
  check('pdf: a PDF with content is ok', pdfItem.json.pdf.ok, true);
  const portal = runWith({ stage: 'pdf', response: { statusCode: 200, headers: {} } },
    { data: { mimeType: 'application/octet-stream', fileExtension: 'pdf', fileSize: '247 kB', bytes: 246928 } });
  check('pdf: the binary as n8n writes it for the portal\'s answer is ok', portal.json.pdf.ok, true);
  const zero = runWith({ stage: 'pdf', response: { statusCode: 200, headers: {} } }, { data: { mimeType: 'application/pdf', fileSize: '0 B' } });
  check('pdf: n8n\'s "0 B" is an empty file', zero.json.pdf.reason, 'empty file');
  const asText = runWith({ stage: 'pdf', mime: 'text/plain', file_extension: 'txt',
    response: { statusCode: 200, headers: {}, body: 'Documento non disponibile' } });
  check('pdf: an answer turned into text is judged by its type, and counted', asText.json.pdf, { ok: false, reason: 'not a PDF: text/plain' });
  check('pdf: an HTML page turned into text stops the reading, whatever it says (DEC-033, rule 4)',
    /an HTML page instead of the PDF/.test(thrown(() => runWith({ stage: 'pdf', mime: 'text/html', file_extension: 'html',
      response: { statusCode: 200, headers: {}, body: '<html><p>Documento non disponibile</p></html>' } })) || ''), true);
  checks += 1;
  try {
    runWith({ stage: 'pdf', mime: 'text/html', response: { statusCode: 200, headers: {}, body: '<script src="https://www.google.com/recaptcha/api.js"></script><div class="g-recaptcha"></div>' } });
    failures += 1; console.log('  FAIL pdf: a captcha page as text stops the reading\n       got no error');
  } catch (e) { console.log('  ok   pdf: a captcha page as text stops the reading'); }
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}
