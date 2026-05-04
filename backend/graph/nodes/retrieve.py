from backend.services.rag import retrieve_with_scores
from backend.graph.states import ChatState

def retrieve_raw(state: ChatState):
    message = state["message"]

    contexts, scores = retrieve_with_scores(message)
    best_q = min(scores) if scores else float("inf")

    print(f"[GRAPH DEBUG] retrieve_raw -> best_q: {best_q}")
    print(f"[GRAPH DEBUG] contexts: {contexts}")

    return {
        "contexts": contexts,
        "best_q": best_q
    }