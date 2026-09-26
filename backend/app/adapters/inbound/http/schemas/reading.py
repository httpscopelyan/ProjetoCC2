from pydantic import BaseModel
from datetime import datetime

class ReadingIn(BaseModel):
    station_id: str | int
    measured_at: datetime | None = None
    temperature_c: float | None = None
    humidity_pct: float | None = None
    pressure_hpa: float | None = None
    air_quality_raw: int | None = None
    luminosity_raw: int | None = None
    rain_mm: float | None = None