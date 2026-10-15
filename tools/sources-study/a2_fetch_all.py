import os, subprocess, time, csv, sys, re
S=__import__('os').environ['QN_NET']
D=S+'/A2_all'; T=S+'/A2_text'; os.makedirs(T,exist_ok=True)
log=open(D+'/_fetch.log','a')
rows=[l.rstrip('\n').split('\t') for l in open(D+'/_list.tsv')]
n=0; falliti=0; badpdf=0
for name,url,fmt,d in rows:
    p=f'{D}/{name}.pdf'
    if os.path.exists(p) and os.path.getsize(p)>1000: continue
    r=subprocess.run(['curl','-sS','-f','--max-time','90','-o',p,url],capture_output=True); n+=1   # -f: un errore HTTP non e' un PDF
    if r.returncode!=0 or not os.path.exists(p) or os.path.getsize(p)<1000:
        log.write(f'FAIL {name} (curl {r.returncode})\n'); log.flush(); falliti+=1
        if os.path.exists(p): os.remove(p)   # niente corpo di errore al posto del PDF
    if n%50==0: log.write(f'{n} scaricati {time.strftime("%H:%M:%S")}\n'); log.flush()
    time.sleep(1.3)
log.write(f'DOWNLOAD DONE {n} nuovi {time.strftime("%H:%M:%S")}\n'); log.flush()
import fitz
for name,url,fmt,d in rows:
    p=f'{D}/{name}.pdf'; out=f'{T}/{name}.txt'
    if os.path.exists(out) or not os.path.exists(p): continue
    try: doc=fitz.open(p)
    except Exception as e: log.write(f'BADPDF {name} {e}\n'); badpdf+=1; continue
    pages=[pg.get_text() for pg in doc]
    scan = sum(len(x.strip()) for x in pages) < 40*max(1,len(pages))
    txt=[]
    for k,pg in enumerate(doc):
        if scan:
            png=f'{T}/_tmp_{os.getpid()}.png'; pg.get_pixmap(dpi=300).save(png)
            r=subprocess.run(['tesseract',png,'-','-l','ita'],capture_output=True,text=True); os.remove(png)
            txt.append(f'=== pagina {k+1} (OCR Tesseract) ===\n'+r.stdout)
        else: txt.append(f'=== pagina {k+1} ===\n'+pages[k])
    open(out,'w').write('\n'.join(txt))
log.write(f'TEXT DONE {time.strftime("%H:%M:%S")}: {falliti} download falliti, {badpdf} PDF illeggibili\n'); log.flush()
if falliti or badpdf:   # raccolta incompleta: dichiarata con il codice di uscita (HANDOFF §5)
    sys.exit(1)
