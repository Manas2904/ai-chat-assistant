import streamlit as st
from ollama import chat
from long_term_memory import LongTermMemory

st.set_page_config(page_title="AI Assistant with Memory", layout="centered")

st.title("🧠 AI Assistant with Long-Term Memory")

# Initialize memories once
if "ltm" not in st.session_state:
    st.session_state.ltm = LongTermMemory()

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are a helpful AI assistant with memory."}
    ]

user_input = st.text_input("Ask something")

if st.button("Send") and user_input:
    # Retrieve long-term memory
    memories = st.session_state.ltm.search(user_input)
    memory_context = ""
    if memories:
        memory_context = "Relevant past information:\n" + "\n".join(memories)

    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    final_messages = st.session_state.conversation.copy()
    if memory_context:
        final_messages.insert(1, {"role": "system", "content": memory_context})

    response = chat(model="llama3", messages=final_messages)
    reply = response["message"]["content"]

    st.session_state.conversation.append(
        {"role": "assistant", "content": reply}
    )

    # Save meaningful inputs
    if len(user_input.split()) > 4:
        st.session_state.ltm.add(user_input)

# Display chat
for msg in st.session_state.conversation[1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")
