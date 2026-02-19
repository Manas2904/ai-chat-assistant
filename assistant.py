from ollama import chat
from long_term_memory import LongTermMemory

# initialize long-term memory
ltm = LongTermMemory()

# short-term memory (conversation buffer)
conversation = [
    {"role": "system", "content": "You are a helpful AI assistant with memory."}
]

print("AI Assistant started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # retrieve relevant long-term memories
    memories = ltm.search(user_input)

    memory_context = ""
    if memories:
        memory_context = "Relevant past information:\n" + "\n".join(memories)

    # build final prompt
    conversation.append({"role": "user", "content": user_input})

    final_messages = conversation.copy()

    if memory_context:
        final_messages.insert(
            1,
            {"role": "system", "content": memory_context}
        )

    response = chat(
        model="llama3",
        messages=final_messages
    )

    reply = response["message"]["content"]
    print("AI:", reply)

    conversation.append({"role": "assistant", "content": reply})

    # store important info in long-term memory (simple rule)
    if len(user_input.split()) > 4:
        ltm.add(user_input)
