import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

def generate_response(prompt: str) -> str:
    print("\n--- LLM CALL START ---")
    start = time.time()

    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt":prompt,
            "stream": False,
            "option": {
                "num_predict":100,
                "temperature": 0.2,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        },
        timeout=180
    )
    end = time.time()

    print(f"LLM TIME: {end - start:.2f}s")
    print(f"Prompt length: {len(prompt)}")

    resp.raise_for_status()
    data = resp.json()

    print("--- LLM CALL END ---\n")
    return data.get("response", "").strip()

def parse_response(response: str):
    try:
        answer_part, summary_part = response.split("SUMMARY:")
        answer = answer_part.replace("ANSWER:", "").strip()
        summary = summary_part.strip()
    except:
        answer = response.strip()
        summary = ""
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
            if summary:
                history_text += f"Bot summary: {summary}\n"
    
    prompt = f"""
You are a veterinary assistant helping dairy farmers.

STRICT RULES:
- Use ONLY the provided context.
- Do NOT add outside knowledge.
- If the answer is not clearly in the context, reply EXACTLY: 
"We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."
Keep ANSWERS SHORT AND CONCISE (2-3 sentences)
Also generate a SHORT SUMMARY (4-8 words) capturing the key topic.

Return in EXACT format:

ANSWER:
<answer>

SUMMARY:
<short summary>

Context:
{context_text}

Converstaion:
{history_text}

Question:
{query}

Answer:
"""
    return prompt
