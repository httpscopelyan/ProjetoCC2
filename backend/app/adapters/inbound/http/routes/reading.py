from fastapi import APIRouter
from adapters.inbound.http.schemas.reading import ReadingIn
from application.use_cases.create_reading import create_reading
from adapters.outbound.persistence.database import SessionLocal
from adapters.outbound.persistence.repositories.sql_reading_repository import SqlReadingRepository

reading_routes = APIRouter()

@reading_routes.post("/api/v1/readings")
async def posting_readings(dados: ReadingIn):

    session = SessionLocal()

    try:
        repository = SqlReadingRepository(session)
        leituras = await create_reading(dados, repository)
        return {
            "dados": leituras
        }
    finally:
        session.close()