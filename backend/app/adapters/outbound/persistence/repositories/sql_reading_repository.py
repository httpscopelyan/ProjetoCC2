from sqlalchemy.orm import Session
from application.ports.reading_repository import ReadingRepository
from adapters.outbound.persistence.models.reading import ReadingModel
from adapters.outbound.persistence.models.station import StationModel
from domain.entities.reading import Reading


class SqlReadingRepository(ReadingRepository):

    def __init__(self, session: Session):
        self.session = session

    async def save(self, leitura: Reading) -> None:
        model = ReadingModel(
            station_id=leitura.station_id,
            measured_at=leitura.measured_at,
            received_at=leitura.received_at,
            temperature_c=leitura.temperature_c,
            humidity_pct=leitura.humidity_pct,
            pressure_hpa=leitura.pressure_hpa,
            air_quality_raw=leitura.air_quality_raw,
            luminosity_raw=leitura.luminosity_raw,
            rain_mm=leitura.rain_mm,
            is_valid=leitura.is_valid,
            flags=leitura.flags,
            dew_point_c=leitura.dew_point_c,
            heat_index_c=leitura.heat_index_c,
            air_quality_index=leitura.air_quality_index,
        )
        self.session.add(model)
        self.session.commit()


    async def duplicate(self, station_id, measured_at) -> bool:

        existente = self.session.query(ReadingModel).filter(
            ReadingModel.station_id == station_id,
            ReadingModel.measured_at == measured_at,
        ).first()

        if not existente: 
            return False
        
    async def exist(self, station_id: str) -> bool:
        return (
            self.session.query(StationModel).filter(
                StationModel.code == station_id
            ).first()
        ) is not None
        
    async def readings_oldfind(self, station_id: str, limit: int = 10) -> list[Reading]:
        
        rows = (
            self.session.query(ReadingModel)
            .filter(ReadingModel.station_id == station_id, ReadingModel.is_valid == True)
            .order_by(ReadingModel.measured_at.desc())
            .limit(limit)
            .all()
        )

        return rows
