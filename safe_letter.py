import json
from llm import ask_json
from cover_letter import write_cover_letter
from fact_checker import check_document


FIX_SYSTEM = """You fix cover letters.
Rewrite the letter so it contains ONLY facts from the profile.
Remove or rephrase every problem listed. Keep the same tone and 150 to 220 words.
Reply in JSON only, with exactly one key: letter (a string)."""


def revise(profile, letter, report):
    problems = {
        "unsupported_claims":report["llm_flags"],
        "tools_not_in_profile":report["keyword_flags"],
        "numbers_not_in_profile":report["number_flags"]
    }


    user = (
        f"PROFILE:\n{json.dumps(profile, ensure_ascii=False)}\n\n"
        f"LETTER:\n{letter}\n\nPROBLEMS:\n{json.dumps(problems, ensure_ascii=False)}"
    )

    return ask_json(FIX_SYSTEM,user).get("letter", letter)


def safe_cover_letter(profile, job_text, max_rounds=2):
    letter = write_cover_letter(profile, job_text)["letter"]
    report = check_document(profile, letter)
    rounds = 0

    while not report["passed"] and rounds <= max_rounds:
        letter = revise(profile, letter, report)
        report = check_document(profile, letter)
        rounds += 1

    return {"letter": letter, "report": report, "rounds": rounds}