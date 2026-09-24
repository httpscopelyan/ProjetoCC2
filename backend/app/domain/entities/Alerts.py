@dataclass
class AlertRule:
    code: str
    metric: str
    direction: str
    open_threshold: float
    close_threshold: float
    message: str
    severity: str = "atencao"
    is_active: bool = True


@dataclass
class Alert:
    station_id: str
    rule_code: str
    started_at: datetime
    trigger_value: float
    id: int | None = None
    ended_at: datetime | None = None
    peak_value: float | None = None