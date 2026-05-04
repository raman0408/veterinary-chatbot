from backend.graph.states import ChatState
THRESHOLD = 1.0

def route_after_raw(state: ChatState):
    best_q = state["best_q"]
    is_vague = state["is_vague"]

    print(f"[GRAPH DEBUG] route_after_raw -> best_q: {best_q}, is_vague: {is_vague}")

    if best_q < THRESHOLD:
        print("[GRAPH DEBUG] -> route: generate")
        return "generate"
    elif is_vague:
        print("[GRAPH DEBUG] -> route: rewrite")
        return "rewrite"
    else:
        print("[GRAPH DEBUG] -> route: fallback")
        return "fallback"

REL_IMPROVEMENT_THRESHOLD = 0.3

def route_after_rewrite(state: ChatState):
    best_q = state["best_q"]
    best_hq = state["best_hq"]

    print(f"[GRAPH DEBUG] route_after_rewrite -> best_q: {best_q}, best_hq: {best_hq}")

    if best_q != 0:
        improvement_ratio = (best_q - best_hq)/best_q
    else:
        improvement_ratio = 0
    print(f"[GRAPH DEBUG] improvement_ratio: {improvement_ratio}")

    if best_hq < THRESHOLD and improvement_ratio > REL_IMPROVEMENT_THRESHOLD:
        print("[GRAPH DEBUG] -> route: generate")
        return "generate"
    else:
        print("[GRAPH DEBUG] -> route: fallback")
        return "fallback"
