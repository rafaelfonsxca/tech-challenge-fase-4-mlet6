from fastapi import FastAPI
from src.api import auth


app = FastAPI(
    title="Título API",
    description="API descrição aqui.",
    version="1.0.0"
)

app.include_router(
    auth.router, 
    prefix="/api/v1",
    tags=["Auth"])