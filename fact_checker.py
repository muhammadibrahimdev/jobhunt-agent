import json 
import re
from llm import ask_json


TECH_TERMS = [
    "python", "javascript", "typescript", "react", "react native", "next.js",
    "node.js", "express", "mongodb", "postgresql", "mysql", "sql", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "nginx",
    "websockets", "socket.io", "graphql", "fastapi", "django", "flask",
    "flutter", "dart", "supabase", "firebase", "langchain", "langgraph",
    "rag", "llm", "tensorflow", "pytorch", "java", "c++", "c#", "go",
    "rust", "swift", "kotlin", "tailwind", "git", "ci/cd", "terraform",
]

SYSTEM = """You are a strict fact-checker for job application documents.
You receive a PROFILE (the only source of truth) and a DOCUMENT written from it.
Find every claim in the DOCUMENT that the PROFILE does not support.
Check skills, tools, numbers, employers, job titles, dates, achievements, and responsibilities.
Rules:
- Rewording is fine. New facts are not.
- Do not flag greetings, opinions, or sentences that only repeat what the job asks for.
Reply in JSON only, with exactly one key: unsupported
(a list of objects with: text (exact quote from the DOCUMENT), reason (short))."""

def has_term(text, term):
    pattern = r"(?<![\w])" + re.escape(term) + r"(?![\w])"
    return re.search(pattern, text) is not None

def keyword_check(profile, document):
    profile_text = json.dumps(profile , ensure_ascii=False).lower()
    doc = document.lower()
    return sorted(
        t for t in TECH_TERMS
        if has_term(doc, t) and not has_term(profile_text, t)
    )


def number_check(profile, document):
    nums = lambda s: set(re.findall(r"\d+(?:\.\d+)?", s))
    return sorted(nums(document) - nums(json.dumps(profile, ensure_ascii=False)))


def check_document(profile, document):
    user = f"Profile:\n{json.dumps(profile, ensure_ascii=False)}\n\nDocument:\n{document}"
    try:
        llm_flags = ask_json(SYSTEM, user).get("unsupported", [])
    except Exception as e:
        print("LLM check failed:", e)
        llm_flags = []

    keywords = keyword_check(profile, document)
    numbers = number_check(profile, document)

    return{
        "llm_flags": llm_flags,
        "keyword_flags": keywords,
        "number_flags": numbers,
        "passed": not (llm_flags or keywords or numbers)
    }