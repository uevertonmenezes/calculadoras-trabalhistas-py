from decimal import Decimal, ROUND_HALF_UP

from aliquotas.inss_2026 import TABELA_INSS_2026, TETO_INSS_2026

ZERO = Decimal("0.00")
DUAS_CASAS = Decimal("0.01")


def calcular_inss(base: Decimal) -> Decimal:
    if base <= ZERO:
        return ZERO

    base = min(base, TETO_INSS_2026)

    desconto_total = ZERO
    limite_anterior = ZERO

    for faixa in TABELA_INSS_2026:
        limite_atual = faixa["limite_superior"]
        aliquota = faixa["aliquota"]

        if base > limite_atual:
            valor_faixa = limite_atual - limite_anterior
        else:
            valor_faixa = base - limite_anterior

        if valor_faixa > ZERO:
            desconto_total += valor_faixa * aliquota

        limite_anterior = limite_atual

        if base <= limite_atual:
            break

    return desconto_total.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
