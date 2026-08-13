from google import genai

class QAEngine:
    def __init__(self, client: genai.Client):
        self.client = client
        self.memory = []

    def generate_answer(self, query: str, context_chunks: list[str]) -> str:
        """Relevant context aur user query ko strict system prompt ke sath LLM ko bhejta hai."""
        context_text = "\n\n---\n\n".join(context_chunks)
        system_instruction = (
            "You are a strict document QA assistant. Answer the user's question using ONLY "
            "the provided Context. If the answer cannot be found in the Context, respond with: "
            "'I cannot answer this question based on the provided document.' "
            "Do NOT use any outside general knowledge."
        )
        prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
        messages = [
            {"role": "user", "parts": [{"text": system_instruction}]}
        ] + self.memory[-6:]
        # Current prompt add karna
        messages.append({"role": "user", "parts": [{"text": prompt}]})
        # 5. Gemini API Call
        response = self.client.models.generate_content(
            model="gemini-3.6-flash", contents=messages
        )
        answer = response.text
        # 6. Memory Update (Agli conversation turn ke liye user aur bot ki baat save karna)
        self.memory.append({"role": "user", "parts": [{"text": query}]})
        self.memory.append({"role": "model", "parts": [{"text": answer}]})
        return answer