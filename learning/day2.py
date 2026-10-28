from utils import read_cv
import requests 

cv = read_cv()
skills = ["Python", "SQL", "LangGraph", "Docker"]
found = {}

for skill in skills:
    found[skill] = skill.lower() in cv.lower()
print(found)


url = "https://remotive.com/api/remote-jobs?search=python&limit=5"
data = requests.get(url).json()

for job in data["jobs"]:
    print(job["title"], "|", job["company_name"])
    print(job["url"])
    print()