from ..services.subscriber_claims_service import upload_claims_service, get_top_providers_service

from fastapi import APIRouter, UploadFile, File

subscriber_claims_router = APIRouter(
    prefix="/subscriber_claims",
    tags=["subscriber_claims"]
)

# 127.0.0.1/upload_claims
@subscriber_claims_router.post("/upload_claims")
async def upload_claims(file: UploadFile = File(...)):
    """
    API to upload claims info from csv file to DB
    """
    data = await upload_claims_service(file)

    # TODO: Improve this response with JSONResponse
    return data


@subscriber_claims_router.get("/top_10_provider_npis")
async def get_top_10_provider_npis():
    """
    API to fetch top 10 provider_npi based on net fee
    """
    data = get_top_providers_service()

    return data


@subscriber_claims_router.post("/test_endpoint")
async def test_endpoint(data):
    if data:
        return vowels_countries(data)
    return []

"""
["spain", "america", "Paris", "Netherlands", "india"]

Create a json response:
    1. return data as:
        1. {"spain":{"a":2, "i":3} ...}



"""
def vowels_countries(data):
    country_vowels = dict()
    for country in data:
        country_vowels[country] = get_vowel_index(country)


def get_vowel_index(country):
    vowels = {"a", "e", "i", "o", "u"}
    idx_vowels = dict()
    for ch in vowels:
        idx_vowels[ch] = []

    for idx, ch in enumerate(country):
        if ch in vowels:
            idx_vowels[ch] = idx_vowels[ch].append(idx)
