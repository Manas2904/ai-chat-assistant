# 🧠 AI Assistant with Long-Term Memory (Local LLM)

A ChatGPT-like AI assistant built using a local LLaMA-3 model with short-term conversational memory and long-term semantic memory.

## 🚀 Features
- Local LLM inference using Ollama (LLaMA-3)
- Short-term conversational memory
- Long-term semantic memory using FAISS
- Memory-augmented prompt construction
- Streamlit web interface
- Modular, extensible architecture

## 🛠 Tech Stack
- Python 3.11
- Ollama (LLaMA-3)
- FAISS
- Sentence Transformers
- Streamlit

## ⚙️ Setup
```bash
git clone <repo-url>
cd ai-chat-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama run llama3
streamlit run app.py
