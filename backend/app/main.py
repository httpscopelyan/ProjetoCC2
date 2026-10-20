from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters.inbound.http.routes.health import router
from adapters.inbound.http.routes.reading import reading_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(reading_routes)
