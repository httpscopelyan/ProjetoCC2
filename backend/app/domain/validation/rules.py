FAIXAS = {
    "temperature_c": (-40, 80),
    "humidity_pct": (0, 100),
    "pressure_hpa": (300, 1100),
    "air_quality_raw": (0, 4095),
    "luminosity_raw": (0, 4095),
    "rain_mm": (0, 50),
}

CAMPOS_SENSOR = ["temperature_c", "humidity_pct", "pressure_hpa",
                 "air_quality_raw", "luminosity_raw", "rain_mm"]

SALTO_MAXIMO_POR_MINUTO = {
    "temperature_c": 5.0,
    "humidity_pct": 20.0,
    "pressure_hpa": 5.0,
}

def campos_travados(leitura, anteriores, repeticoes=10):
    if len(anteriores) < repeticoes - 1:
        return []

    ultimas = anteriores[:repeticoes - 1]
    travados = []
    for campo in ["temperature_c", "humidity_pct", "pressure_hpa"]:
        atual = getattr(leitura, campo)
        if atual is None:
            continue
        valores = [getattr(r, campo) for r in ultimas]
        if all(v == atual for v in valores):
            travados.append(campo)
    return travados

def campos_com_salto(leitura, anterior):
    if anterior is None:
        return []

    minutos = (leitura.measured_at - anterior.measured_at).total_seconds() / 60
    if minutos <= 0:
        return []

    saltaram = []
    for campo, limite_por_minuto in SALTO_MAXIMO_POR_MINUTO.items():
        atual = getattr(leitura, campo)
        passado = getattr(anterior, campo)
        if atual is None or passado is None:
            continue
        if abs(atual - passado) > limite_por_minuto * minutos:
            saltaram.append(campo)
    return saltaram

def campos_ausentes(leitura):
    return [campo for campo in CAMPOS_SENSOR if getattr(leitura, campo) is None]

def Faixa_value (leitura):      
    fora = []
    for campo, (minimo, maximo) in FAIXAS.items():
        valor = getattr(leitura, campo)
        if valor is None:
            continue
        if not (minimo <= valor <= maximo):
            fora.append(campo)
    return fora
