import json
from matcher import match_job
from tailor import tailor_cv
from bullets import rewrite_bullets
from safe_letter import safe_cover_letter
from utils import read_cv

def load_profile(path="profile.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def prepare_application(job_text, min_score=40):
    profile = load_profile()
    cv_text = read_cv()
    out = {"errors": []}

    match = match_job(cv_text, job_text)
    out["match"] = match
    if "error" in match:
        out["errors"].append("match:" + match["error"])
        return out

    if match["score"] < min_score:
        out["skipped"] = True
        return out

    steps = {
        "tailored": lambda: tailor_cv(profile, job_text),
        "bullets": lambda: rewrite_bullets(profile, job_text),
        "letter": lambda: safe_cover_letter(profile, job_text),
    }

    for name, fn in steps.items():
        try:
            out[name] = fn()
        except Exception as e:
            out["errors"].append(f"{name}: {e}")
    return out



