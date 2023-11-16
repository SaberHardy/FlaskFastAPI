import json
import pytest
from not_real_time import app


@pytest.fixture
def client():
    # Create a test client using the Flask application
    with app.test_client() as client:
        yield client


def test_get_data(client):
    # Send a GET request to the /file-api/data endpoint
    response = client.get('/file-api/data')
    # print(f'data contain {response.data}')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the JSON response
    data = json.loads(response.get_data(as_text=True))
    # print(f"the data is {data[0]['amount']}")
    # Check the structure of the JSON response
    assert isinstance(data, list)
    # Do the assert according to what you have in the json return file
    for item in data:
        assert 'id' in item
        assert 'amount' in item
        assert 'type' in item
        assert 'oldbalanceOrg' in item
        assert 'newbalanceOrig' in item
        assert 'nameDest' in item
        assert 'isFraud' in item
        assert 'isFlaggedFraud' in item


if __name__ == '__main__':
    pytest.main()
