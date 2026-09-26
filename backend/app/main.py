from fastapi import FastAPI
from adapters.inbound.http.routes.health import router
from adapters.inbound.http.routes.reading import reading_routes

app = FastAPI()

app.include_router(router)
app.include_router(reading_routes)
