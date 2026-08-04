#!/usr/bin/env python
import argparse, pathlib, re, json
RISK=[('migration',3),('auth',3),('payment',3),('security',3),('config',2),('test',-1),('docs',-1)]
def analyze(paths):
 out=[]
 for p in paths:
  pp=pathlib.Path(p); parts=[x.lower() for x in pp.parts]; ext=pp.suffix.lower(); score=1
  reasons=[]
  for word,delta in RISK:
   if any(word in x for x in parts): score+=delta; reasons.append(word)
  if ext in ['.sql','.yaml','.yml','.toml','.lock']: score+=1; reasons.append(ext)
  owner='/' .join(pp.parts[:2]) if len(pp.parts)>1 else str(pp.parent or '.')
  out.append({'file':str(pp),'area':str(pp.parent or '.'),'suggested_owner_scope':owner,'risk_score':max(0,score),'reasons':reasons})
 return sorted(out,key=lambda x:(-x['risk_score'],x['file']))
def main():
 p=argparse.ArgumentParser(description='Build a compact review minimap from changed file paths.')
 p.add_argument('paths_file'); p.add_argument('--json', action='store_true')
 a=p.parse_args(); paths=[l.strip() for l in open(a.paths_file,encoding='utf-8') if l.strip() and not l.startswith('#')]
 rows=analyze(paths)
 if a.json: print(json.dumps({'files':rows,'total':len(rows),'hotspots':rows[:5]},indent=2))
 else:
  print('| risk | file | area | reasons |') ; print('|---:|---|---|---|')
  for r in rows: print(f"| {r['risk_score']} | {r['file']} | {r['area']} | {', '.join(r['reasons']) or '-'} |")
if __name__=='__main__': main()
