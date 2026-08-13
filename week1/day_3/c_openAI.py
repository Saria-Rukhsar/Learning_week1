import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="mock-key-not-needed"
)

async def ask_ai(prompt):
    response = await client.chat.completions.create(
        model="local-llama",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def main():
    print("Calling Local Mock Server asynchronously...")
    reply = await ask_ai("Python programming kia hai? Aik line mein batao.")
    print("\n--- Response ---")
    print(reply)

if __name__ == "__main__":
    asyncio.run(main())