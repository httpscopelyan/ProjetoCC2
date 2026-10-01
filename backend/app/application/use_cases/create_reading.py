from domain.entities.reading import Reading
from datetime import datetime, timezone
from adapters.outbound.persistence.repositories.sql_reading_repository import SqlReadingRepository
from domain.validation.validation import validate


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

    if not await repository.exist(leitura.station_id): 
        return {"error": "Esta estação não existe ou não esta cadastrada"}

    if await repository.duplicate(leitura.station_id, leitura.measured_at):
        return {"error": "Leitura duplicada"}
    
    oldreadings = await repository.readings_oldfind(leitura.station_id, limit=10)

    anterior = oldreadings[0] if oldreadings else None
    is_valid, flags = validate(leitura, anterior, oldreadings)

    leitura.is_valid = is_valid
    leitura.flags = flags

    await repository.save(leitura)

    return leitura