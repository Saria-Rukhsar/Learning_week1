import asyncio
import json
from openai import AsyncOpenAI
# Tenacity se retry handlers import karein
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Wrapper Class
class AsaanAIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/v1", model="local-llama"):
        print("Initializing AsaanAIClient wrapper...")
        # 1. Internal state setup (Sari configuration ek hi jagah)
        self.client = AsyncOpenAI(base_url=base_url, api_key="mock-key")
        self.model = model

        # Cost config
        self.INPUT_RATE = 0.15
        self.OUTPUT_RATE = 0.60

    def _estimate_tokens(self, text: str) -> int:
        """Aapka bataya hua custom estimation function (1 token ~= 4 chars)"""
        if not text:
            return 0
        return max(1, round(len(text) / 4))

    def _calculate_cost(self, in_tokens: int, out_tokens: int) -> float:
        return ((in_tokens / 1_000_000) * self.INPUT_RATE) + ((out_tokens / 1_000_000) * self.OUTPUT_RATE)

    # 2. TASK 4: Retry Mechanism 
    # Agar network error aaye, toh exponential gap ke sath maximum 3 dafa retry karo
    @retry(
        stop=stop_after_attempt(3), # Max 3 koshishein
        wait=wait_exponential(multiplier=1, min=2, max=10), # Pehla wait 2s, phir 4s, phir 8s
        reraise=True # Agar 3 dafa bhi na ho toh error throw karo
    )
    async def _safe_api_call(self, prompt: str):
        """Yeh internal helper function safety ke sath API call karta hai"""
        return await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

    # 3. Main wrapper function jo doosre log use karenge
    async def ask_ai_streaming(self, prompt: str):
        in_tokens = self._estimate_tokens(prompt)
        print(f"\n[AI Client] Prompt Tokens: {in_tokens}")
        try:
            # Safe call with auto-retries
            stream = await self._safe_api_call(prompt)
            
            print("[AI Client] Response: ", end="", flush=True)
            full_response = ""
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
                        full_response += content
            
            out_tokens = self._estimate_tokens(full_response)
            cost = self._calculate_cost(in_tokens, out_tokens)
            
            print("\n" + "="*40)
            print(f"📊 REPORT: In: {in_tokens} | Out: {out_tokens} | Cost: ${cost:.6f}")
            print("="*40 + "\n")
            return full_response

        except Exception as e:
            # Agar sab retries fail ho jayein toh gracefully handle karein
            print(f"\n❌ [AI Client Error]: API completely failed or network down. Details: {e}")
            return None

# --- Wrapper Class Ko Test Karne Ka Code ---
async def main():
    print("--- Testing Our AI Client Wrapper Class ---")
    
    # Simple initialization (No complex setups required anymore!)
    ai = AsaanAIClient()
    
    # Clean, direct call!
    await ai.ask_ai_streaming("Python kya hai? Ek line mein batao.")

if __name__ == "__main__":
    asyncio.run(main())