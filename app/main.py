from fastapi import FastAPI
from core.pipeline import Pipeline

app = FastAPI()
pipeline = Pipeline()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predict")
def predict(home: str, away: str):
    return pipeline.predict(home, away)
