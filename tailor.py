import json
from llm import ask_json

SYSTEM = """You tailor a CV to a job.
Rules:
- Use ONLY facts found in the profile. Never invent skills, tools, numbers, employers, or dates.
- Write in plain, confident language.
Reply in JSON only, with exactly these keys:
summary (2 to 3 sentences, aimed at this job),
skills (skills from the profile, most relevant to the job first, max 12),
top_projects (up to 3 project names from the profile, most relevant first)"""

def tailor_cv(profile, job_text):
    user = f"PROFILE:\n{json.dumps(profile, ensure_ascii=False)}\n\nJOB DESCRIPTION:\n{job_text}"
    result = ask_json(SYSTEM, user)

    allowed = {s.lower() for s in profile["skills"]}
    result["skills"] = [s for s in result["skills"] if s.lower() in allowed]
    return result