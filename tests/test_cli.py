import subprocess, sys, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
out=subprocess.check_output([sys.executable,str(root/'src'/'repository_review_context_minimap.py'),str(root/'examples'/'changed-files.txt')], text=True)
normalized=out.replace('\\','/')
assert 'src/auth/session.py' in normalized and '| risk |' in out
print('ok repository-review-context-minimap')
