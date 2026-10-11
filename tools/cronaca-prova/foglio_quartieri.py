"""Foglio della cronaca del mese per quartiere (tabella_quartieri.py → Excel per Drive).

Uso: foglio_quartieri.py DIR [MESE]   (legge DIR/tabella/*, scrive DIR/tabella/cronaca_quartieri.xlsx)

Fogli: Leggimi; Quartieri in colonna (come chiesto dall'owner: una colonna per pagina, le
notizie del mese come valori); Quartieri in riga (la stessa tabella, comoda da ordinare);
Riepilogo; Fatti (una riga per fatto con fonti e link: dati delle fonti, solo Drive).
"""
import csv, json, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

RIGHE = [("pubblicabili", "Notizie pubblicabili (ufficiali + giornali con 2 fonti)"),
         ("ufficiale", "di cui da fonti ufficiali"),
         ("stampa_due_fonti", "di cui dai giornali con almeno 2 fonti"),
         ("stampa_una_fonte", "Giornali con 1 sola fonte (non pubblicate)"),
         ("chiuse_due_fonti", "Solo testate chiuse, 2+ fonti (non scrivibili)")]
VUOTO = PatternFill("solid", fgColor="F8D7DA")
PIENO = PatternFill("solid", fgColor="D4EDDA")


def main(base, mese="giugno 2026"):
    righe = list(csv.DictReader(open(f"{base}/tabella/per_pagina.csv", encoding="utf-8-sig"), delimiter=";"))
    R = json.load(open(f"{base}/tabella/riepilogo.json"))
    fatti = json.load(open(f"{base}/tabella/fatti.json"))
    wb = Workbook()
    ws = wb.active
    ws.title = "Leggimi"
    pc = R["pagine_coperte"]
    for line in [
        f"Cronaca di {mese} per quartiere, con la regola delle due fonti (DEC-108, MVP)",
        "",
        "Pubblicabile = fatto da fonte ufficiale (Questura, Carabinieri, Vigili del Fuoco, Polizia Locale),",
        "oppure fatto riportato da almeno due editori diversi di cui almeno una testata aperta (da cui si può scrivere).",
        "Le testate dello stesso gruppo valgono una fonte (Il Messaggero e Leggo; RomaToday e Today.it; Il Tempo e il Giornale).",
        "Testate chiuse (RomaToday, Il Messaggero, Corriere, Repubblica, ANSA…): solo titolo, link e ora dall'indice GDELT.",
        "Si contano solo i fatti con una pagina-quartiere; quelli di livello municipio, città o dubbi sono nel foglio Fatti.",
        "",
        f"Pagine con almeno una notizia pubblicabile: {pc['ufficiali_piu_stampa_due_fonti']} su {R['pagine_attive']} "
        f"(solo fonti ufficiali: {pc['solo_ufficiali']}).",
        "",
        "Contiene titoli e link delle testate: resta su Drive (DEC-102, DEC-104). Metodo: docs/sources/CRONACA_PROCESSO_2026-10.md.",
    ]:
        ws.append([line])
    ws["A1"].font = Font(bold=True)

    # quartieri in colonna
    ws = wb.create_sheet("Quartieri in colonna")
    ws.append(["", *[r["pagina"] for r in righe], "Totale", "Pagine con almeno 1"])
    ws.append(["Municipio", *[r["municipio"] for r in righe]])
    for chiave, etichetta in RIGHE:
        valori = [int(r[chiave]) for r in righe]
        ws.append([etichetta, *valori, sum(valori), sum(1 for v in valori if v)])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(text_rotation=90)
    for j, r in enumerate(righe, 2):
        ws.cell(3, j).fill = PIENO if int(r["pubblicabili"]) else VUOTO
    ws.column_dimensions["A"].width = 52
    for j in range(2, len(righe) + 4):
        ws.column_dimensions[get_column_letter(j)].width = 5
    ws.freeze_panes = "B2"

    # quartieri in riga
    ws = wb.create_sheet("Quartieri in riga")
    ws.append(["Pagina", "Municipio", *[e for _, e in RIGHE]])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in sorted(righe, key=lambda r: -int(r["pubblicabili"])):
        ws.append([r["pagina"], r["municipio"], *[int(r[k]) for k, _ in RIGHE]])
        ws.cell(ws.max_row, 3).fill = PIENO if int(r["pubblicabili"]) else VUOTO
    ws.column_dimensions["A"].width = 30
    for j in range(3, 8):
        ws.column_dimensions[get_column_letter(j)].width = 22
    ws.freeze_panes = "A2"

    # riepilogo
    ws = wb.create_sheet("Riepilogo")
    for k, v in R.items():
        ws.append([k, json.dumps(v, ensure_ascii=False) if not isinstance(v, (int, str)) else v])
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 140

    # fatti
    ws = wb.create_sheet("Fatti")
    col = ["id", "categoria", "origine", "data", "fatto", "livello", "pagine", "n_editori", "editori", "aperte", "chiuse", "link"]
    ws.append(col)
    for c in ws[1]:
        c.font = Font(bold=True)
    for f in sorted(fatti, key=lambda f: (f["categoria"], f["data"] or "")):
        ws.append([f["id"], f["categoria"], f["origine"], f["data"], f["fatto"], f.get("livello"), "+".join(f["pagine"]),
                   f["n_editori"], "; ".join(f["editori"]), "; ".join(f["aperte"]), "; ".join(f["chiuse"]),
                   " ".join(f["link"])])
    for j, w in enumerate([14, 18, 10, 11, 70, 11, 24, 9, 40, 30, 40, 60], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A2"
    wb.save(f"{base}/tabella/cronaca_quartieri.xlsx")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(*sys.argv[1:3])
