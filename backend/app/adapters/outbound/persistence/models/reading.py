from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from adapters.outbound.persistence.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import UniqueConstraint


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    station_id: Mapped[str] = mapped_column(String, ForeignKey("stations.code"), nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity_pct: Mapped[float| None] = mapped_column(Float, nullable=True)
    pressure_hpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    air_quality_raw: Mapped[int | None] = mapped_column(Integer, nullable=True)
    luminosity_raw: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rain_mm: Mapped[float| None] = mapped_column(Float, nullable=True)

    received_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    dew_point_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat_index_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    air_quality_index: Mapped[int | None] = mapped_column(Integer, nullable=True)


    __table_args__ = (
        UniqueConstraint("station_id", "measured_at", name="uq_station_measured"),
    )