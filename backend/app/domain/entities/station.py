@dataclass

class Station: 

    code: str
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    altitude_m: float | None = None
    installed_at: datetime | None = None
    is_active: bool = True