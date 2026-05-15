from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import summary

app = FastAPI(
    title="FinTrack API",
    description="API de métricas financeiras do fintrack-pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # origem do Str
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)

app.include_router(summary.router)

@app.get("/")
def root():
    return {"message": "FinTrack API rodando!"}