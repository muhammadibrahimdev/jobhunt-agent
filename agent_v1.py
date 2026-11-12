import json
import sys
from llm import client, model
from tools import FUNCTIONS, TOOLS

SYSTEM = """You are a job hunting assistant.
Use tools to find jobs and score them against the user's CV.
Never guess scores or job details. Always use the tools.
At the end, give a short ranked list with title, company, score, and url. The user's CV is already loaded. score_job uses it automatically. Never ask the user for their CV.
Search once. Then call score_job for every job returned. Then give the ranked list.
If results are poor or empty, say so honestly. Never keep searching."""


def run_agent(task, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": c.id,
                    "type": "function",
                    "function": {"name": c.function.name, "arguments": c.function.arguments},
                }
                for c in msg.tool_calls
            ],
        })

        for call in msg.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments or "{}")
                result = FUNCTIONS[name](**args)
            except Exception as e:
                result = {"error": str(e)}
            print(f"[step {step + 1}] {name}({call.function.arguments})")
            # print("   ->", json.dumps(result, ensure_ascii=False)[:200])
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

    return "Stopped: too many steps."


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Find 3 remote python jobs and tell me which fits me best."
    print("\n" + run_agent(task))