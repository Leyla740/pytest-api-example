from pydantic import BaseModel
from typing import Optional

pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}
order_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "The order ID"
        },
        "pet_id": {
            "type": "integer",
            "description": "The ID of the pet being ordered"
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"],
            "description": "Current order status"
        }
    },
    "required": ["pet_id"],
    # Changed from False to True to allow additional properties
    "additionalProperties": True
}

class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    type: str  # "cat", "dog", or "fish"
    status: Optional[str] = None  # "available", "sold", or "pending"

class Order(BaseModel):
    id: str
    pet_id: int
    status: Optional[str] = None