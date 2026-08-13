from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import uvicorn

app = FastAPI()

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    stream: bool = False

async def fake_stream_generator(prompt):
    words = f"Hello! This is a live streamed response from your local server. You asked about: {prompt}".split()
    for word in words:
        # Bilkul OpenAI standard stream format
        chunk = {
            "choices": [
                {
                    "delta": {
                        "content": word + " "  # Har word ke baad space
                    }
                }
            ]
        }
        # SSE (Server-Sent Events) format mein yield karna zaroori hai
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.3)  # 0.3 seconds ka delay taaki typewriter effect dikhe
    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    return StreamingResponse(fake_stream_generator(request.messages[-1]["content"]), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)