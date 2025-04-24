from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI()

# Model và tokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)

sentiment_map = {
    0: "Very Negative",
    1: "Negative",
    2: "Neutral",
    3: "Positive",
    4: "Very Positive"
}

# Schema input
class TextRequest(BaseModel):
    text: str

class BatchRequest(BaseModel):
    texts: List[str]

# Dự đoán 1 câu
@app.post("/predict")
def predict_sentiment(request: TextRequest):
    inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=-1).item()
    return {"label": sentiment_map[pred]}

# Dự đoán batch
@app.post("/predict_batch")
def predict_batch(request: BatchRequest):
    texts = request.texts
    if not texts:
        print("[⚠️] Empty request received.")
        return {"labels": []}
    
    print(f"[📦] Received {len(texts)} texts for prediction.")
    all_preds = []
    batch_size = 16

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"[🔄] Processing batch {i // batch_size + 1} with {len(batch)} texts...")
        
        inputs = tokenizer(batch, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            preds = torch.argmax(probs, dim=-1).tolist()

        labels = [sentiment_map[p] for p in preds]
        for text, label in zip(batch, labels):
            print(f"[✅] Text: \"{text}\" → Sentiment: {label}")
        
        all_preds.extend(labels)
    
    print(f"[🎯] Finished predicting {len(all_preds)} texts.\n")
    return {"labels": all_preds}
