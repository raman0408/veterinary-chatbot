from fastapi import APIRouter
from backend.services.memory import load_history, append_message
from backend.services.rag import retrieve_with_scores, is_relevant
from backend.services.llm import generate_response, build_prompt, rewrite_query, needs_rewrite

FALLBACK_MESSAGE = "We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."
router = APIRouter()

@router.post("/chat")
def chat(data: dict):
    phone = data.get("phone")
    message = data.get("message")

    # Load History
    history = load_history(phone)
    has_history = len(history) > 0

    # Save User Message
    append_message(phone, "user", message)

    # Retrieve Context
    contexts, scores = retrieve_with_scores(message)
    
    if not is_relevant(scores):
        if needs_rewrite(message):
            rewritten_query = rewrite_query(message, history)

            contexts, scores = retrieve_with_scores(rewritten_query)

            if not is_relevant(scores):
                append_message(phone, "assistant", FALLBACK_MESSAGE)
                return {"response": FALLBACK_MESSAGE}
        else:
            append_message(phone, "assistant", FALLBACK_MESSAGE)
            return {"response": FALLBACK_MESSAGE}

    

    # Build Prompt (Only reaches here if relevant)
    prompt = build_prompt(message, contexts, history)

    # Generate Answer
    response = generate_response(prompt)

    # Save Bot Response
    append_message(phone, "assistant", response)

    return {
        "response": response
    }