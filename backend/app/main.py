from fastapi import FastAPI
from domain.adapters.inbound.http.routes.health import router

app = FastAPI()

app.include_router(router)
