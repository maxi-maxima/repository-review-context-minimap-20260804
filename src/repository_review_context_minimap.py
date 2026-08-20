#!/usr/bin/env python
import argparse, pathlib, re, json, fnmatch
RISK=[('migration',3),('auth',3),('payment',3),('security',3),('config',2),('test',-1),('docs',-1)]
def read_lines(path):
 for encoding in ('utf-8-sig','utf-16'):
  try:
   return [l.strip() for l in open(path,encoding=encoding) if l.strip()]
  except UnicodeError:
   pass
 raise UnicodeError(f'could not decode {path} as UTF-8 or UTF-16')
def paths_from_diff(lines):
 paths=[]
 for line in lines:
  if line.startswith('+++ b/'):
   paths.append(line[6:].strip())
 return paths

def load_codeowners(path):
 rules=[]
 if not path:
  return rules
 for raw in open(path, encoding='utf-8'):
  line=raw.strip()
  if not line or line.startswith('#'):
   continue
  parts=line.split()
  if len(parts)<2:
   continue
  rules.append((parts[0], parts[1:]))
 return rules

def codeowners_for(path, rules):
 owners=[]
 normalized=path.replace('\\','/')
 for pattern, candidates in rules:
  pat=pattern.lstrip('/').replace('\\','/')
  if pat.endswith('/'):
   matched=normalized.startswith(pat)
  elif '/' not in pat:
   matched=fnmatch.fnmatch(pathlib.PurePosixPath(normalized).name, pat) or fnmatch.fnmatch(normalized, pat)
  else:
   matched=fnmatch.fnmatch(normalized, pat) or fnmatch.fnmatch('/'+normalized, pattern)
  if matched:
   owners=candidates
 return owners

def default_codeowners(paths_file):
 base=pathlib.Path(paths_file).resolve().parent
 for candidate in [base/'.github'/'CODEOWNERS', base/'CODEOWNERS']:
  if candidate.exists():
   return candidate
 return None

def analyze(paths, codeowners=None):
 out=[]
 for p in paths:
  pp=pathlib.Path(p); parts=[x.lower() for x in pp.parts]; ext=pp.suffix.lower(); score=1
  reasons=[]
  for word,delta in RISK:
   if any(word in x for x in parts): score+=delta; reasons.append(word)
  if ext in ['.sql','.yaml','.yml','.toml','.lock']: score+=1; reasons.append(ext)
  owner='/' .join(pp.parts[:2]) if len(pp.parts)>1 else str(pp.parent or '.')
  owners=codeowners_for(str(pp), codeowners or [])
  out.append({'file':str(pp),'area':str(pp.parent or '.'),'suggested_owner_scope':owner,'codeowners':owners,'risk_score':max(0,score),'reasons':reasons})
 return sorted(out,key=lambda x:(-x['risk_score'],x['file']))
def main():
 p=argparse.ArgumentParser(description='Build a compact review minimap from changed file paths.')
 p.add_argument('paths_file'); p.add_argument('--json', action='store_true'); p.add_argument('--diff', action='store_true', help='Read changed files from a unified diff file.')
 p.add_argument('--codeowners', help='Read CODEOWNERS rules and attach matching owners to each changed file.')
 a=p.parse_args(); lines=read_lines(a.paths_file)
 paths=paths_from_diff(lines) if a.diff else [l for l in lines if not l.startswith('#')]
 codeowners_path=pathlib.Path(a.codeowners) if a.codeowners else default_codeowners(a.paths_file)
 rows=analyze(paths, load_codeowners(codeowners_path) if codeowners_path else [])
 if a.json: print(json.dumps({'files':rows,'total':len(rows),'hotspots':rows[:5]},indent=2))
 else:
  print('| risk | file | area | owners | reasons |') ; print('|---:|---|---|---|---|')
  for r in rows: print(f"| {r['risk_score']} | {r['file']} | {r['area']} | {', '.join(r['codeowners']) or '-'} | {', '.join(r['reasons']) or '-'} |")
if __name__=='__main__': main()
