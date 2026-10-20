from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from adapters.outbound.persistence.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import UniqueConstraint

class AlertRuleModel(Base):
    __tablename__ = "alertrule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, nullable=True)

    code: str
    metric: str
    direction: str
    open_threshold: float
    close_threshold: float
    message: str
    severity: str = "atencao"
    is_active: bool = True