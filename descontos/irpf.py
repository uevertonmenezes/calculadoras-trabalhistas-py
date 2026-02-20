from aliquotas.irpf_2026 import (
    TABELA_IRPF_2026,
    ABATIMENTO_ISENCAO_2026,
    LIMITE_ISENCAO_2026,
)


def calcular_irpf(base: float) -> float:
    if base <= 0:
        return 0.0

    imposto = 0.0

    for faixa in TABELA_IRPF_2026:
        if base <= faixa["base_ate"]:
            imposto = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
            break

    imposto = max(imposto, 0.0)

    if base <= LIMITE_ISENCAO_2026:
        return 0.0

    imposto -= ABATIMENTO_ISENCAO_2026

    return max(imposto, 0.0)
