from backend.graph.states import ChatState
from backend.services.rag import retrieve_with_scores
from backend.services.rewrite import rewrite_query_llm

def rewrite(state: ChatState):
    message = state["message"]
    history = state["history"]

    rewritten_query = rewrite_query_llm(message, history)

    contexts, scores = retrieve_with_scores(rewritten_query)
    best_hq = min(scores) if scores else float("inf")

    print(f"[GRAPH DEBUG] rewrite -> rewritten_query: {rewritten_query}")
    print(f"[GRAPH DEBUG] rewrite -> best_hq: {best_hq}")
    print(f"[GRAPH DEBUG] rewrite -> contexts: {contexts}")

    return {
        "rewritten_query": rewritten_query,
        "contexts": contexts,
        "best_hq": best_hq
    }