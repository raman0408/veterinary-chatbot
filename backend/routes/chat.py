from fastapi import APIRouter
from backend.services.memory import load_history, append_message
from backend.services.rag import retrieve_with_scores
from backend.services.rewrite import rewrite_query_llm
from backend.services.llm import generate_response, build_prompt, parse_response

router = APIRouter()

THRESHOLD = 1.0
IMPROVEMENT_RATIO_THRESHOLD = 0.3
LOOSE_THRESHOLD = 1.2


FALLBACK_MESSAGE = "We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."


def is_vague_query(message: str):
    message = message.lower().strip()

    vague_patterns = [
        "explain", "repeat", "about", "that", 
        "this", "it", "more", "details", "else", 
        "again", "understand"
        
    ]

    short = len(message.split()) <= 2
    contains_vague = any(p in message for p in vague_patterns)

    return short or contains_vague


@router.post("/chat")
def chat(data: dict):
    phone = data.get("phone")
    message = data.get("message")

    # Load history
    history = load_history(phone)

    # Save user message
    append_message(phone, "user", message)

    history = load_history(phone)

    # -------- STEP 1: RAW RETRIEVAL --------
    contexts_q, scores_q = retrieve_with_scores(message)
    best_q = min(scores_q) if scores_q else float("inf")

    print(f"[DEBUG] best_q: {best_q}")

    vague = is_vague_query(message)
    print(f"[DEBUG] is_vague: {vague}")

    # -------- CASE 1: STRONG RAW MATCH --------
    if best_q < THRESHOLD:
        print("[DEBUG] Using original query")
        contexts = contexts_q

    # -------- CASE 2: VAGUE → REWRITE --------
    elif vague or best_q < LOOSE_THRESHOLD:
        print("[DEBUG] Vague query → rewriting")

        rewritten_query = rewrite_query_llm(message, history)

        contexts_hq, scores_hq = retrieve_with_scores(rewritten_query)
        best_hq = min(scores_hq) if scores_hq else float("inf")

        print(f"[DEBUG] best_hq: {best_hq}")

        improvement_ratio = (best_q - best_hq)/best_q if best_q != 0 else 0

        if best_hq < THRESHOLD and improvement_ratio > IMPROVEMENT_RATIO_THRESHOLD:
            print("[DEBUG] Rewrite accepted")
            contexts = contexts_hq
        else:
            print("[DEBUG] Rewrite rejected → fallback")
            append_message(phone, "assistant", FALLBACK_MESSAGE, summary="fallback")
            return {"response": FALLBACK_MESSAGE}

    # -------- CASE 3: NOT VAGUE + WEAK → FALLBACK --------
    else:
        print("[DEBUG] Not vague + weak match → fallback")
        append_message(phone, "assistant", FALLBACK_MESSAGE, summary="fallback")
        return {"response": FALLBACK_MESSAGE}

    # -------- LLM GENERATION --------
    prompt = build_prompt(message, contexts, history)
    raw = generate_response(prompt)
    answer, summary = parse_response(raw)

    append_message(phone, "assistant", answer, summary)

    return {
        "response": answer
    }