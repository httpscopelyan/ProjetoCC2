from domain.entities.reading import  Reading
from domain.validation.rules import Faixa_value
from domain.validation.rules import campos_ausentes
from domain.validation.rules import campos_com_salto
from domain.validation.rules import campos_travados

def validate(readings: Reading, olds= None, anteriores=None  ): 
    anteriores = anteriores or []
    
    fora = Faixa_value(readings)
    ausentes = campos_ausentes(readings)
    saltos = campos_com_salto(readings, olds)
    travados = campos_travados(readings, anteriores, repeticoes=10)

    flags = (
        [f"{c}_out_of_range" for c in fora]
        + [f"{c}_missing" for c in ausentes]
        + [f"{c}_jump" for c in saltos]
        + [f"{c}_stuck" for c in travados]
    )
    is_valid = not (fora or ausentes or saltos or travados)

    return is_valid, flags