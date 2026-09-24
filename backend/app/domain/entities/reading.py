from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Reading:

    station_id: str
    measured_at: datetime

    temperature_c: float | None = None
    humidity_pct: float | None = None
    pressure_hpa: float | None = None
    air_quality_raw: int | None = None
    luminosity_raw: int | None = None
    rain_mm: float | None = None

    received_at: datetime | None = None
    is_valid: bool = True
    flags: list[str] = field(default_factory=list)

    dew_point_c: float | None = None
    heat_index_c: float | None = None
    air_quality_index: int | None = None