from enum import Enum
from typing import TypedDict

from descontos.descontos_previdenciarios import calcular_descontos_legais


class ParcelaDecimo(str, Enum):
    UNICA = "unica"
    PRIMEIRA = "primeira"
    SEGUNDA = "segunda"


class ResultadoDecimoTerceiro(TypedDict):
    valor_bruto: float
    desconto_inss: float
    desconto_irpf: float
    valor_liquido: float


def calcular_decimo_terceiro(
        salario_bruto: float,
        meses_trabalhados: int,
        parcela: ParcelaDecimo,
        dependentes: int = 0
) -> ResultadoDecimoTerceiro:

    if not isinstance(parcela, ParcelaDecimo):
        raise ValueError("Parcela inválida")

    elif salario_bruto <= 0:
        raise ValueError("Salário deve ser maior que zero")

    elif not 0 <= meses_trabalhados <= 12:
        raise ValueError("Meses trabalhados deve estar entre 0 e 12")

    salario_mes = salario_bruto / 12
    base_calculo = salario_mes * meses_trabalhados

    valor_bruto = 0.0
    desconto_inss = 0.0
    desconto_irpf = 0.0

    if parcela == ParcelaDecimo.PRIMEIRA:
        valor_bruto = base_calculo / 2

    elif parcela == ParcelaDecimo.SEGUNDA:
        valor_bruto = base_calculo / 2
        desconto_inss, desconto_irpf = calcular_descontos_legais(
            valor_bruto, dependentes
        )

    elif parcela == ParcelaDecimo.UNICA:
        valor_bruto = base_calculo
        desconto_inss, desconto_irpf = calcular_descontos_legais(
            valor_bruto, dependentes
        )

    valor_liquido = valor_bruto - desconto_inss - desconto_irpf


    return {
        "valor_bruto": round(valor_bruto, 2),
        "desconto_inss": round(desconto_inss, 2),
        "desconto_irpf": round(desconto_irpf, 2),
        "valor_liquido": round(valor_liquido, 2)
    }