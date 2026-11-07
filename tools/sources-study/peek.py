import re,sys,html as h
f=sys.argv[1]; maxlinks=int(sys.argv[2]) if len(sys.argv)>2 else 60
doc=open(f,encoding='utf-8',errors='replace').read()
t=re.search(r'<title>(.*?)</title>',doc,flags=re.S); print("TITLE:",h.unescape(t.group(1)).strip() if t else None)
body=re.sub(r'<script.*?</script>','',doc,flags=re.S); body=re.sub(r'<style.*?</style>','',body,flags=re.S)
links=re.findall(r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>',body,flags=re.S)
seen=set(); n=0
for href,txt in links:
    txt=re.sub(r'<[^>]+>',' ',txt); txt=h.unescape(re.sub(r'\s+',' ',txt)).strip()
    if not txt or (href,txt) in seen or href.startswith(('#','javascript')): continue
    seen.add((href,txt)); n+=1
    if n<=maxlinks: print(f"  [{href[:110]}] {txt[:90]}")
print("LINKS total distinct:",len(seen))
dates=re.findall(r'\b\d{1,2}[/.-]\d{1,2}[/.-]\d{4}\b|\b\d{1,2}\s+(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+\d{4}\b|\b\d{4}-\d{2}-\d{2}\b',body,flags=re.I)
print("DATES sample:",dates[:12],"| total",len(dates))
pag=re.findall(r'[^"\s]*(?:page=|pagina|/page/|pag=|offset=|start=)[^"\s]*',body,flags=re.I)
print("PAGINATION hints:",sorted(set(pag))[:10])
