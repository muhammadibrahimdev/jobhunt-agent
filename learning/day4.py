from llm import ask_json
from utils import read_cv

cv = read_cv()
job = read_cv("job.txt")

system = """You are a strict recruiter. Compare a CV to a job description.
Only use skills that are actually written in the CV. Never invent anything.
Reply in JSON only, with exactly these keys:
score (integer 0 to 100),
matched_skills (list of strings),
missing_skills (list of strings),
reason (one short sentence)."""

user = f"CV:\n{cv}\n\nJOB DESCRIPTION:\n{job}"

result = ask_json(system, user)

print("Score:", result["score"])
print("Matched:", result["matched_skills"])
print("Missing:", result["missing_skills"])
print("Reason:", result["reason"])