from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.predict import router as predict_router


app = FastAPI(
    title="Ionic SL API",
    version="0.1.0",
    description="Dual-phase ionic conductivity prediction service for solid and liquid lithium battery electrolytes.",
)
@app.get("/")
def root():
    return {"status": "Ionic SL API is running", "docs": "/docs"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(predict_router)
