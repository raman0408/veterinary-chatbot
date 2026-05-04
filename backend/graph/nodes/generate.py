from backend.graph.states import ChatState
from backend.services.llm import generate_response, build_prompt, parse_response

def generate(state: ChatState):
    message = state["message"]
    history = state["history"]
    contexts = state["contexts"]

    prompt = build_prompt(message, contexts, history)

    print(f"[GRAPH DEBUG] generate -> prompt length: {len(prompt)}")

    raw = generate_response(prompt)

    answer, summary = parse_response(raw)

    print(f"[GRAPH DEBUG] generate → answer: {answer}")
    print(f"[GRAPH DEBUG] generate → summary: {summary}")

    return {
        "response": answer,
        "summary": summary
    }