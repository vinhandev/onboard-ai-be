import os
import asyncio
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

# Load .env when present
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    # In development, it's common to run without env set; we still let the server start but any call to OpenAI will return 500.
    pass
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')
origins = [o.strip() for o in ALLOWED_ORIGINS.split(',') if o.strip()]
app = FastAPI(title='FastAPI OpenAI Proxy')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)



class ChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 500

class ChatResponse(BaseModel):
    reply: str

OPENAI_CHAT_URL = 'https://aiportalapi.stu-platform.live/jpe/v1/chat/completions'

@app.get('/health')
async def health():
    return { 'status': 'ok' }

@app.post('/api/chat', response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Receive a prompt from the frontend, call OpenAI, and return the assistant reply.

    This endpoint is deliberately simple for demonstration. In production you should:
    - Add authentication (so anyone can't call your proxy)
    - Implement rate-limiting
    - Validate/clean prompts if necessary
    - Consider streaming responses for large outputs
    """
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail='OpenAI API key not configured on the server')

    model = req.model or 'gpt-4o-mini'  # default - change to the model you prefer

    payload = {
        'model': model,
        'messages': [
            { 'role': 'system', 'content': 'You are a helpful assistant.' },
            { 'role': 'user', 'content': req.prompt }
        ],
        'max_tokens': req.max_tokens,
        'temperature': 0.7
    }

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(OPENAI_CHAT_URL, json=payload, headers=headers)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f'Error calling OpenAI: {exc}')

    if r.status_code >= 400:
        # Forward a helpful error to the frontend (avoid leaking internal secrets)
        try:
            body = r.json()
        except Exception:
            body = { 'error': r.text }
        raise HTTPException(status_code=502, detail={ 'openai_status': r.status_code, 'openai_response': body })

    data = r.json()

    # Extract assistant content robustly
    try:
        choices = data.get('choices') or []
        if not choices:
            raise ValueError('No choices returned from OpenAI')
        first = choices[0]
        message = first.get('message') or {}
        content = message.get('content')
        if content is None:
            # Some models return text directly in a "text" field for legacy endpoints
            content = first.get('text') or ''
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Could not parse OpenAI response: {e}')

    return { 'reply': content }

# Optional: run with `python fastapi_openai_proxy.py` for quick dev testing
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('fastapi_openai_proxy:app', host='0.0.0.0', port=8000, reload=True)


