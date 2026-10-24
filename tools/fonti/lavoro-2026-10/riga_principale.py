# Colonna riga_principale_proposta in 'Eventi unificati': per ogni gruppo di doppioni comanda la riga più vicina alla fonte primaria (DEC-025, opzione a, PROPOSTA).
import openpyxl,collections,sys
from openpyxl.styles import Font
UNICO='/mnt/user-data/outputs/eventi_unico.xlsx'
wb=openpyxl.load_workbook(UNICO); ws=wb['Eventi unificati']; h=[c.value for c in ws[1]]
def g(r,k): return r[h.index(k)] if k in h else None
RANK={'letto alla fonte (sito del luogo)':0,"sito dell'organizzatore o dell'evento":1}
SRC={'Fonte locale':0,'Comune di Roma':1,'Romatoday → sorgente':2,'Facebook':3,'Romatoday (scheda)':4}
def src(r): 
    f=str(g(r,'fonte') or '')
    return 'Fonte locale' if f.startswith('Fonte locale') else 'Romatoday → sorgente' if f.startswith('Romatoday →') else 'Romatoday (scheda)' if f.startswith('Romatoday') else 'Comune di Roma' if f.startswith('Comune') else 'Facebook'
rows=[[c.value for c in row] for row in ws.iter_rows(min_row=2)]
if 'riga_principale_proposta' not in h:
    ws.cell(1,len(h)+1,'riga_principale_proposta').font=Font(bold=True); h.append('riga_principale_proposta'); rows=[r+[None] for r in rows]
groups=collections.defaultdict(list)
for i,r in enumerate(rows):
    if g(r,'gruppo_doppione'): groups[g(r,'gruppo_doppione')].append(i)
def key(i):
    r=rows[i]; return (RANK.get(str(g(r,'rintracciabile_alla_fonte')),2), SRC[src(r)], i)
n=0
for i,r in enumerate(rows):
    gid=g(r,'gruppo_doppione')
    if not gid: val='sì'
    else:
        best=min(groups[gid],key=key); val='sì' if best==i else f'no: comanda {src(rows[best])}'
        n+= val!='sì'
    ws.cell(i+2,h.index('riga_principale_proposta')+1,val)
wb.save(UNICO); print('righe',len(rows),'secondarie',n,'gruppi',len(groups))
c=collections.Counter(); 
for r in rows:
    pass
