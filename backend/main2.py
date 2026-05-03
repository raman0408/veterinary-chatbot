from backend.services.memory import load_history, append_message
from backend.routes.chat import chat

phone = "9999999999"

print("Chatbot ready. Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    response = chat({
        "phone": phone,
        "message": message
    })

    print("\nBot:", response["response"], "\n")