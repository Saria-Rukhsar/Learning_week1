import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="mock-key"
)

# Cost config (Rates per 1 Million tokens in USD)
INPUT_RATE_PER_1M = 0.15   # $0.15 per 1 Million input tokens
OUTPUT_RATE_PER_1M = 0.60  # $0.60 per 1 Million output tokens

def estimate_tokens(text: str) -> int:
    """Ek simple aur reliable tareeqa tokens estimate karne ka (1 token ~= 4 chars)"""
    if not text:
        return 0
    return max(1, round(len(text) / 4))

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Tokens ko dollars mein convert karne ka formula"""
    input_cost = (input_tokens / 1_000_000) * INPUT_RATE_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_RATE_PER_1M
    return input_cost + output_cost

async def ask_ai_with_tracking(prompt):
    print(f"Prompt: '{prompt}'")
    
    # 1. Input tokens count karein
    input_tokens = estimate_tokens(prompt)
    print(f"-> Input Tokens (Estimated): {input_tokens}")
    
    stream = await client.chat.completions.create(
        model="local-llama",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    print("\nAI Response: ", end="", flush=True)
    
    full_response = ""
    
    # 2. Response stream karte waqt har chunk ko jama (concatenate) karte jayein
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content  # Response ko jod rahe hain
                
    print("\n" + "-"*40)
    
    # 3. Output tokens count karein jo humne stream se jama kiye
    output_tokens = estimate_tokens(full_response)
    
    # 4. Total cost calculate karein
    total_cost_usd = calculate_cost(input_tokens, output_tokens)
    # PKR mein convert karne ke liye (Farz karein $1 = 278 PKR)
    total_cost_pkr = total_cost_usd * 278 
    
    # 5. Report print karein
    print("📊 COST & TOKEN REPORT:")
    print(f"   - Input Tokens:  {input_tokens}")
    print(f"   - Output Tokens: {output_tokens} (AI Generated)")
    print(f"   - Total Tokens:  {input_tokens + output_tokens}")
    print(f"   - Estimated Cost: ${total_cost_usd:.6f} USD (~ {total_cost_pkr:.4f} PKR)")
    print("-"*40 + "\n")

async def main():
    print("--- Starting Task 3: Token & Cost Tracking ---")
    await ask_ai_with_tracking("Python programming kya hai? Aik line mein batao.")

if __name__ == "__main__":
    asyncio.run(main())