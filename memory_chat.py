from ollama import chat

conversation = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    conversation.append({"role": "user", "content": user_input})

    response = chat(
        model="llama3",
        messages=conversation
    )

    reply = response["message"]["content"]
    print("AI:", reply)

    conversation.append({"role": "assistant", "content": reply})
