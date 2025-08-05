from jsonschema import validate
import pytest
from pydantic import ValidationError
from schemas import Order
from api_helpers import patch_api_data, post_api_data, get_api_data, delete_api_data
import uuid

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def test_pet():
    """Creates a new pet for testing and cleans up afterward"""
    # Create unique test data with an ID
    pet_data = {
        "id": 998,  # Use a high number unlikely to conflict
        "name": f"TestPet-{uuid.uuid4().hex[:4]}",
        "type": "cat",
        "status": "available"
    }

    # Create the pet
    response = post_api_data('/pets/', pet_data)
    assert response.status_code == 201, f"Failed to create test pet: {response.text}"
    pet = response.json()

    yield pet

    # # Cleanup
    # delete_response = delete_api_data(f'/pets/{pet["id"]}')
    # assert delete_response.status_code in [200, 204], "Failed to delete test pet"

@pytest.fixture
def test_order(test_pet):
    """Creates order data using the test pet"""
    return {
        "pet_id": test_pet['id']
    }


def test_update_order_status(test_order, test_pet):
    """Tests the complete order workflow"""
    # Debug print the pet we're using
    print(f"\nUsing pet ID: {test_pet['id']}")

    # 1. Create order
    create_response = post_api_data('/store/order', test_order)
    print("Create Order Response:", create_response.status_code, create_response.text)
    assert create_response.status_code == 201

    # Get the created order data
    order_data = create_response.json()

    # Validate order structure
    try:
        Order(**order_data)  # Note the ** for unpacking the dict
    except ValidationError as e:
        pytest.fail(f"Order validation failed: {str(e)}")

    # 2. Update order status
    update_data = {"status": "sold"}
    order_id = order_data['id']
    patch_response = patch_api_data(f'/store/order/{order_id}', update_data)
    print("Update Order Response:", patch_response.status_code, patch_response.text)

    # Validate response
    assert patch_response.status_code == 200
    assert patch_response.json().get("message") == "Order and pet status updated successfully"

    # 3. Verify pet status changed
    pet_response = get_api_data(f'/pets/{test_pet["id"]}')
    assert pet_response.status_code == 200
    assert pet_response.json()['status'] == "sold"