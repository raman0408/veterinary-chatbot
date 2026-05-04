from backend.graph.states import ChatState

def is_vague_query(message: str):
    message = message.lower().strip()

    vague_patterns = [
        "explain", "repeat", "again", "that", "there", "here",
        "it", "this", "more", "details", "understand", "else"
    ]
    short = len(message.split()) <= 2
    contains_vague = any(p in message for p in vague_patterns)

    return short or contains_vague

def detect_vague(state: ChatState):
    message = state["message"]

    vague = is_vague_query(message)

    print(f"[GRAPH DEBUG] detect_vague -> {vague}")

    return {
        "is_vague": vague
    }