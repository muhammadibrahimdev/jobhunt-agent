import json
from llm import ask_json
from utils import read_cv

SYSTEM = """You extract structured data from a CV.
Only use information written in the CV. Never invent anything.
If a field is missing, use an empty string or empty list.
Reply in JSON only, with exactly these keys:
name, headline, summary,
skills (list of strings),
experience (list of objects with: title, company, dates, bullets (list of strings)),
projects (list of objects with: name, description, tech (list of strings)),
education (list of strings)"""

def parse_cv(text):
    return ask_json(SYSTEM, f"CV:\n{text}")

if __name__ == "__main__":
    profile = parse_cv(read_cv())
    with open("profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print("Saved profile.json")