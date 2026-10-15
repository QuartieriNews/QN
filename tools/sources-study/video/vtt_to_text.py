import sys,re,glob,os
def convert(path, step=10):   # marcatori a 10 secondi (HANDOFF §4, punto 4)
    lines=open(path,encoding='utf-8',errors='replace').read().splitlines()
    out=[]; last=-step; words=0; cur=None
    for ln in lines:
        m=re.match(r'(\d+):(\d+):(\d+)\.(\d+) --> ',ln)
        if m: cur=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3)); continue
        if not ln.strip() or ln.strip().isdigit() or ln.startswith('WEBVTT'): continue
        if cur is not None and cur-last>=step: out.append(f'\n[{cur//60:02d}:{cur%60:02d}] '); last=cur
        out.append(ln.strip()+' '); words+=len(ln.split())
    return ''.join(out), words, cur or 0
for p in sys.argv[1:]:
    t,w,d=convert(p); open(p[:-4]+'.txt','w').write(t); print(os.path.basename(p), 'parole',w,'durata_s',d,'wpm',round(w/(d/60)) if d else '')
