import json
from typing import List
from pydantic import BaseModel, Field, ValidationError

# 1. Humne apna strict pinjra (Schema) tayar kiya
class StudentReport(BaseModel):
    name: str
    roll_number: int
    subjects: List[str]
    passed: bool

ai_good_response = '{"name": "Zeeshan", "roll_number": 402, "subjects": ["Maths", "Physics"], "passed": true}'

print("--- Scenario A: Validating Good AI Response ---")
try:
    # model_validate_json() string ko uthata hai, check karta hai aur direct object bana deta hai
    parsed_report = StudentReport.model_validate_json(ai_good_response)
    
    print(f"Success! Student Name: {parsed_report.name}")
    print(f"Roll Number Type: {type(parsed_report.roll_number)}")  # Yeh int hoga

except ValidationError as e:
    print(f"Validation Failed: {e}")

ai_bad_response = '{"name": "Kamran", "roll_number": "Four Hundred", "subjects": ["Chemistry"], "passed": false}'

print("\n--- Scenario B: Validating Bad AI Response ---")
try:
    parsed_report = StudentReport.model_validate_json(ai_bad_response)
except ValidationError as e:
    print("Pydantic caught the error! Backend crash hone se bach gaya.")
    # Pydantic exact bataye ga ke galti kahan hui hai
    print(e)

# Pydantic class ko standard JSON schema instruction mai print karna
print("\n--- This is the schema template sent to LLMs ---")
print(json.dumps(StudentReport.model_json_schema(), indent=2))