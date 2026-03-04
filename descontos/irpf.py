from decimal import Decimal, ROUND_HALF_UP

from aliquotas.irpf_2026 import (
    TABELA_IRPF_2026,
    ABATIMENTO_ISENCAO_2026,
    LIMITE_ISENCAO_2026,
)


ZERO = Decimal("0.00")
DUAS_CASAS = Decimal("0.01")


def calcular_irpf(base: Decimal) -> Decimal:
    if base <= ZERO or base <= LIMITE_ISENCAO_2026:
        return ZERO

    imposto = ZERO

    for faixa in TABELA_IRPF_2026:
        if base <= faixa["base_ate"]:
            imposto = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
            break

    imposto = max(imposto, ZERO)
    imposto -= ABATIMENTO_ISENCAO_2026
    imposto = max(imposto, ZERO)

    return imposto.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
