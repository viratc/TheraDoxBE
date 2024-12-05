import csv

from ..models.model import SubscriberClaimsModel
from ..models.schema import SubscriberClaimsCSV
from ..constants import *

from fastapi import HTTPException, File

def is_csv_file(file: File) -> bool:
    return file.filename.endswith(".csv")

def csv_to_json(rows: list, header: list) -> list:
    return [dict(zip(header, row)) for row in rows]

def is_valid_csv_header(header: list) -> bool:
    return header == CSV_HEADER_ROW

async def upload_claims_service(file):
    if not is_csv_file(file):
        raise HTTPException(status_code=400, detail="Only csv files are allowed") 
    
    # Read the contents of the uploaded file
    contents = await file.read()  

    # Decode the binary contents to a string
    decoded_contents = contents.decode("utf-8")  

    # Parse the CSV data
    csv_data = csv.reader(decoded_contents.splitlines(), delimiter=',')

    # Extract the rows from the CSV data
    rows = [row for row in csv_data] 

    # We need atleast 2 rows 
    if len(rows) < 2:
        raise HTTPException(status_code=400, detail="CSV file should have at least two rows: header and data.")

    # The first row is the header
    header = rows[0]

    if not is_valid_csv_header(header):
        raise HTTPException(status_code=400, detail="Header row does not conform to the expected format")

    # Mapping fields from csv with fields in our schema
    map_fields = dict(zip(header, SubscriberClaimsCSV.__fields__.keys()))

    # List of dicts of SubscriberClaims
    json_data = csv_to_json(rows[1:], map_fields.values())

    validated_json_data = list()
    for row in json_data:
        data = SubscriberClaimsCSV(**row)
        validated_json_data.append(data.dict())

    # Pass validated_json_data as a JSON object to be written into the DB 
    SubscriberClaimsModel.write_claims_to_db(validated_json_data)
    
    return validated_json_data

def get_top_providers_service():

    top_ten_providers = SubscriberClaimsModel.fetch_top_ten_provider_npi()

    # Improve this to maybe use Fast API native hacks
    top_ten = [npi[0] for npi in top_ten_providers]

    return top_ten