# DEC-026 — Posizione su Roma Today (Citynews) come fonte di eventi

Status: OPEN (OWNER_DECISION_REQUIRED)
Blocks: il flusso continuo del blocco eventi per il canale Roma Today; la rilettura delle
168 schede senza fonte.

Context: Roma Today è l'aggregatore con più schede evento non rintracciabili altrove (168
su 324 a ottobre 2026: redazione che riscrive il comunicato senza linkare). Il robots.txt
di Citynews vieta scraping, text and data mining e usi per AI senza licenza scritta; il
registro fonti lo classifica «nessun canale senza licenza». Il 23 ottobre 2026 l'owner ha
autorizzato una lettura una tantum delle 324 schede per i soli campi di scheda (Dove,
Quando, Prezzo, Sito web), promotore e link esterni; nessun testo conservato; i titoli non
entrano nel repository (DEC-022). La ricerca uno a uno del 24 ottobre ha mostrato che per
127 di quelle schede non esiste una pagina non-aggregatore che citi l'evento.

Question: che cosa fa QN con Roma Today d'ora in poi?
  Options:
  a) nessuna lettura, né regolare né una tantum, finché non c'è una licenza scritta di
     Citynews; gli eventi che vivono solo lì non entrano in QN;
  b) chiedere la licenza a Citynews (riuso dei soli campi di scheda con credito e link,
     nessun testo) e, nell'attesa, a);
  c) letture una tantum autorizzate caso per caso dall'owner, come il 23 ottobre, per i
     soli campi di scheda, con registrazione della data e del perimetro in questo file.
  Claude recommendation: b). a) è la regola che già vale; c) somiglia a una lettura
  regolare fatta a pezzi e il robots.txt non distingue.

Impact: a) e b) lasciano 168 eventi al mese fuori finché l'organizzatore non pubblica
altrove; la ricerca del 24 ottobre dice che di norma non lo fa.

Decided by: — · Date: — · Affected components: `docs/wiki/fonti-eventi/aggregatori.md`,
registro fonti (voce Roma Today), flusso continuo del blocco eventi.
