from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def rewrite_query_llm(message, history):
    """
    Convert vague follow-ups into standalone queries.
    """

    last_summary = None

    for msg in reversed(history):
        if msg["role"] == "assistant" and msg.get("summary") not in {"fallback", "smalltalk"}:
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

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    rewritten = response.output_text.strip()
    if not rewritten:
        rewritten = f"{last_summary} {message}"

    print("[DEBUG] rewritten_query: ", rewritten)
    return rewritten