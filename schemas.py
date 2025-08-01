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
    "additionalProperties": False
}
order_update_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        }
    },
    "additionalProperties": False
}