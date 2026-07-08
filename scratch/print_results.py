import os
path = 'output/results.json'
print("Exists:", os.path.exists(path))
if os.path.exists(path):
    print("Size:", os.path.getsize(path))
    with open(path, 'r', encoding='utf-8') as f:
        print("Content:", repr(f.read()))
