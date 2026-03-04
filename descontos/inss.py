from decimal import Decimal, ROUND_HALF_UP

from aliquotas.inss_2026 import TABELA_INSS_2026


ZERO = Decimal("0.00")
DUAS_CASAS = Decimal("0.01")


def calcular_inss(base: Decimal) -> Decimal:
    if base <= ZERO:
        return ZERO

    for faixa in TABELA_INSS_2026:
        if base <= faixa["salario_ate"]:
            desconto = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
            desconto = max(desconto, ZERO)
            return desconto.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)

    ultima_faixa = TABELA_INSS_2026[-1]
    teto = ultima_faixa["salario_ate"]

    desconto = (teto * ultima_faixa["aliquota"]) - ultima_faixa["parcela_deduzir"]
    desconto = max(desconto, ZERO)

    return desconto.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
