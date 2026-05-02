from fastapi import APIRouter
from backend.services.memory import load_history, append_message
from backend.services.rag import retrieve_with_scores, compute_similarity
from backend.services.llm import generate_response, build_prompt, parse_response

FALLBACK_MESSAGE = "We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."
THRESHOLD = 1.0
SIM_THRESHOLD = 0.6

router = APIRouter()

@router.post("/chat")
def chat(data: dict):
    phone = data.get("phone")
    message = data.get("message")

    # Load History
    history = load_history(phone)
    
    # Save user message
    append_message(phone, "user", message)

    # --------- Buid history summary ---------
    last_summary = None
    for msg in reversed(history):
        if msg["role"] == "assistant" and "summary" in msg:
            last_summary = msg["summary"]
            break
    
    # --------- Buid retrieval query ---------
    history_text = last_summary if last_summary else ""
    retrieval_query = f"{history_text} {message}"

    # --------- Dual retrieval ---------
    contexts_q, scores_q = retrieve_with_scores(message)
    contexts_hq, scores_hq = retrieve_with_scores(retrieval_query)

    best_q = min(scores_q) if scores_q else float("inf")
    best_hq = min(scores_hq) if scores_hq else float("inf")

    # --------- Similarity ---------
    sim_q_h = compute_similarity(message, last_summary)

    print(f"[DEBUG] Q={best_q}, HQ={best_hq}, QHSim={sim_q_h}")

    # --------- Decision Logic ---------

    # Case 1: Query is strong -> ignore history
    if best_q < THRESHOLD:
        contexts = contexts_q
    
    # Case 2: Weak query, history helps AND alligned
    elif best_hq < THRESHOLD and sim_q_h > SIM_THRESHOLD:
        contexts = contexts_hq
    
    # Case 3: History helps but NOT alligned -> reject
    elif best_hq < THRESHOLD and sim_q_h <= SIM_THRESHOLD:
        append_message(phone, "assistant", FALLBACK_MESSAGE, summary="fallback")
        return {"response": FALLBACK_MESSAGE}
    
    # Case 4: nothing useful
    else:
        append_message(phone, "assistant", FALLBACK_MESSAGE, summary="fallback")
        return {"response": FALLBACK_MESSAGE}

    # Build Prompt (Only reaches here if relevant)
    prompt = build_prompt(message, contexts, history)

    # Generate Answer
    raw_response = generate_response(prompt)

    answer, summary = parse_response(raw_response)

    append_message(phone, "assistant", answer, summary)

    return {
        "response": answer
    }