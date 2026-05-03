import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"


def rewrite_query_llm(message, history):
    """
    Convert vague follow-ups into standalone queries.
    """

    last_summary = None

    for msg in reversed(history):
        if msg["role"] == "assistant" and msg.get("summary") != "fallback":
            last_summary = msg["summary"]
            break

    # No useful history → no rewrite
    if not last_summary:
        print("[DEBUG] rewrite skipped (no summary)")
        return message

    prompt = f"""
You are a query rewriting assistant.

Convert the user's question into a standalone query using context.

Rules:
- Max 10 words
- Use ONLY the context given
- DO NOT add new information
- Output ONLY the rewritten query

Context:
{last_summary}

User question:
{message}

Rewritten query:
"""

    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 30,
                "temperature": 0.1
            }
        },
        timeout=60
    )

    resp.raise_for_status()
    rewritten = resp.json().get("response", "").strip()

    if not rewritten:
        rewritten = f"{last_summary} {message}"

    print("[DEBUG] rewritten_query:", rewritten)

    return rewritten