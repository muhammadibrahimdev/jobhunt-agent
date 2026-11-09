import json
import os
import sys
from safe_letter import safe_cover_letter
from utils import read_cv

with open("profile.json", encoding="utf-8") as f:
    profile = json.load(f)

job_path = sys.argv[1]
result = safe_cover_letter(profile, read_cv(job_path))

print(result["letter"])
print("\nFix rounds used:", result["rounds"])
print("Passed checks:", result["report"]["passed"])
if not result["report"]["passed"]:
    print("Still flagged:", json.dumps(result["report"], indent=2))

os.makedirs("output", exist_ok=True)
name = os.path.splitext(os.path.basename(job_path))[0]
with open(f"output/safe_cover_{name}.txt", "w", encoding="utf-8") as f:
    f.write(result["letter"])
print(f"Saved output/safe_cover_{name}.txt")