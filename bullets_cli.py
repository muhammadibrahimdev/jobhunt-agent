import json
import sys
from bullets import rewrite_bullets
from utils import read_cv

with open("profile.json", encoding="utf-8") as f:
    profile = json.load(f)

job = read_cv(sys.argv[1])
items, output = rewrite_bullets(profile, job)

for item in items:
    print("\n==", item["id"])
    print("BEFORE:")
    for b in item["bullets"]:
        print(" -", b)
    print("AFTER:")
    for b in output[item["id"]]:
        print(" -", b)