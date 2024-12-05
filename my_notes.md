Transform a JSON payload representing a single claim input with multiple lines and store it in a RDB:
    1. Should this be a service, running for perpetuity ? 
    2. Should this be an API endpoint ? NO
    3. Schema of DB ? 
    4. DB models ? Migrations ? 
    5. Data validation ? 
    6.  Please add data validation for *“submitted procedure”* and *“Provider NPI”* columns. *“Submitted procedure”* always begins with the letter ‘D’ and *“Provider NPI”* is always a 10 digit number. The data validation should be flexible to allow for other validation rules as needed. All fields except *”quadrant”* are required.
    7. Regex:
        a. 10 digit number: ^[1-9]\d{9}$
        b. Begins with D: ^D
        c. Begins with $: ^$

Unique ID per claim:
    1. How is this invoked ? 
    2. Part of each entry in DB ?

Computes the *“net fee”* as :
    1. *“net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”* (note again that the names are not consistent in capitalization).
    2. Is this an API endpoint ?
        a. A downstream service, **payments**, will consume *“net fee”* computed by **claim_process**.

Implement an endpoint that returns the top 10 provider_npis by net fees generated:
    1. The endpoint should be optimized for performance
    2. Explain the data structure and algorithm used to compute the top 10 provider_npis
    3. Good to have a rate limiter to this api (probably 10 req/min)

Approach:
    1. DB layer (model, schema, validations, migrations)
    2. Writing API endpoints 
    3. Test cases
    4. Logging (if time permits)
    5. API rate limiter (Only write up) 
    6. Dockerisation 
    7. Final write up with explanation for fetching top 10 records 

 

