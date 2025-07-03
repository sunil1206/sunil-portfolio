# ml_chatbot_fastapi/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from chatbot_model import load_model, predict_intent
from db_cache import load_intent_cache
from grammar import grammar_correct

app = FastAPI()

# Load ML model and response cache ONCE at startup
vectorizer, classifier = load_model()
intent_cache = load_intent_cache()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatInput):
    corrected_text = grammar_correct(data.message)
    intent = predict_intent(corrected_text, vectorizer, classifier)
    response = intent_cache.get(intent, "Sorry, I didn't understand.")
    return {"response": response}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running."}