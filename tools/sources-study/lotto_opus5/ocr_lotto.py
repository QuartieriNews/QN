import csv, time, subprocess, fitz, os, sys
S=__import__('os').environ['QN_NET']; L=S+'/lotto_opus5'
rows=[r for r in csv.DictReader(open(L+'/manifest_B.csv')) if r['formato']=='scansione' and r['pdf']]
for r in rows:
    t=time.time(); doc=fitz.open(r['pdf']); out=[]
    for k,pg in enumerate(doc):
        png=f"{L}/log/_p{r['n']}_{k}.png"; pg.get_pixmap(dpi=300).save(png)
        res=subprocess.run(['tesseract',png,'-','-l','ita'],capture_output=True,text=True)
        out.append(f"=== pagina {k+1} (OCR Tesseract) ===\n"+res.stdout); os.remove(png)
    open(f"{L}/{r['testo']}",'w').write('\n'.join(out))
    with open(L+'/log/macchina.csv','a') as f: f.write(f"ocr_scansione,{r['n']},{round(time.time()-t,1)}\n")
    print(r['n'],len(doc),'pagine',round(time.time()-t,1),'s',flush=True)
print('OCR completato',flush=True)
