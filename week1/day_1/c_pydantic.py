from pydantic import BaseModel, ValidationError, Field
from typing import Literal

# 1. REQUEST MODEL
class HousePredictionRequest(BaseModel):
    square_feet: float = Field(..., gt=100, description="Ghar ka size square feet mein")
    bedrooms: int = Field(..., ge=1, le=10, description="Bedrooms ki tadad")
    location: Literal["Urban", "Suburban", "Rural"] = Field(..., description="Ghar ka ilaka")

# 2. RESPONSE MODEL
class HousePredictionResponse(BaseModel):
    predicted_price: float = Field(..., description="AI model ki taraf se predicted price")
    model_version: str = Field("v1.0.0", description="AI model ka version")
    status: str = "Success"

# AI Prediction
def fake_ai_predict(data: HousePredictionRequest):
    base_price = data.square_feet * 50 + (data.bedrooms * 10000)
    if data.location == "Urban":
        base_price *= 1.2
    return base_price

# CASE 1
print("Test 1")
sahi_data = {
    "square_feet": 1500.5,
    "bedrooms": 3,
    "location": "Urban"
}

try:
    validated_request = HousePredictionRequest(**sahi_data)
    prediction = fake_ai_predict(validated_request)
    final_response = HousePredictionResponse(predicted_price=prediction)
    print("API Response JSON:", final_response.model_dump()) # model_dump() dictionary me convert karta hai
except ValidationError as e:
    print(e.json())


print("\n" + "="*40 + "\n")


# CASE 2
print("Test 2")
galat_data = {
    "square_feet": 50,
    "bedrooms": 12,
    "location": "Karachi"
}

try:
    validated_request = HousePredictionRequest(**galat_data)
except ValidationError as e:
    print("❌ Pydantic ne Error Pakad Liya!")
    for error in e.errors():
        print(f"Field '{error['loc'][0]}': {error['msg']}")