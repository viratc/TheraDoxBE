"""
DB Model 
"""
from ..models.db import db_session, Base

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float, func

class SubscriberClaimsModel(Base):
    __tablename__ = "subscriber_claims"

    id = Column(Integer, primary_key=True)
    service_date = Column(DateTime)
    submitted_procedure = Column(String)
    quadrant = Column(String)
    plan = Column(String)
    subscriber = Column(BigInteger)
    provider_npi = Column(BigInteger)
    provider_fees = Column(Float)
    allowed_fees = Column(Float)
    member_coinsurance = Column(Float)
    member_copay = Column(Float)
    net_fee = Column(Float)

    @staticmethod
    def write_claims_to_db(subscriber_claims):
        session_to_use = db_session()

        try:
            for claim in subscriber_claims:
                model_claim = SubscriberClaimsModel(**claim)
                session_to_use.add(model_claim)

            session_to_use.commit()

        except Exception as e:
            session_to_use.rollback()
            raise e

        finally:
            session_to_use.close()

    @staticmethod
    def fetch_top_ten_provider_npi():
        session_to_use = db_session()

        try:

            #### This works if there are no duplicates
            # Query: SELECT TOP 10 provider_npis FROM subscriber_claims ORDER BY net_fee DESC 
            # top_10_providers = session_to_use.query(
            #     SubscriberClaimsModel.provider_npi
            # ).order_by(
            #     desc(SubscriberClaimsModel.net_fee)
            # ).limit(10).all()

            # Order the records by the sum of net_fee in descending order, and group_by provider_npi
            # Thanks chatGPT
            subquery = (
                session_to_use.query(SubscriberClaimsModel.provider_npi)
                .order_by(func.sum(SubscriberClaimsModel.net_fee).desc())
                .group_by(SubscriberClaimsModel.provider_npi)
                .subquery()
            )

            # Retrieves the distinct provider_npi values from the subquery
            top_10_provider_npi = (
                session_to_use.query(subquery.c.provider_npi)
                .distinct()
                .limit(10)
                .all()
            )

            return top_10_provider_npi
        
        except Exception as e:
            raise e 
        
        finally:
            session_to_use.close()



