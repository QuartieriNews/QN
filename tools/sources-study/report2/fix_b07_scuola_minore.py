# Correzione singola, DEC-102. Una riga del lotto B07 portava fra i `luoghi` il nome di un liceo che
# nell'atto non e' la sede di un servizio ma **il luogo di una vicenda personale che riguarda uno
# studente minorenne** (un principio di sospensione per il mancato riconoscimento della carriera
# alias). La riga non racconta quella vicenda, quindi non e' una violazione in atto; ma il nome
# della scuola in quella colonna non serve al fatto che la riga afferma — la riapertura degli
# sportelli in tre Municipi — e accostato all'episodio, che e' pubblico, contribuisce a
# identificare un minore. DEC-102: un nome non e' l'unico modo di identificare una persona.
# Trovato da un lettore delle registrazioni, che aveva escluso la stessa vicenda dal proprio file e
# si e' accorto che rientrava dal ramo atti.
import csv, os, shutil

F = os.environ['QN_NET'] + '/report2/out/B07_atti.csv'
shutil.copy(F, F + '.prima_del_fix_scuola')
DA_TOGLIERE = '; Liceo Aristofane'

righe = list(csv.reader(open(F, encoding='utf-8')))
tocc = 0
for r in righe:
    for i, v in enumerate(r):
        if DA_TOGLIERE in v:
            r[i] = v.replace(DA_TOGLIERE, ''); tocc += 1
with open(F, 'w', newline='', encoding='utf-8') as fh:
    csv.writer(fh).writerows(righe)
print('celle corrette:', tocc, '(attesa 1)')
