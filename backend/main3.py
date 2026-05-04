from backend.graph.builder import build_graph
from backend.services.memory import load_history

graph = build_graph()

phone = "8888888888"
history = load_history(phone)

result = graph.invoke({
    "phone": phone,
    "message": "what is mastitis",
    "history": history
})

print(result["response"])