from langgraph.graph import StateGraph, END

from backend.graph.states import ChatState

from backend.graph.nodes.retrieve import retrieve_raw
from backend.graph.nodes.detect_vague import detect_vague
from backend.graph.nodes.rewrite import rewrite
from backend.graph.nodes.generate import generate
from backend.graph.nodes.fallback import fallback
from backend.graph.nodes.detect_smalltalk import detect_smalltalk
from backend.graph.nodes.smalltalk_response import smalltalk_response


from backend.graph.routes.routing import route_after_raw, route_after_rewrite, route_initial

def build_graph():
    builder = StateGraph(ChatState)

    # --- Register nodes ---
    builder.add_node("detect_smalltalk", detect_smalltalk)
    builder.add_node("smalltalk_response", smalltalk_response)
    builder.add_node("retrieve_raw", retrieve_raw)
    builder.add_node("detect_vague", detect_vague)
    builder.add_node("rewrite", rewrite)
    builder.add_node("generate", generate)
    builder.add_node("fallback", fallback)

    # --- Entry Point ---
    builder.set_entry_point("detect_smalltalk")

    # --- First decision ---
    builder.add_conditional_edges(
        "detect_smalltalk",
        route_initial,
        {
            "smalltalk_response": "smalltalk_response",
            "retrieve_raw": "retrieve_raw"
        }
    )
    # --- Linear edges ---
    builder.add_edge("retrieve_raw", "detect_vague")

    # --- Second decision ---
    builder.add_conditional_edges(
        "detect_vague",
        route_after_raw,
        {
            "generate": "generate",
            "rewrite": "rewrite",
            "fallback": "fallback"
        }
    )

    # --- Third decision ---
    builder.add_conditional_edges(
        "rewrite",
        route_after_rewrite,
        {
            "generate": "generate",
            "fallback": "fallback"
        }
    )

    # --- Terminal edges ---
    builder.add_edge("generate", END)
    builder.add_edge("fallback", END)
    builder.add_edge("smalltalk_response", END)
    # --- Compile graph ---
    graph = builder.compile()

    return graph
