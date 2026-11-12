import re
import requests
from matcher import match_job
from utils import read_cv

JOB_CACHE = {}

def clean_html(text):
    return re.sub(r"<[^>]+>", " ", text or "").strip()


# def search_remote_jobs(query, limit=3):
#     data = requests.get(
#         "https://remotive.com/api/remote-jobs",
#         params={"search": query, "limit": limit},
#         timeout=15
#     ).json()

#     results = []
#     for job in data.get("jobs", [])[:limit]:
#         job_id = str(job["id"])
#         JOB_CACHE[job_id] = clean_html(job["description"])[:3000]
#         results.append({
#             "id": job_id,
#             "title": job["title"],
#             "company": job["company_name"],
#             "url": job["url"],
#         })

    return results

def search_remote_jobs(query, limit=3):
    limit = min(limit, 5)
    data = requests.get(
        "https://remotive.com/api/remote-jobs",
        params={"category": "software-dev", "limit": 100},
        timeout=15,
    ).json()

    words = query.lower().split()
    scored = []
    for job in data.get("jobs", []):
        text = (job["title"] + " " + " ".join(job.get("tags", []))).lower()
        hits = sum(1 for w in words if re.search(r"\b" + re.escape(w) + r"\b", text))
        if hits > 0:
            scored.append((hits, job))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for hits, job in scored[:limit]:
        job_id = str(job["id"])
        JOB_CACHE[job_id] = clean_html(job["description"])[:3000]
        results.append({
            "id": job_id,
            "title": job["title"],
            "company": job["company_name"],
            "url": job["url"],
        })
    return results


def score_job(job_id):
    if job_id not in JOB_CACHE:
        return {"error": "Unknown job id. Search first"}

    result = match_job(read_cv(), JOB_CACHE[job_id])

    if "error" in result:
            return result
    
    return {
         "score": result["score"],
         "matched_skills": result["matched_skills"],
         "missing_skills": result["missing_skills"],
     }

FUNCTIONS = {
     "search_remote_jobs": search_remote_jobs,
     "score_job": score_job,
}


TOOLS = [
     {
          "type": "function",
          "function":{
               "name": "search_remote_jobs",
               "description": "Search remote jobs by keyword. Returns id, title, company, and url.",
               "parameters":{
                    "type": "object",
                    "properties":{
                         "query":  {"type": "string", "description": "Search keyword, e.g. python"},
                         "limit": {"type": "integer", "description": "Number of jobs, max 5"}
                    },
                    "required": ["query"],
               },
          },    
     },
         {
        "type": "function",
        "function": {
            "name": "score_job",
            "description": "Score the user's CV against a job found by search_remote_jobs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The id returned by search_remote_jobs",
                    },
                },
                "required": ["job_id"],
            },
        },
    },
]