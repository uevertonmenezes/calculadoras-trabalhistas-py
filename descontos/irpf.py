from decimal import Decimal

from aliquotas.irpf_2026 import (
    TABELA_IRPF_2026,
    ABATIMENTO_ISENCAO_2026,
    LIMITE_ISENCAO_2026,
)


ZERO = Decimal("0.00")


def calcular_irpf(base: Decimal) -> Decimal:
    if base <= ZERO:
        return ZERO

    imposto = ZERO

    for faixa in TABELA_IRPF_2026:
        if base <= faixa["base_ate"]:
            imposto = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
            break

    imposto = max(imposto, ZERO)

    if base <= LIMITE_ISENCAO_2026:
        return ZERO

    imposto -= ABATIMENTO_ISENCAO_2026

    return max(imposto, ZERO)
