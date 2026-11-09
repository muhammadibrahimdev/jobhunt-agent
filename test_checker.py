import json
from fact_checker import check_document

with open("profile.json", encoding="utf-8") as f:
    profile = json.load(f)

fake = "I have 7 years of Kubernetes experience and led a team of 12 engineers at Google."
print(json.dumps(check_document(profile, fake), indent=2))