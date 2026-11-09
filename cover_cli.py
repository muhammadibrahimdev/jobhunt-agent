import json
import os
import sys
from cover_letter import write_cover_letter
from utils import read_cv

with open("profile.json", encoding="utf-8") as f:
    profile = json.load(f)

job_path = sys.argv[1]
job = read_cv(job_path)
result = write_cover_letter(profile, job)

print(result["letter"])
print("\nWords:", result["words"])
if result["suspicious_numbers"]:
    print("WARNING, numbers not in your profile:", result["suspicious_numbers"])

os.makedirs("output", exist_ok=True)
name = os.path.splitext(os.path.basename(job_path))[0]
with open(f"output/cover_{name}.txt", "w", encoding="utf-8") as f:
    f.write(result["letter"])
print(f"Saved output/cover_{name}.txt")