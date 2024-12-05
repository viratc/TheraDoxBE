SERVICE_DATE_FORMAT = "%m/%d/%y %H:%M"
STARTS_WITH_D_REGEX = "^D"
TEN_DIGIT_NUM_REGEX = "^[1-9]\d{9}$"
VALID_PRICE_REGEX = "^\$\d+\.\d{2}$"
DEFAULT_POSTGRES_USER = "postgres"
DEFAULT_POSTGRES_PASSWORD = "password"
DEFAULT_POSTGRES_URL = "127.0.0.1:5432/subscriber_claims"
CSV_HEADER_ROW = ["service date", "submitted procedure", "quadrant", "Plan/Group #",  
                  "Subscriber#", "Provider NPI", "provider fees", "Allowed fees", \
                  "member coinsurance", "member copay"]

