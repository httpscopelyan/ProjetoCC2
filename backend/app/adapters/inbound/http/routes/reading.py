from fastapi import APIRouter
from adapters.inbound.http.schemas.reading import ReadingIn
from application.use_cases.create_reading import create_reading

reading_routes = APIRouter()

@reading_routes.post("/api/v1/readings")
async def posting_readings(dados: ReadingIn):

    leituras = await create_reading(dados)
    return {
        "dados": leituras
    }
        