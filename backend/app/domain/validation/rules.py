from domain.entities.reading import Reading





def Faixa_value (leitura):     
    
    if leitura.temperature_c is None:
        return True
    return -40 <= leitura.temperature_c <= 80

    if leitura.humidity_pct is None:
        return True
    return 0 >= leitura.humidity_pct <= 100
    
    if leitura.pressure_hpa is None:
        return True
    return 300 >= leitura.pressure_hpa <= 1100

    if leitura.air_quality_raw is None:
        return True
    return 0 >= leitura.air_quality_raw <= 4095

    if leitura.luminosity_raw is None:
        return True
    return 0 >= leitura.luminosity_raw <= 4095

    if leitura.rain_mm is None:
        return True
    return 0 >= leitura.rain_mm <= 50

//TODO melhorar código acima . 