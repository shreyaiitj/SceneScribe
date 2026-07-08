import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from src.output_writer import save_results

results = [
    {
        "task_id": "v1",
        "captions": {
            "formal": "Test formal",
            "sarcastic": "Test sarcastic",
            "humorous_tech": "Test tech",
            "humorous_non_tech": "Test non-tech"
        }
    }
]

print("Saving results...")
success = save_results(results, "output/test_results.json")
print("Success:", success)
if success:
    print("File exists:", os.path.exists("output/test_results.json"))
    if os.path.exists("output/test_results.json"):
        print("File size:", os.path.getsize("output/test_results.json"))
        with open("output/test_results.json", "r") as f:
            print("Content:", f.read())
