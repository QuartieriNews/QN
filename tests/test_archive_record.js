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

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}
