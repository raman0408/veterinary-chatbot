import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_response(prompt: str) -> str:
    print("--- LLM Call Start ---")
    start = time.time()
    response = client.responses.create(
        model="gpt-4o-mini",
        input = prompt
    )
    elapsed = time.time() - start
    print(f"LLM Time: {elapsed:.2f}s")
    print(f"Prompt length: {len(prompt)}")
    print("--- LLM Call End ---")

    return response.output_text

def parse_response(raw: str):
    if "SUMMARY:" in raw:
        parts = raw.split("SUMMARY:")
        answer = parts[0].replace("ANSWER:", "").strip()
        summary = parts[1].strip()
    else:
        # fallback parsing
        answer = raw.strip()
        summary = raw.strip()

    return answer, summary



def build_prompt(query: str, contexts: list[str], history: list[dict]) -> str:
    context_text = "\n\n".join(contexts)
    recent = history[-2:]

    history_text = ""
    for msg in recent:
        if msg["role"] == "user":
            history_text += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            summary = msg.get("summary", "")
            if summary and summary != "fallback":
                history_text += f"Bot summary: {summary}\n"
    
    prompt = f"""
You are a veterinary assistant helping dairy farmers.

RULES:
- Use ONLY the provided context.
- If the answer is not clearly in the context, reply EXACTLY: 
"We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."
Keep ANSWERS SHORT AND CONCISE (2-3 sentences)
Also generate a SHORT SUMMARY (4-8 words) capturing the key topic.

Context:
{context_text}

Converstaion:
{history_text}

Question:
{query}

Return in EXACT format:

ANSWER:
<answer>

SUMMARY:
<short summary>
"""
    return prompt
