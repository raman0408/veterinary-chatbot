from backend.graph.states import ChatState

def detect_smalltalk(state: ChatState):
    msg = state["message"].lower().strip()

    smalltalk_patterns = {
        "hi", "hello", "hey", "thanks",
        "thank you", "bye"
    }
    is_smalltalk = msg in smalltalk_patterns

    return {
        "is_smalltalk": is_smalltalk
    }