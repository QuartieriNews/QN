#!/usr/bin/env python3
"""June 2026 table: 89 QN pages x editorial blocks, with the contents behind each cell.

  tabella_giugno.py --pkg PKG --cronaca 'DIR/schede_lotto_*.jsonl' \
      --eventi-fb FB/fb_proposte.json --eventi-fb-decisioni 'FB/decisioni_*.jsonl' \
      --correzioni runs/2026-10-09/correzioni_giugno.json --out DIR

Sources, as the owner chose on 9 October 2026:
- Amministrazione and official Eventi: the 19 September reference assignments,
  with the documented corrections file applied (and listed).
- Cronaca: the June official releases reread in full (C1, C2, C4, C5); the old
  C* records of the reference are replaced, not added.
- Eventi Facebook: the owner's 20 September-20 October collection, a declared
  proxy for a month of Facebook events, never mixed with the June count.
- Conversazione: ND (not collected), never zero.

Writes DIR/tabella_giugno_2026.xlsx (per-item contents: goes to Drive, not to
the repository, DEC-102: DIR must be outside the worktree) and the counts-only
matrix, DIR/matrice_giugno_conteggi.csv or the path given with --matrice (the
one file of the two that may be versioned). Counts are records and page
presences, not certified facts; the dedup interval shows how many distinct
facts the doubtful twins could leave.
"""
import argparse
import collections
import csv
import glob
import io
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import _read, fuori_dal_repository, package_root  # noqa: E402

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
GATE = {'Amministrazione': 5, 'Cronaca': 1, 'Eventi': 10}
BLOCKS = ('Amministrazione', 'Cronaca', 'Eventi')
OFFICIAL_CRONACA = {'C1', 'C2', 'C4', 'C5'}      # Questura, Carabinieri, Vigili del Fuoco, Polizia Locale
LEVELS = {'quartiere', 'municipio', 'citta'}
OUTCOMES = {'U', 'M', 'T', 'D', 'I', 'F'}


def source_code(fonte):
    """The source code of a record ('C1' from 'C1' or 'C1 Questura'): exact, never a prefix."""
    return str(fonte or '').strip().split()[0] if str(fonte or '').strip() else ''


def jl(pattern):
    """Records of every file matching the glob. A duplicate id across files is
    an error, not two presences (a retry can leave two lots behind)."""
    out, seen = [], {}
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f'nessun file per {pattern!r}')
    for f in files:
        for l in Path(f).read_text(encoding='utf-8').splitlines():
            if not l.strip():
                continue
            r = json.loads(l)
            if r['id'] in seen:
                raise SystemExit(f"id {r['id']} ripetuto: {seen[r['id']]} e {f}")
            seen[r['id']] = f
            out.append(r)
    return out


def by_id(lines, what):
    """id -> record, refusing a repeated id instead of keeping the last copy."""
    out = {}
    for l in lines:
        if not l.strip():
            continue
        r = json.loads(l)
        if r['id'] in out:
            raise SystemExit(f"id {r['id']} ripetuto in {what}")
        out[r['id']] = r
    return out


def check_corrections(corr_list):
    """The corrections file: one entry per id, every entry well formed."""
    out = {}
    for c in corr_list:
        if c['id'] in out:
            raise SystemExit(f"correzione ripetuta per {c['id']}")
        if c.get('esito') not in OUTCOMES or c.get('livello_portata') not in LEVELS:
            raise SystemExit(f"correzione {c['id']}: esito o livello_portata non ammessi")
        out[c['id']] = c
    return out


def check_level(d, what):
    """DEC-106: a decision states its livello_portata; no default is invented."""
    lv = d.get('livello_portata')
    if lv not in LEVELS:
        raise SystemExit(f"{what} {d.get('id')}: livello_portata mancante o non ammesso ({lv!r})")
    if d.get('esito') == 'T' and lv == 'quartiere':
        raise SystemExit(f"{what} {d.get('id')}: T con livello_portata quartiere")
    return lv


def cell(v):
    """A value from the sources as text in a spreadsheet cell, never a formula."""
    if isinstance(v, str) and v[:1] in ('=', '+', '-', '@'):
        return "'" + v
    return v


def muns(text):
    return {m for m in re.findall(r'\b([IVX]{1,4})\b', text or '') if m in ROMAN}


def load(a):
    pkg = package_root(a.pkg)
    gaz = _read(pkg / 'input' / 'gazetteer_qn.json')
    pages = {z['publication_zone_id']: z for z in gaz['publication_zones'] if z['is_page']}
    page_mun = {k: muns(z['primary_municipality'] + ';' + z['spans_municipalities']) or {z['primary_municipality']}
                for k, z in pages.items()}
    inp = by_id((pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines(), 'schede_input.jsonl')
    ref = by_id((pkg / 'benchmark' / 'assegnazioni_2026-09-19.jsonl').read_text(encoding='utf-8').splitlines(), 'assegnazioni_2026-09-19.jsonl')
    corr = check_corrections(json.loads(Path(a.correzioni).read_text(encoding='utf-8'))['correzioni'])
    return pkg, pages, page_mun, inp, ref, corr


def items(a):
    pkg, pages, page_mun, inp, ref, corr = load(a)
    rows = []
    applied = set()
    # 1. Reference records (Amministrazione, official Eventi), C* replaced by the reread.
    for i, r in inp.items():
        if r['in_stock'] != 1 or r['fonte'].startswith('C'):
            continue
        if r['blocco_editoriale_proposto'] not in BLOCKS:
            raise SystemExit(f"{i}: blocco {r['blocco_editoriale_proposto']!r} non ammesso ({', '.join(BLOCKS)})")
        d = dict(ref[i])
        level = 'quartiere' if d['esito'] in 'UM' else ''
        if i in corr:
            d.update({k: corr[i][k] for k in ('esito', 'pagine')})
            level = corr[i]['livello_portata']
            applied.add(i)
        if d['esito'] == 'T' and not level:
            level = 'municipio' if muns(r['municipio']) else 'citta'
        rows.append({'id': i, 'blocco': r['blocco_editoriale_proposto'], 'fonte': r['fonte'], 'esito': d['esito'],
                     'pagine': sorted(d['pagine']), 'livello': level, 'municipi': sorted(muns(r['municipio'])),
                     'titolo': r['titolo'], 'data': r['data_fatto'] or r['data_pubblicazione'], 'url': r['url_fonte'],
                     'motivo': d['motivo'], 'gemello': r['gemello_id'] if r['dedup_stato'] == 'dubbio' else '',
                     'periodo': 'giugno 2026', 'corretta': i in corr})
    # Every correction names a record it could change; a stale id is an error, not a silent no-op.
    stale = sorted(set(corr) - applied)
    if stale:
        raise SystemExit(f"correzioni non applicabili (id assenti, C* o non in_stock): {stale}")
    # 2. Cronaca reread in full: official sources only (owner, 9 October).
    cron = jl(a.cronaca)
    bad = sorted({str(s['fonte']) for s in cron if source_code(s['fonte']) not in OFFICIAL_CRONACA})
    if bad:
        raise SystemExit(f"Cronaca solo da fonti ufficiali {sorted(OFFICIAL_CRONACA)}: trovate {bad}")
    for s in cron:
        lv = s.get('livello_portata') or ('quartiere' if s['esito'] in 'UM' else 'municipio')
        rows.append({'id': s['id'], 'blocco': 'Cronaca', 'fonte': s['fonte'], 'esito': s['esito'], 'pagine': sorted(s['pagine']),
                     'livello': lv, 'municipi': sorted(muns(s.get('municipio', ''))), 'titolo': s['titolo'],
                     'data': s.get('data_fatto') or s.get('data_pubblicazione', ''), 'url': s['url'], 'motivo': s['motivo'],
                     'gemello': s.get('stesso_fatto_di', ''), 'periodo': 'giugno 2026', 'corretta': False,
                     'fuori_roma': s.get('fuori_roma', False)})
    # 3. Facebook events: civic-confirmed automatic U, reviewer decisions for the rest.
    dec = {d['id']: d for d in jl(a.eventi_fb_decisioni)}
    for e in json.loads(Path(a.eventi_fb).read_text(encoding='utf-8')):
        civic_ok = e['proposta']['esito_proposto'] == 'U' and any(
            c['trovato'] and c['pagine'] == e['proposta']['pagine_proposte'] for c in e['civici'])
        if e['id'] in dec:
            d = dec[e['id']]
            esito, pg, motivo, lv = d['esito'], sorted(d['pagine']), d['motivo'], check_level(d, 'decisione Facebook')
        elif not civic_ok:
            # Never count an unreviewed uncertain proposal as an assignment.
            esito, pg, motivo, lv = 'D', [], 'non ancora rivisto: proposta del codice incerta', ''
        else:
            esito, pg, lv = 'U', e['proposta']['pagine_proposte'], 'quartiere'
            motivo = 'civico ufficiale del Geoportale: ' + '; '.join(f"{c['testo']} {c['civico']}" for c in e['civici'] if c['trovato'])
        inwin = '2026-09-20' <= e['data_inizio'] <= '2026-10-20' or (e['data_inizio'] < '2026-09-20' <= (e['data_fine'] or ''))
        rows.append({'id': e['id'], 'blocco': 'Eventi Facebook', 'fonte': 'Facebook (raccolta owner)', 'esito': esito,
                     'pagine': pg, 'livello': lv, 'municipi': [], 'titolo': e['titolo'], 'data': e['data_inizio'],
                     'url': e['url'], 'motivo': motivo, 'gemello': '', 'corretta': False,
                     'periodo': '20 set-20 ott 2026' if inwin else 'fuori finestra'})
    return pages, page_mun, rows, corr


def fatti_min(ids, twin):
    """Distinct facts if every doubtful twin is the same fact (union-find in the cell)."""
    parent = {i: i for i in ids}

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in ids:
        g = twin.get(i)
        if g in parent:
            parent[f(i)] = f(g)
    return len({f(i) for i in ids})


def build(a):
    pages, page_mun, rows, corr = items(a)
    twin = {r['id']: r['gemello'] for r in rows if r['gemello']}
    own = collections.defaultdict(list)          # (page, block) -> ids
    mun_level = collections.defaultdict(list)    # (municipio, block) -> ids of municipal-level items without a page
    city = collections.defaultdict(list)
    for r in rows:
        if r['esito'] in ('U', 'M') and (r['blocco'] != 'Eventi Facebook' or r['periodo'] != 'fuori finestra'):
            for p in r['pagine']:
                own[(p, r['blocco'])].append(r['id'])
        elif r['esito'] == 'T':
            if r['livello'] == 'municipio' and r['municipi']:
                for m in r['municipi']:
                    mun_level[(m, r['blocco'])].append(r['id'])
            else:
                city[r['blocco']].append(r['id'])
    blocks = ['Amministrazione', 'Cronaca', 'Eventi', 'Eventi Facebook']
    matrix = []
    for slug, z in sorted(pages.items(), key=lambda kv: kv[1]['name_display']):
        ms = page_mun[slug]
        row = {'pagina': z['name_display'], 'slug': slug, 'municipio': '/'.join(sorted(ms, key=ROMAN.index))}
        for b in blocks:
            ids = own[(slug, b)]
            row[f'{b} propri'] = len(ids)
            if b in ('Amministrazione', 'Eventi'):
                row[f'{b} fatti (min)'] = fatti_min(ids, twin)
            mids = sorted({i for m in ms for i in mun_level[(m, b)]})
            if b != 'Eventi Facebook':
                row[f'{b} del Municipio'] = len(mids)
                # DEC-006 (open): a thin page could show its Municipio's content.
                same_mun = {i for p2, ms2 in page_mun.items() if ms2 & ms for i in own[(p2, b)]}
                row[f'{b} con ripiego Municipio'] = len(same_mun | set(mids))
        row['Conversazione'] = 'ND'
        ev = row['Eventi propri'] + row['Eventi Facebook propri']
        row['Soglia Amministrazione >=5'] = 'sì' if row['Amministrazione propri'] >= GATE['Amministrazione'] else 'no'
        row['Soglia Cronaca >=1'] = 'sì' if row['Cronaca propri'] >= GATE['Cronaca'] else 'no'
        row['Soglia Eventi >=10 (giugno + FB)'] = 'sì' if ev >= GATE['Eventi'] else 'no'
        row['Soglie con ripiego'] = 'sì' if (row['Amministrazione con ripiego Municipio'] >= 5 and row['Cronaca con ripiego Municipio'] >= 1
                                            and row['Eventi con ripiego Municipio'] + row['Eventi Facebook propri'] >= 10) else 'no'
        matrix.append(row)
    return pages, rows, matrix, own, mun_level, city, corr


def write(a, pages, rows, matrix, own, mun_level, city, corr):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    byid = {r['id']: r for r in rows}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Leggimi'
    tot = collections.Counter()
    for r in matrix:
        for k, v in r.items():
            if isinstance(v, int):
                tot[k] += v
    esiti = collections.Counter((r['blocco'], r['esito']) for r in rows)
    lines = [
        ['QN — tabella di giugno 2026: quartieri x blocchi'],
        ['Preparata il 9 ottobre 2026 da Claude Code su indicazioni dell\'owner. Le celle contano schede e presenze, non fatti certificati.'],
        [],
        ['Blocco', 'Fonte e periodo', 'Note'],
        ['Amministrazione', 'A1 notizie municipali (tutto giugno); A2 atti, A3 RomaTV, A4 YouTube (8-28 giugno)', 'Assegnazioni del 19 settembre con 13 correzioni documentate (scheda Correzioni). Atti e video non coprono 1-7 e 29-30 giugno (scelta dell\'owner: nessuna spesa).'],
        ['Cronaca', 'C1 Questura, C2 Carabinieri, C4 Vigili del Fuoco, C5 Polizia Locale: 109 comunicati di giugno riletti per intero il 9 ottobre', 'Procura e Guardia di Finanza: nessun comunicato su Roma a giugno (misurato). Solo fonti ufficiali (scelta dell\'owner).'],
        ['Eventi', 'E2 culture.roma.it, E3 agenda comune.roma.it, avvisi di eventi dei Municipi (giugno)', 'Eventi del mese, non «eventi futuri nei 30 giorni» della soglia di lancio.'],
        ['Eventi Facebook', 'Raccolta manuale dell\'owner, 20 settembre-20 ottobre 2026 (258 URL)', 'STIMA: è un altro mese, usata come rappresentativa di un mese di eventi Facebook. Esclusi gli eventi fuori finestra.'],
        ['Conversazione', '—', 'ND: gruppi Facebook non raccolti. Non è zero.'],
        [],
        ['Colonne', 'propri = schede assegnate alla pagina (U/M); fatti (min) = se ogni dubbio di doppione fosse lo stesso fatto; del Municipio = notizie di portata municipale senza pagina (DEC-106); con ripiego Municipio = tutto il Municipio (DEC-006, aperta: mostrato, non deciso)'],
        ['Soglie', 'DEC-014: per pagina almeno 5 Amministrazione, 1 Cronaca, 10 eventi futuri. Qui confrontate con i conteggi del mese, quindi indicative.'],
        [],
        ['Totali', 'Pagine 89', f"Amministrazione presenze {tot['Amministrazione propri']}; Cronaca {tot['Cronaca propri']}; Eventi giugno {tot['Eventi propri']}; Eventi Facebook {tot['Eventi Facebook propri']}"],
        ['Notizie cittadine (senza Municipio)', '; '.join(f'{b}: {len(v)}' for b, v in sorted(city.items()))],
        ['Esiti per blocco', '; '.join(f'{b} {e}: {n}' for (b, e), n in sorted(esiti.items()))],
    ]
    for l in lines:
        ws.append(l)
    ws['A1'].font = Font(bold=True, size=14)
    ws.column_dimensions['A'].width = 34
    ws.column_dimensions['B'].width = 80
    ws.column_dimensions['C'].width = 90
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')

    wm = wb.create_sheet('Matrice')
    cols = list(matrix[0])
    wm.append(cols)
    for r in matrix:
        wm.append([r[c] for c in cols])
    red = PatternFill('solid', fgColor='F8D7DA')
    green = PatternFill('solid', fgColor='D4EDDA')
    for c in wm[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for row in wm.iter_rows(min_row=2):
        for c in row:
            if c.value in ('sì', 'no'):
                c.fill = green if c.value == 'sì' else red
    wm.freeze_panes = 'D2'
    wm.column_dimensions['A'].width = 26

    wc = wb.create_sheet('Contenuti')
    hdr = ['pagina', 'municipio', 'blocco', 'id', 'data', 'titolo', 'fonte', 'esito', 'pagine del contenuto', 'periodo', 'link', 'motivo geografico', 'corretta']
    wc.append(hdr)
    names = {k: z['name_display'] for k, z in pages.items()}
    page_mun = {r['slug']: r['municipio'] for r in matrix}
    for (p, b), ids in sorted(own.items(), key=lambda kv: (names[kv[0][0]], kv[0][1])):
        for i in ids:
            r = byid[i]
            wc.append([cell(x) for x in (names[p], page_mun[p], b, i, r['data'], r['titolo'], r['fonte'], r['esito'],
                                         ', '.join(names.get(x, x) for x in r['pagine']), r['periodo'], r['url'], r['motivo'],
                                         'sì' if r['corretta'] else '')])
    wc.freeze_panes = 'A2'

    wmu = wb.create_sheet('Notizie dei Municipi')
    wmu.append(['municipio', 'blocco', 'id', 'data', 'titolo', 'fonte', 'link', 'motivo'])
    for (m, b), ids in sorted(mun_level.items(), key=lambda kv: (ROMAN.index(kv[0][0]), kv[0][1])):
        for i in ids:
            r = byid[i]
            wmu.append([cell(x) for x in (m, b, i, r['data'], r['titolo'], r['fonte'], r['url'], r['motivo'])])
    for b, ids in sorted(city.items()):
        for i in ids:
            r = byid[i]
            wmu.append([cell(x) for x in ('città', b, i, r['data'], r['titolo'], r['fonte'], r['url'], r['motivo'])])

    wd = wb.create_sheet('Non assegnati')
    wd.append(['blocco', 'id', 'esito', 'data', 'titolo', 'fonte', 'periodo', 'link', 'motivo'])
    for r in rows:
        if r['esito'] in ('D', 'I', 'F') or (r['blocco'] == 'Eventi Facebook' and r['periodo'] == 'fuori finestra'):
            wd.append([cell(x) for x in (r['blocco'], r['id'], r['esito'], r['data'], r['titolo'], r['fonte'], r['periodo'], r['url'], r['motivo'])])

    wk = wb.create_sheet('Correzioni')
    wk.append(['id', 'nuovo esito', 'nuove pagine', 'livello', 'origine', 'ragione'])
    for c in corr.values():
        wk.append([cell(x) for x in (c['id'], c['esito'], ', '.join(c['pagine']), c['livello_portata'], c['origine'], c['ragione'])])
    for sh in (wc, wmu, wd, wk):
        for c in sh[1]:
            c.font = Font(bold=True)
    # Both outputs land whole or not at all: a temporary beside the target, then os.replace.
    xlsx = out / 'tabella_giugno_2026.xlsx'
    tmp = xlsx.with_suffix(f'.{os.getpid()}.tmp')
    wb.save(tmp)
    os.replace(tmp, xlsx)
    num = [c for c in cols if c not in ('pagina',)]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=['pagina'] + num, delimiter=';', lineterminator='\r\n')
    w.writeheader()
    w.writerows(matrix)
    matrice = Path(a.matrice) if a.matrice else out / 'matrice_giugno_conteggi.csv'
    tmp = matrice.with_suffix(f'.{os.getpid()}.tmp')
    tmp.write_text('\ufeff' + buf.getvalue(), encoding='utf-8', newline='')
    os.replace(tmp, matrice)
    return xlsx


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--cronaca', required=True)
    ap.add_argument('--eventi-fb', required=True)
    ap.add_argument('--eventi-fb-decisioni', required=True)
    ap.add_argument('--correzioni', required=True)
    ap.add_argument('--out', required=True, help='cartella del foglio con i contenuti: fuori dal repository (DEC-102)')
    ap.add_argument('--matrice', help='percorso della matrice dei soli conteggi (default: OUT/matrice_giugno_conteggi.csv)')
    a = ap.parse_args()
    if not fuori_dal_repository(a.out):
        raise SystemExit('il foglio contiene titoli e link delle fonti: --out deve stare fuori dal repository (DEC-102); '
                         'la matrice dei conteggi si versiona con --matrice')
    pages, rows, matrix, own, mun_level, city, corr = build(a)
    xlsx = write(a, pages, rows, matrix, own, mun_level, city, corr)
    summary = collections.Counter()
    for r in matrix:
        for k in ('Soglia Amministrazione >=5', 'Soglia Cronaca >=1', 'Soglia Eventi >=10 (giugno + FB)', 'Soglie con ripiego'):
            summary[(k, r[k])] += 1
    cron = [r for r in rows if r['blocco'] == 'Cronaca']
    print(json.dumps({'xlsx': str(xlsx), 'pagine': len(matrix), 'correzioni_applicate': len(corr),
                      'cronaca': {'schede': len(cron), 'comunicati_unici': len({r['url'] for r in cron})},
                      'soglie': {f'{k} {v}': n for (k, v), n in sorted(summary.items())}},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
