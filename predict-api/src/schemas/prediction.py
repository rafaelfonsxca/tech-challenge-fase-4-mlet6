from pydantic import BaseModel

class PredictRequest(BaseModel):
    symbol: str