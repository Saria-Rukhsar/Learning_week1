from google import genai
import numpy as np

class SimpleVectorStore:
    def __init__(self, client: genai.Client):
        self.client = client
        self.chunks = []
        self.embeddings = []

    def _get_embedding(self, text: str) -> np.ndarray:
        """Text ko vector embedding mein convert karta hai."""
        response = self.client.models.embed_content(
            model="gemini-embedding-001", contents=text
        )

        if hasattr(response, "embedding"):
            return np.array(response.embedding.values)
        elif hasattr(response, "embeddings"):
            return np.array(response.embeddings[0].values)
        else:
            raise ValueError("Embedding values not found in response")

    def add_chunks(self, chunks: list[str]):
        self.chunks = chunks
        self.embeddings = []
        print("Creating vectors of document chunks...")
        for chunk in chunks:
            emb = self._get_embedding(chunk)
            self.embeddings.append(emb)
        print("Indexing completed!")

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """Cosine similarity search."""
        if not self.embeddings:
            return []
        query_emb = self._get_embedding(query)
        similarities = []
        for emb in self.embeddings:
            sim = np.dot(query_emb, emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(emb)
            )
            similarities.append(sim)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]