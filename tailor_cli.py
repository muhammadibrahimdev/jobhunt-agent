import json
import sys
from tailor import tailor_cv
from utils import read_cv

with open("profile.json", encoding="utf-8") as f:
    profile = json.load(f)

job = read_cv(sys.argv[1])
result = tailor_cv(profile, job)

print("SUMMARY:\n", result["summary"])
print("\nSKILLS:", ", ".join(result["skills"]))
print("\nTOP PROJECTS:", ", ".join(result["top_projects"]))