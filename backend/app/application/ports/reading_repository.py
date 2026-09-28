from abc import ABC, abstractmethod

from domain.entities.reading import Reading


class ReadingRepository(ABC):
    @abstractmethod
    async def salvar(self, leitura: Reading) -> None:
        pass

    async def existir(self, station_id, measured_at) -> bool:
        pass