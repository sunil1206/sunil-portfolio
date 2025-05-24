import os
import re
import string
import pickle

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# -------------------------------
# 1. Init FastAPI
# -------------------------------
app = FastAPI(title="Spam Detection API")

# -------------------------------
# 2. Load Model & Tokenizer
# -------------------------------
MODEL_PATH = os.path.join('model', 'light-gru_spam_model.h5')
TOKENIZER_PATH = os.path.join('model', 'tokenizer.pkl')

try:
    model = load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)
    load_error = None
except Exception as e:
    model = None
    tokenizer = None
    load_error = str(e)

# -------------------------------
# 3. Spam Keyword Set & Cleaner
# -------------------------------
spam_keywords = {
    'win', 'free', 'prize', 'urgent', 'winner', 'cash', 'claim', 'offer',
    'limited', 'credit', 'congratulations', 'click', 'now', 'money',
    'bonus', 'buy', 'purchase', 'subscribe', 'reward', 'instant', 'discount',
    'deal', 'selected', 'cheap', 'exclusive', 'guaranteed', 'risk-free',
    'act now', 'call now', 'buy now', 'apply now', 'click here', 'order now',
    'urgent response', 'limited time', 'easy money', 'no cost', 'trial',
    'gift card', 'get paid', 'winner selected', 'double your', 'act fast',
    'lowest price', 'pre-approved', 'miracle', 'this won’t last', 'earn money',
    'insurance', 'work from home', 'investment', 'earn extra', 'no obligation',
    'luxury', 'pills', 'lottery', 'viagra', 'lose weight', 'weight loss',
    'income', 'fast cash', '100% free', 'free access', 'exclusive deal',
    'clearance', 'satisfaction guaranteed', 'extra income', 'no fees'
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'@\w+|\#', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    return re.sub(r'\s+', ' ', text).strip()


# -------------------------------
# 4. Prediction Function
# -------------------------------
def predict_spam_message(text: str):
    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    pad = pad_sequences(seq, maxlen=100, padding='post')
    prob = float(model.predict(pad, verbose=0)[0][0])
    label = "Spam" if prob > 0.5 else "Not Spam"
    confidence = round(prob * 100, 2) if label == "Spam" else round((1 - prob) * 100, 2)
    matched = [w for w in cleaned.split() if w in spam_keywords]
    return label, confidence, matched


# -------------------------------
# 5. Pydantic Schema
# -------------------------------
class SpamRequest(BaseModel):
    message: str


class SpamResponse(BaseModel):
    prediction: str
    confidence: float
    matched_keywords: list


# -------------------------------
# 6. Prediction Endpoint
# -------------------------------
@app.post("/spam", response_model=SpamResponse)
def predict(request: SpamRequest):
    if load_error:
        raise HTTPException(status_code=500, detail=f"Model loading error: {load_error}")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    try:
        label, confidence, matched = predict_spam_message(request.message)
        return SpamResponse(prediction=label, confidence=confidence, matched_keywords=matched)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
