import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    print("DEBUG: Importing src.main...")
    from src.main import main
    print("DEBUG: Import successful. Calling main()...")
    res = main()
    print("DEBUG: main() returned:", res)
    import os
    results_path = "output/results.json"
    print("DEBUG: file exists:", os.path.exists(results_path))
    if os.path.exists(results_path):
        print("DEBUG: file size:", os.path.getsize(results_path))
        with open(results_path, "r", encoding="utf-8") as f:
            print("DEBUG: file content:", repr(f.read()))
    sys.exit(res)
except Exception as e:
    print("DEBUG: Caught exception:")
    traceback.print_exc()
    sys.exit(1)
except BaseException as e:
    print("DEBUG: Caught BaseException (like SystemExit):")
    traceback.print_exc()
    sys.exit(1)
