from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import TypedDict

from descontos.descontos_previdenciarios import calcular_descontos_legais


class ParcelaDecimo(str, Enum):
    UNICA = "unica"
    PRIMEIRA = "primeira"
    SEGUNDA = "segunda"


class ResultadoDecimoTerceiro(TypedDict):
    valor_bruto: Decimal
    desconto_inss: Decimal
    desconto_irpf: Decimal
    valor_liquido: Decimal


ZERO = Decimal("0.00")

def _to_decimal(valor: float | Decimal) -> Decimal:
    return Decimal(str(valor))


def _arredondar(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _calcular_base_decimo(
        salario_bruto: Decimal,
        meses_trabalhados: int
) -> Decimal:
    return (salario_bruto / Decimal("12")) * Decimal(meses_trabalhados)


def _calcular_fator_parcela(parcela: ParcelaDecimo) -> Decimal:
    if parcela == ParcelaDecimo.UNICA:
        return Decimal("1")

    if parcela in (ParcelaDecimo.PRIMEIRA, ParcelaDecimo.SEGUNDA):
        return Decimal("0.5")

    raise ValueError("Parcela inválida")


def _deve_aplicar_desconto(parcela: ParcelaDecimo) -> bool:
    return parcela in (ParcelaDecimo.UNICA, ParcelaDecimo.SEGUNDA)


def calcular_decimo_terceiro(
        salario_bruto: float | Decimal,
        meses_trabalhados: int,
        parcela: ParcelaDecimo,
        dependentes: int = 0
) -> ResultadoDecimoTerceiro:

    if salario_bruto <= 0:
        raise ValueError("Salário deve ser maior que zero.")

    if not 0 <= meses_trabalhados <= 12:
        raise ValueError("Meses trabalhados deve estar entre 0 e 12.")

    if dependentes < 0:
        raise ValueError("Dependentes não pode ser negativo.")


    salario_bruto = _to_decimal(salario_bruto)

    base_calculo = _calcular_base_decimo(
        salario_bruto,
        meses_trabalhados
    )

    fator = _calcular_fator_parcela(parcela)
    valor_bruto = base_calculo * fator

    desconto_inss = ZERO
    desconto_irpf = ZERO

    if _deve_aplicar_desconto(parcela):
        inss, irpf = calcular_descontos_legais(valor_bruto, dependentes)
        desconto_inss = _to_decimal(inss)
        desconto_irpf = _to_decimal(irpf)

    total_descontos = desconto_inss + desconto_irpf
    valor_liquido = valor_bruto - total_descontos


    return {
        "valor_bruto": _arredondar(valor_bruto),
        "desconto_inss": _arredondar(desconto_inss),
        "desconto_irpf": _arredondar(desconto_irpf),
        "valor_liquido": _arredondar(valor_liquido),
    }