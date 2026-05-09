from backend.graph.builder import build_graph
from backend.services.memory import load_history, append_message

graph = build_graph()

phone = "9999999990"

print("Veterinary Chatbot (LangGraph Version)")
print("Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    # --- Load history ---
    history = load_history(phone)

    # --- Invoke graph ---
    result = graph.invoke({
        "phone": phone,
        "message": message,
        "history": history
    })

    response = result["response"]
    summary = result["summary"]

    # --- Print response ---
    print(f"\nBot: {response}\n")

    # --- Save memory ---
    append_message(phone, "user", message)
    append_message(phone, "assistant", response, summary)