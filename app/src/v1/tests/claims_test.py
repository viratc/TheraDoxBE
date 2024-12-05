import pytest
from fastapi.testclient import TestClient
from ..main import fastapi_app
from ..models.model import SubscriberClaimsModel

client = TestClient(fastapi_app)

##### Tests for upload_claims API
@pytest.fixture
def csv_file():
    # Return a sample CSV file
    return open("sample.csv", "rb")

def test_upload_claims_valid_csv(csv_file):
    response = client.post("/upload_claims", files={"file": csv_file})
    assert response.status_code == 200
    assert response.json() == {"success": True}

def test_upload_claims_invalid_csv(csv_file):
    # Modify the content type to something other than CSV

    csv_file.headers["Content-Type"] = "text/plain"
    response = client.post("/upload_claims", files={"file": csv_file})
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files are allowed"}

def test_upload_claims_insufficient_rows(csv_file):
    # Modify the CSV content to have only 1 row (insufficient)

    csv_file.content = b"header1,header2,header3\nvalue1,value2,value3"
    response = client.post("/upload_claims", files={"file": csv_file})
    assert response.status_code == 400
    assert response.json() == {"detail": "CSV file should have at least two rows: header and data."}

def test_upload_claims_exception(csv_file, mocker):
    # Mock the write_claims_to_db function to raise an exception

    mocker.patch("app.SubscriberClaimsModel.write_claims_to_db", side_effect=Exception("DB error"))
    response = client.post("/upload_claims", files={"file": csv_file})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

##### Tests for top_10_provider_npis API
@pytest.fixture
def mock_fetch_top_ten_provider_npi(mocker):
    # Mock the fetch_top_ten_provider_npi method to return sample data

    top_ten_providers = [("1122334455",), ("2233445566",), ("7777777777",)]
    mocker.patch.object(SubscriberClaimsModel, "fetch_top_ten_provider_npi", return_value=top_ten_providers)

def test_get_top_10_provider_npis(mock_fetch_top_ten_provider_npi):
    response = client.get("/top_10_provider_npis")
    assert response.status_code == 200
    assert response.json() == ["1122334455", "2233445566", "7777777777"]

def test_get_top_10_provider_npis_exception(mock_fetch_top_ten_provider_npi, mocker):
    # Mock the fetch_top_ten_provider_npi method to raise an exception

    mocker.patch.object(SubscriberClaimsModel, "fetch_top_ten_provider_npi", side_effect=Exception("DB error"))
    response = client.get("/top_10_provider_npis")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}