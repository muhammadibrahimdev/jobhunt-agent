import csv
import glob
import time
from matcher import match_job
from utils import read_cv

cv = read_cv()
rows = []

for path in sorted(glob.glob("jobs/*.txt")):
    job = read_cv(path)
    result = match_job(cv, job)
    if "error" in result:
        print(path, "failed:", result["error"])
        continue
    rows.append({
        "file": path,
        "score": result["score"],
        "matched": ", ".join(result["matched_skills"]),
        "missing": ", ".join(result["missing_skills"]),
        "reason": result["reason"],
    })
    print(path, result["score"])
    time.sleep(3)

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)