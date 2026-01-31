from pydantic import BaseModel

class PredictionInput(BaseModel):
    data: list[float]