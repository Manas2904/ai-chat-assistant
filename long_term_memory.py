import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer

class LongTermMemory:
    def __init__(self, path="memory_store"):
        self.path = path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384

        if not os.path.exists(path):
            os.makedirs(path)

        self.index_file = os.path.join(path, "index.faiss")
        self.data_file = os.path.join(path, "data.pkl")

        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.data_file, "rb") as f:
                self.data = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.data = []

    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(embedding)
        self.data.append(text)
        self._save()

    def search(self, query, k=3):
        embedding = self.model.encode([query])
        distances, indices = self.index.search(embedding, k)
        return [self.data[i] for i in indices[0] if i < len(self.data)]

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.data_file, "wb") as f:
            pickle.dump(self.data, f)
