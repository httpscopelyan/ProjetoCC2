import sys
sys.path.insert(0, "app")

from adapters.outbound.persistence.models.station import StationModel
from adapters.outbound.persistence.models.reading import ReadingModel
from adapters.outbound.persistence.database import SessionLocal

session = SessionLocal()


estacao = StationModel(
    code="est-01",
    name="Estação Teste",
    latitude=-23.5505,
    longitude=-46.6333,
    altitude_m=760.0,
    is_active=True,
)

session.add(estacao)
session.commit()
session.close()

print("Sessão cadastrada")
        
        
        