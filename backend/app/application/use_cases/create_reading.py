from domain.entities.reading import Reading
from datetime import datetime, timezone

antigos = []
atual = []

def conversao(valor):
    try:
        return int(valor)
    except ValueError:
        return float(valor)
async def create_reading(leitura): 

      

    leitura = Reading(
        station_id= leitura.station_id,
        measured_at= datetime.now(timezone.utc),
        temperature_c= leitura.temperature_c,
        humidity_pct= leitura.humidity_pct,
        pressure_hpa= leitura.pressure_hpa,
        air_quality_raw= leitura.air_quality_raw,
        luminosity_raw= leitura.luminosity_raw,
        rain_mm= leitura.rain_mm,
        received_at= datetime.now(timezone.utc)
    )

    if not leitura.station_id and leitura.station_id  == None :
        return {"message": "Envie um nome para a estação!"}

    for i, n in enumerate(antigos):
        if not (i < 1 or i == 0):
            continue

    for campo in ["temperature_c", "humidity_pct", "pressure_hpa", "air_quality_raw", "luminosity_raw", "rain_mm"]:
        atual.append(getattr(leitura, campo))
        dados_atuais = ",".join(map(str, atual))
    string__valores = dados_atuais.split(",")

    for x in string__valores: 
        antigos.append(conversao(x))

    duplicatas_Nverificadas = set(atual) & set(antigos)    
    duplicadas_verificadas = len(atual) - len(duplicatas_Nverificadas)
    print(duplicadas_verificadas)
    if (duplicadas_verificadas == 3):
        print("3 itens duplicados", duplicatas_Nverificadas)



    return leitura
            
    #for i, n in enumerate(antigos):
    
        # print(antigos[i].station_id)
        # if not (i == 1):
        #     continue
        # ns= antigos[1].station_id = "est-02"
        # print(ns)
        