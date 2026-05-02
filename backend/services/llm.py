import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

def generate_response(prompt: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt":prompt,
            "stream": False
        },
        timeout=300
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()

def needs_rewrite(query: str):
    query = query.lower()
    vague_words = ["it", "that", "again", "explain", "why", "how", "understand"]
    return any(word in query for word in vague_words)


def rewrite_query(query, history):
    recent = history[-4:]

    history_text = ""
    for msg in recent:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
Given the conversation and the latest user query, rewrite the query to be fully self-contained.

Conversation:
{history_text}

User Query:
{query}

Rewritten Query:
"""

    return generate_response(prompt).strip()

def build_prompt(query: str, contexts: list[str], history: list[dict]) -> str:
    context_text = "\n\n".join(contexts)
    recent = history[-6:]
    history_text = ""
    for msg in recent:
        history_text += f"{msg['role']}: {msg['content']}\n"
    
    prompt = f"""
You are a veterinary assistant helping dairy farmers.

STRICT RULES:
- Use ONLY the provided context.
- Do NOT add outside knowledge.
- If the answer is not clearly in the context, reply EXACTLY: "We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."

Context:
{context_text}

Converstaion:
{history_text}

Question:
{query}

Answer:
"""
    return prompt
