from llm import ask_json

SYSTEM = """You are a strict recruiter. Compare a CV to a job description.
Rules:
- Only use skills and experience that are written in the CV.
- Never invent or assume anything.
- Be honest: if a required skill is not in the CV, list it as missing.
- Ignore non-skill requirements (owning a laptop, location, visa, salary).
- List at most 8 missing skills, most important first.
- Score by required skills first, nice-to-haves second.
Reply in JSON only, with exactly these keys:
score (integer 0 to 100),
matched_skills (list of strings),
missing_skills (list of strings),
strengths (list of up to 3 short strings),
reason (one short sentence)."""

def match_job(cv, job_text):
    user = f"CV:\n{cv}\n\nJOB DESCRIPTION:\n{job_text}"
    try:
        result = ask_json(SYSTEM, user)
    except Exception as e:
        return {"error": str(e)}

    score = result.get("score", 0)
    if not isinstance(score, int):
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = 0
    result["score"] = max(0, min(100, score))
    return result