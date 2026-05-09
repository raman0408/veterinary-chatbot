from backend.graph.states import ChatState

def smalltalk_response(state: ChatState):
    msg = state["message"].lower().strip()

    if msg in {"hi", "hello", "hey"}:
        response = "Hello! How can I help you with dairy cattle care today?"
    elif msg in {"thanks", "thank you"}:
        response = "You're welcome! Let me know if you need help with dairy cattle health or management."

    elif msg in {"bye", "goodbye"}:
        response = "Goodbye! Take care of your cattle"
    else:
        response = "Hello!"
    
    return {
        "response": response,
        "summary": "smalltalk"
    }