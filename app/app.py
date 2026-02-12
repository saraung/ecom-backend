from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return "Welcome to footyconnects"

@app.get("/health")
def health():
    return {"status":"ok"}