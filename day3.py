from llm import ask
from utils import read_cv

cv = read_cv()

system = "You are a career coach, Only use facts found in the CV. Never invent anything"
user = f"Summarize this CV in exactly 5 lines using: Skill: [name] | Evidence: [CV proof].\n\nCV:\n{cv}"

print(ask(user, system))