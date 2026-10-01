from abc import ABC, abstractmethod

from domain.entities.reading import Reading


class ReadingRepository(ABC):
    @abstractmethod
    async def save(self, leitura: Reading) -> None:
        pass

    async def duplicate(self, station_id, measured_at) -> bool:
        pass

    async def exist(self, station_id: str) -> bool: 
        pass

    async def readings_oldfind(self, station_id: str, limit: int = 10) -> list[Reading]:
        pass
