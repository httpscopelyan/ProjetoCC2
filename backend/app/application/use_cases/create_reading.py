from domain.entities.reading import Reading
from datetime import datetime, timezone
from adapters.outbound.persistence.repositories.sql_reading_repository import SqlReadingRepository 
async def create_reading(leitura, repository):

    leitura = Reading(
        station_id= leitura.station_id,
        measured_at= datetime.now(),
        temperature_c= leitura.temperature_c,
        humidity_pct= leitura.humidity_pct,
        pressure_hpa= leitura.pressure_hpa,
        air_quality_raw= leitura.air_quality_raw,
        luminosity_raw= leitura.luminosity_raw,
        rain_mm= leitura.rain_mm,
        received_at= datetime.now()
    )

    if await repository.existir(leitura.station_id, leitura.measured_at):
        return {"error": "Leitura duplicada"}

    await repository.salvar(leitura)

    return leitura