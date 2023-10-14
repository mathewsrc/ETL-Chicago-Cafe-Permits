from transformers import pipeline
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()

class Body(BaseModel):
    text:str
    
summarizer = pipeline(
                    "summarization",
                    model="t5-small",
                    tokenizer="t5-small",
                    truncation=True,
                    framework="tf")

sentiment = pipeline(
                        "sentiment-analysis",
                        model="gpt2",
                        tokenizer="gpt2",
                        truncation=True,
                        framework="tf")
    
@app.get('/')
def root():
    return HTMLResponse("<h1>Hugging Face NLP</h1>")

    
@app.post('/summarize')
def summarize(body: Body):
    results = summarizer(body.text)
    return results
        
@app.post('/sentiment')
def sentiment_analysis(body: Body):
    return sentiment(body.text)
