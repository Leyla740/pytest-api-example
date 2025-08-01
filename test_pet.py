from jsonschema import validate
import pytest
import schemas
import api_helpers
from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    # Validate response matches pet schema
    pet_data = response.json()
    validate(instance=pet_data, schema=schemas.pet)

    # Additional validation for required fields
    assert "name" in pet_data, "Pet data missing 'name' field"
    assert "type" in pet_data, "Pet data missing 'type' field"

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {"status": status}

    response = api_helpers.get_api_data(test_endpoint, params)

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    pets = response.json()
    assert isinstance(pets, list), "Response should be a list of pets"

    for pet in pets:
        # Validate each pet matches the status
        assert pet["status"] == status, f"Pet status should be {status}"
        # Validate each pet matches the schema
        validate(instance=pet, schema=schemas.pet)
    # TODO...

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''


@pytest.mark.parametrize("invalid_id", [-1, 999999, "invalid"])
def test_get_by_id_404(invalid_id):
    test_endpoint = f"/pets/{invalid_id}"
    response = api_helpers.get_api_data(test_endpoint)

    # First assert the status code is 404
    assert response.status_code == 404, (
        f"Expected 404 for invalid ID {invalid_id}, got {response.status_code}"
    )

    # Handle cases where the response might not be JSON
    try:
        error_data = response.json()
        # If JSON is returned, validate it has a message (common API pattern)
        if error_data:  # Only check if response has content
            assert "message" in error_data, "Error response should contain 'message'"
    except ValueError:
        # If response isn't JSON, just confirm it's a 404
        pass  # Some APIs return plain text 404 pages - that's fine for this test

# Notes: fixes: updated pet's name type from "integer" to "string"
# imported needed packages
# exception handling is added for negative testing, to validate response not being in Json
