"""Foglio per Drive con le righe per fatto (titoli e link delle testate: non va nel repository).

Uso: foglio.py DIR   (legge DIR/righe_*.json e DIR/riepilogo.json, scrive DIR/cronaca_testate.xlsx)
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font

LEGGIMI = [
    "Cronaca del mese: fatti ufficiali e testate",
    "",
    "Foglio 'Ufficiali x testate': i fatti di cronaca nel Comune di Roma pubblicati da Questura, Carabinieri,",
    "Vigili del Fuoco e Polizia Locale, con le testate che li hanno ripresi, trovate con la ricerca web",
    "(solo titolo, URL e riassunto della ricerca; nessun articolo aperto).",
    "'certa': tipo, luogo, almeno due dettagli e data compatibili. 'probabile': un solo dettaglio, o data non verificabile.",
    "La ricerca non vede corriere.it, repubblica.it e rainews.it; la colonna 'cercato' dice quali fatti sono rimasti",
    "senza ricerca per il tetto del turno.",
    "",
    "Foglio 'Testate aperte': i fatti di cronaca romana del mese sulle sei testate che non escludono gli agenti AI,",
    "dai titoli presi da sitemap e API ammesse dal robots.txt, e se corrispondono a un fatto ufficiale.",
    "",
    "Contiene titoli e link delle testate: resta su Drive (DEC-102, DEC-104).",
    "Metodo: docs/sources/CRONACA_PROCESSO_2026-10.md; strumenti: tools/cronaca-prova/.",
]
LARGHE = {"fatto", "titoli", "testate", "link", "nota"}


def foglio(wb, nome, righe, colonne):
    ws = wb.create_sheet(nome)
    ws.append(colonne)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in righe:
        ws.append([r.get(c) for c in colonne])
    ws.freeze_panes = "A2"
    for i, c in enumerate(colonne, 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = 60 if c in LARGHE else 14


def main(base):
    wb = Workbook()
    ws = wb.active
    ws.title = "Leggimi"
    for line in LEGGIMI:
        ws.append([line])
    ws["A1"].font = Font(bold=True)
    foglio(wb, "Ufficiali x testate", json.load(open(f"{base}/righe_avanti.json")),
           ["id", "fonte", "pubblicato", "esito", "pagine", "fatto", "cercato", "n_testate", "n_testate_certe",
            "testate", "link", "nota"])
    foglio(wb, "Testate aperte", json.load(open(f"{base}/righe_inverso.json")),
           ["fid", "data", "tipo", "fatto", "luogo", "pagina_qn", "livello", "n_testate", "testate", "ufficiale",
            "corrispondenza", "titoli", "link"])
    ws = wb.create_sheet("Riepilogo")
    for parte, valori in json.load(open(f"{base}/riepilogo.json")).items():
        for k, v in valori.items():
            ws.append([parte, k, json.dumps(v, ensure_ascii=False)])
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 120
    wb.save(f"{base}/cronaca_testate.xlsx")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
