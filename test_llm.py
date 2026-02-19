from ollama import chat

response = chat(
    model="llama3",
    messages=[
        {"role": "user", "content": "Explain LLMs in simple terms"}
    ]
)

print(response["message"]["content"])
