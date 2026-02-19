from long_term_memory import LongTermMemory

memory = LongTermMemory()

memory.add("Manas is a final year AIML student.")
memory.add("Manas likes building AI systems.")
memory.add("Manas prefers local LLMs for learning.")

results = memory.search("What does Manas like?")
print(results)
