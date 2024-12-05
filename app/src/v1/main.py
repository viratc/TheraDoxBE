from fastapi import FastAPI

# from app.src.v1.controllers.subscriber_claims import subscriber_claims_router
from .controllers.subscriber_claims import subscriber_claims_router  

fastapi_app = FastAPI()

fastapi_app.include_router(subscriber_claims_router)