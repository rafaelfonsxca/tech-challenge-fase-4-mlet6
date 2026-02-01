from pydantic import BaseModel

class PredictionInput(BaseModel):
    # Add ticker symbol
    data: list[list[float]]