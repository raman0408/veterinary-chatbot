from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
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

Your job is ONLY to clarify vague follow-up questions using conversation context.

IMPORTANT:
- Preserve the ORIGINAL topic of the user's question.
- NEVER replace the user's topic with context topic.
- If the user's query introduces a NEW topic, keep it unchanged.
- ONLY rewrite ambiguous references like:
  - it
  - this
  - explain more
  - symptoms
  - prevention

Rules:
- Max 10 words
- Use ONLY context when resolving ambiguous references
- DO NOT invent or substitute topics
- Output ONLY the rewritten query

Context:
{last_summary}

User question:
{message}

Rewritten query:
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=20
    )
    rewritten = response.choices[0].message.content.strip()
    rewritten = rewritten.replace("```", "")
    rewritten = rewritten.replace("Rewritten query:", "")
    rewritten = rewritten.strip()
    
    if not rewritten:
        rewritten = f"{last_summary} {message}"

    print("[DEBUG] rewritten_query: ", rewritten)
    return rewritten