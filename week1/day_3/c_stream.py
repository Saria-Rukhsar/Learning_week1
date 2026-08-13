import asyncio
from openai import AsyncOpenAI

# 1. Local Mock Server ka address
client = AsyncOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="mock-key"
)

async def ask_ai_streaming(prompt):
    print("Sending request for streaming...")
    
    stream = await client.chat.completions.create(
        model="local-llama",
        messages=[{"role": "user", "content": prompt}],
        stream=True  # <--- Yeh line streaming activate karti hai
    )
    
    print("AI Response: ", end="", flush=True)
    
    # 3. 'async for' loop ke zariye har ek chunk ko live received aur print karenge
    async for chunk in stream:
        # Har chunk ke andar se naya word nikalte hain
        content = chunk.choices[0].delta.content
        if content:
            # end="" se line change nahi hoti, aur flush=True se terminal foran print karta hai
            print(content, end="", flush=True)
            
    print("\n\n--- Streaming Finished! ---")

async def main():
    print("--- Starting Task 2: Streaming Handler ---")
    await ask_ai_streaming("Python programming kya hai?")

if __name__ == "__main__":
    asyncio.run(main())