import subprocess, sys, pathlib, tempfile
root=pathlib.Path(__file__).resolve().parents[1]
out=subprocess.check_output([sys.executable,str(root/'src'/'repository_review_context_minimap.py'),str(root/'examples'/'changed-files.txt')], text=True)
normalized=out.replace('\\','/')
assert 'src/auth/session.py' in normalized and '| risk |' in out
diff='''diff --git a/src/auth/session.py b/src/auth/session.py
--- a/src/auth/session.py
+++ b/src/auth/session.py
@@ -1 +1 @@
-old
+new
'''
with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as f:
 f.write(diff); diff_path=f.name
out=subprocess.check_output([sys.executable,str(root/'src'/'repository_review_context_minimap.py'),diff_path,'--diff'], text=True)
assert 'src/auth/session.py' in out.replace('\\','/')
with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-16') as f:
 f.write(diff); diff_path=f.name
out=subprocess.check_output([sys.executable,str(root/'src'/'repository_review_context_minimap.py'),diff_path,'--diff'], text=True)
assert 'src/auth/session.py' in out.replace('\\','/')
print('ok repository-review-context-minimap')
