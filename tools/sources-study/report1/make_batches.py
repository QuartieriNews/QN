# Splits report1/manifest_report1.csv into reading batches of 40-60 items for the Opus subagents
# (feasibility note §9.6, Report 1): report1/batches/L<nn>.txt, one document id per line.
import csv, os, sys
S=os.environ['QN_NET']; R=S+'/report1'; os.makedirs(R+'/batches',exist_ok=True)
SIZE=int(sys.argv[1]) if len(sys.argv)>1 else 50
rows=list(csv.DictReader(open(R+'/manifest_report1.csv',encoding='utf-8')))
# One source per batch: the reading rules differ by block, and a mixed batch costs the subagent a
# context switch per item.
by={}
for r in rows: by.setdefault(r['fonte'],[]).append(r)
n=0; index=[]
for fonte in sorted(by):
    items=sorted(by[fonte],key=lambda r:(r.get('data_pubblicazione') or '', r['id']))
    for k in range(0,len(items),SIZE):
        n+=1; chunk=items[k:k+SIZE]
        open(f'{R}/batches/L{n:02d}.txt','w').write('\n'.join(r['id'] for r in chunk)+'\n')
        index.append((f'L{n:02d}',fonte,len(chunk)))
with open(R+'/batches/_index.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['lotto','fonte','item']); w.writerows(index)
print(n,'lotti,',sum(i[2] for i in index),'item')
for l,fo,c in index: print(' ',l,fo,c)
