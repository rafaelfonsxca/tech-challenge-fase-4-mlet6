from fastapi import FastAPI
from src.api import auth, predict, user


app = FastAPI(
    title="Stock Price Prediction API",
    description="API for predicting stock prices using LSTM model.",
    version="1.0.0"
)

app.include_router(
    auth.router, 
    prefix="/api/v1",
    tags=["Auth"])

app.include_router(
    user.router, 
    prefix="/api/v1",
    tags=["Users"])

app.include_router(
    predict.router,
    prefix="/api/v1",
    tags=["Prediction"])