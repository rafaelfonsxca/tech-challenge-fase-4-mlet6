from fastapi import APIRouter, HTTPException, Depends
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from src.schemas.prediction import PredictionInput
from src.schemas.user import UserResponse
from src.core.security import get_current_user
from src.core.monitoring import track_model_performance

router = APIRouter()

# Load the trained model and scalers
model = load_model('../model/models/lstm_v1.keras')
scaler_features = joblib.load('../model/models/scaler_features_lstm_v1.pkl')
scaler = joblib.load('../model/models/scaler_lstm_v1.pkl')

@router.post("/predict")
@track_model_performance
def predict_stock_price(
    input: PredictionInput,
    current_user: UserResponse = Depends(get_current_user)):
    """
    Predict the stock price using the trained LSTM model.

    This endpoint takes 30 days of stock data (Open, High, Low, Close, Volume)
    and predicts the next day's closing price.

    Args:
        input (PredictionInput): Input data containing a list of 30 days,
                                 each with 5 features.

    Returns:
        dict: Dictionary containing the predicted price under 'predicted_price'.

    Raises:
        HTTPException: 400 if input data is invalid, 500 if prediction fails,
                       or 401 if authentication fails.
    """
    try:
        if len(input.data) != 30 or any(len(day) != 5 for day in input.data):
            raise HTTPException(status_code=400, detail="Input data must contain exactly 30 days of 5 features each (Open, High, Low, Close, Volume).")

        data = np.array(input.data)
        
        data_scaled = scaler_features.transform(data)
        data_scaled = data_scaled.reshape(1, 30, 5)
        
        prediction_scaled = model.predict(data_scaled)
        
        prediction = scaler.inverse_transform(prediction_scaled.reshape(-1, 1))
        
        return {"predicted_price": float(prediction[0][0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
