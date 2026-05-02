from backend.services.memory import load_history, append_message
from backend.services.rag import retrieve_with_scores, is_relevant
from backend.services.llm import generate_response, build_prompt, parse_response

phone = "9999999999"

print("Chatbot ready. Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    # Load history
    history = load_history(phone)

    # Save user message
    append_message(phone, "user", message)

    # 🔷 Build retrieval query (summary-based)
    recent = history[-3:]
    history_text = " ".join(
        [msg.get("summary", "") for msg in recent if msg["role"] == "assistant"]
    )

    retrieval_query = f"{history_text} {message}"

    print(f"\n[DEBUG] Retrieval Query: {retrieval_query}")

    # 🔷 Retrieve
    contexts, scores = retrieve_with_scores(retrieval_query)

    print(f"[DEBUG] Scores: {scores}")

    if not is_relevant(scores):
        print("\nBot: FALLBACK\n")
        append_message(phone, "assistant", "fallback")
        continue

    # 🔷 Build prompt
    prompt = build_prompt(message, contexts, history)

    print(f"[DEBUG] Prompt length: {len(prompt)}")

    # 🔷 Generate response
    raw_response = generate_response(prompt)

    answer, summary = parse_response(raw_response)

    print("\nBot:", answer)
    print("[DEBUG] Summary:", summary, "\n")

    append_message(phone, "assistant", answer, summary)