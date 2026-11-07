# json3 (YouTube ASR) -> plain text with [mm:ss] markers every ~30 s; prints stats (words, mean ASR confidence when present)
import json,sys
def convert(path, step=30):
    d=json.load(open(path)); out=[]; last=-step; words=0; confs=[]
    for ev in d.get('events',[]):
        segs=ev.get('segs') or []
        t=ev.get('tStartMs',0)/1000
        txt=''.join(s.get('utf8','') for s in segs).replace('\n',' ').strip()
        if not txt: continue
        for s in segs:
            if 'acAsrConf' in s: confs.append(s['acAsrConf'])
        words+=len(txt.split())
        if t-last>=step:
            out.append(f'\n[{int(t//60):02d}:{int(t%60):02d}] '); last=t
        out.append(txt+' ')
    text=''.join(out)
    return text, dict(words=words, events=len(d.get('events',[])), conf_mean=(sum(confs)/len(confs) if confs else None), conf_n=len(confs), dur_s=max((ev.get('tStartMs',0)+ev.get('dDurationMs',0))/1000 for ev in d.get('events',[])) if d.get('events') else 0)
if __name__=='__main__':
    for p in sys.argv[1:]:
        text,st=convert(p)
        open(p.replace('.json3','.txt'),'w').write(text)
        print(p, st, '| wpm=', round(st['words']/(st['dur_s']/60)) if st['dur_s'] else '')
