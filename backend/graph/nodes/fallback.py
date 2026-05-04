from backend.graph.states import ChatState

FALLBACK_MESSAGE = "We will connect you to our veterinary expert. Please contact the doctor at +91 9999999999."


def fallback(state: ChatState):
    print("[GRAPH DEBUG] fallback -> triggered")

    return {
        "response": FALLBACK_MESSAGE,
        "summary": "fallback"
    }