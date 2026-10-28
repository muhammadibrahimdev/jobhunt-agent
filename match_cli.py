import sys
from matcher import match_job
from utils import read_cv

cv = read_cv()

if len(sys.argv) > 1:
    job = read_cv(sys.argv[1])
else:
    print("Paste the job description, then press Enter and Ctrl+Z (Windows) or Ctrl+D (Mac/Linux):")
    job = sys.stdin.read()

result = match_job(cv, job)

if "error" in result:
    print("Failed:", result["error"])
else:
    print("\nMATCH REPORT")
    print("Score:", result["score"], "/ 100")
    print("Matched:", ", ".join(result["matched_skills"]))
    print("Missing:", ", ".join(result["missing_skills"]))
    print("Strengths:", ", ".join(result["strengths"]))
    print("Reason:", result["reason"])