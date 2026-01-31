from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from src.schemas.prediction import PredictionInput

router = APIRouter()

# Load the trained model and scalers
model = load_model('../../model/lstm_v1.keras') # caminho relativo ao arquivo predict.py
scaler = joblib.load('../../model/scaler_lstm_v1.pkl') # caminho relativo ao arquivo predict.py

@router.post("/predict")
def predict_stock_price(input: PredictionInput):
    try:
        if len(input.data) != 60:
            raise HTTPException(status_code=400, detail="Input data must contain exactly 60 historical price values.")

        data = np.array(input.data).reshape(-1, 1)
        
        data_scaled = scaler.transform(data)
        data_scaled = data_scaled.reshape(1, 60, 1)
        
        prediction_scaled = model.predict(data_scaled)
        
        prediction = scaler.inverse_transform(prediction_scaled)
        
        return {"predicted_price": float(prediction[0][0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
