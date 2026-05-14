from fastapi import FastAPI
from api.routers import summary

app = FastAPI(
    title="FinTrack API",
    description="API de métricas financeiras do fintrack-pipeline",
    version="1.0.0"
)

app.include_router(summary.router)

@app.get("/")
def root():
    return {"message": "FinTrack API rodando!"}