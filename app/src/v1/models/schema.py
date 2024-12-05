# import app.src.v1.constants as constants

from ..constants import *

from datetime import datetime
from typing import Union, List

import re

from pydantic import BaseModel, validator, root_validator

class CountriesData(BaseModel):
    data: List[str]

class SubscriberClaimsCSV(BaseModel):

    service_date: str
    submitted_procedure: str
    quadrant: Union[str, None] = None
    plan: str
    subscriber: int
    provider_npi: str
    provider_fees: str
    allowed_fees: str
    member_coinsurance: str
    member_copay: str
    net_fee: Union[float, None] = None

    @validator("service_date")
    def service_date_validate(cls, string_value):
        """
        Validate to check if the value adheres to the expected format
        """
        accepted_format = SERVICE_DATE_FORMAT
        try:
            datetime_value = datetime.strptime(string_value.strip(), accepted_format)
        except ValueError:
            raise ValueError(f"Invalid datetime format. Expected format: {accepted_format}")
        return datetime_value


    @validator("submitted_procedure")
    def submitted_procedure_validate(cls, value):
        """
        Validate to check if value starts with "D"
        """
        starts_with_D = re.match(STARTS_WITH_D_REGEX, value.strip())

        if starts_with_D:
            return value.strip()
        else:
            raise ValueError("Invalid string value: Value should start with D")


    @validator("provider_npi")
    def provider_npi_validate(cls, value):
        """
        Validate to check if this value is a 10 digit number
        """
        valid_num = re.match(TEN_DIGIT_NUM_REGEX, value.strip())

        if valid_num:
            return int(value.strip())
        else:
            raise ValueError("Invalid number: this should be a valid 10 digit number")

    @staticmethod
    def extract_fee_value(value: str) -> float:
        valid_price_val = re.match(VALID_PRICE_REGEX, value.strip())

        if valid_price_val:
            value_amount = float("{:.2f}".format(float(value.strip()[1:])))
            return value_amount
        else:
            raise ValueError("Invalid value: value should start with $ sign, followed by a number with two decimal places")


    @validator("provider_fees", "allowed_fees", "member_coinsurance", "member_copay")
    def fee_validate(cls, value):
        """
        Validate to check if value is of the form "$100.00" i.e. a valid price
        """
        return cls.extract_fee_value(value)

    @root_validator(pre=True)
    def validate_net_fee(cls, values):
        """
        Computes net_fee as:
            “net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”
        """
        provider_fees = cls.extract_fee_value(values.get('provider_fees'))
        allowed_fees = cls.extract_fee_value(values.get('allowed_fees'))
        member_coinsurance = cls.extract_fee_value(values.get('member_coinsurance'))
        member_copay = cls.extract_fee_value(values.get('member_copay'))

        if (
            provider_fees is not None
            and allowed_fees is not None
            and member_coinsurance is not None
            and member_copay is not None
        ):
            net_fee = provider_fees + member_coinsurance + member_copay - allowed_fees

            if net_fee < 0:
                raise ValueError("Invalid values for provider fees, allowed fees, member_coinsurance or member_copay")

            values['net_fee'] = round(float(net_fee), 2)

        return values