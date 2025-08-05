import requests
from schemas import Order
from pydantic import ValidationError

base_url = 'http://127.0.0.1:5000'

def validate_response(response, model=None):
    if response.status_code >= 400:
        return response

    try:
        json_data = response.json()
        if model and json_data:
            model(**json_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
    except ValueError:
        print("Invalid JSON response")

    return response

# GET requests
def get_api_data(endpoint, params = {}):
    response = requests.get(f'{base_url}{endpoint}', params=params)
    return response

# POST requests
def post_api_data(endpoint, data):
    response = requests.post(f'{base_url}{endpoint}', json=data)
    return response

# PATCH requests
def patch_api_data(endpoint, data):
    response = requests.patch(f'{base_url}{endpoint}', json=data)
    return response

# DELETE requests
def delete_api_data(endpoint):
    response = requests.delete(f'{base_url}{endpoint}')
    return response  # Typically no response body for DELETE