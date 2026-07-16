from fastapi import FastAPI
from pydantic import BaseModel
from agent.loop import chat, conversation_history
from memory.long_term import init_db, load_history, clear_history

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
def startup():
    init_db()
    past_history = load_history(limit=10)
    if past_history:
        conversation_history.extend(past_history)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = chat(request.message)
    return {"response": response}

@app.get("/history")
def history_endpoint():
    return {"history": load_history()}

@app.delete("/memory")
def clear_memory_endpoint():
    conversation_history.clear()
    return {"message": clear_history()}

@app.get("/health")
def health():
    return {"status": "ok"}