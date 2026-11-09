import json
import re
from llm import ask_json

SYSTEM = """You rewrite CV bullet points to fit a specific job.
Rules:
- Keep every fact true. Use ONLY information in the original bullets.
- Never add new tools, skills, numbers, results, or responsibilities.
- You may reorder, shorten, and use the job's wording only when it describes the same thing.
- Start each bullet with a strong action verb. Max 30 words per bullet. Keep technical details (architecture, auth, frameworks) that match the job.
- Return ALL bullets, with the most relevant first. Do not drop any.
Reply in JSON only, with exactly one key: items
(a list of objects with: id (copied unchanged), bullets (list of strings))."""


def numbers_in(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def safe_bullets(original, new):
    allowed = numbers_in(" ".join(original))
    kept = []
    for b in new:
        if numbers_in(b) <= allowed:
            kept.append(b)
        else:
            print("REJECTED:", b)
    return kept


def rewrite_bullets(profile, job_text):
    items = []
    for i, exp in enumerate(profile.get("experience", [])):
        if exp.get("bullets"):
            items.append({"id": f"exp-{i}", "bullets": exp["bullets"]})
    for i, p in enumerate(profile.get("projects", [])):
        if p.get("description"):
            parts = re.split(r"(?<=[.!?])\s+", p["description"])
            items.append({
                "id": f"proj-{i}",
                "bullets": [s.strip() for s in parts if s.strip()],
            })

    user = f"ITEMS:\n{json.dumps(items, ensure_ascii=False)}\n\nJOB DESCRIPTION:\n{job_text}"
    result = ask_json(SYSTEM, user)
    new = {it["id"]: it.get("bullets", []) for it in result.get("items", [])}

    output = {}
    for item in items:
        fresh = safe_bullets(item["bullets"], new.get(item["id"], []))
        output[item["id"]] = fresh or item["bullets"]
    return items, output