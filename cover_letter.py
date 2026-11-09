import json
import re
from llm import ask_json

SYSTEM = """You write short, honest cover letters.
Rules:
- Use ONLY facts found in the profile. Never invent skills, tools, numbers, employers, or achievements.
- Do not claim skills that are not in the profile, even if the job asks for them.
- Length: 150 to 220 words, in 3 short paragraphs (hook, proof, close).
- Mention 2 real projects or experiences from the profile that match the job.
- Plain, confident tone. No cliches like "I am a passionate team player" or "I am writing to apply".
- Address the letter to "Hiring Team" unless a name is given in the job description.
- Sign off with the name from the profile.
Reply in JSON only, with exactly one key: letter (a string)."""


def numbers_in(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def write_cover_letter(profile, job_text):
    user = (
        f"PROFILE:\n{json.dumps(profile, ensure_ascii=False)}\n\n"
        f"JOB DESCRIPTION:\n{job_text}"
    )
    result = ask_json(SYSTEM, user)
    letter = result.get("letter", "").strip()

    allowed = numbers_in(json.dumps(profile, ensure_ascii=False))
    suspicious = sorted(numbers_in(letter) - allowed)

    return {
        "letter": letter,
        "words": len(letter.split()),
        "suspicious_numbers": suspicious,
    }