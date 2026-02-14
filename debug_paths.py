import os

base_dir = os.path.dirname(os.path.abspath("backend/app.py"))
frontend_dir = os.path.join(base_dir, "..", "frontend")
resolved_frontend = os.path.abspath(frontend_dir)
index_path = os.path.join(resolved_frontend, "index.html")

print(f"Base Dir: {base_dir}")
print(f"Frontend Dir (raw): {frontend_dir}")
print(f"Frontend Dir (resolved): {resolved_frontend}")
print(f"Index Path: {index_path}")
print(f"Index Exists: {os.path.exists(index_path)}")
