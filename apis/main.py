from fastapi import FastAPI, HTTPException
from models.response_models import ChatResponse
from models.request_models import ChatRequest
from app.agent import ask_agent

app = FastAPI(title="SupportPilot AI")

@app.post("/chat",response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """
    Receives a customer message, routes it through the AI agent
    (RAG / Tools / Human Handoff), and returns the response.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    result = ask_agent(payload.message)
    return ChatResponse(response=result["response"],handoff=result["handoff"])


@app.get("/")
async def root():
    return  {"message":"SupportPilot AI is running. Go to /docs to try it."}