from decimal import Decimal
from typing import Tuple

from descontos.inss import calcular_inss
from descontos.irpf import calcular_irpf
from aliquotas.irpf_2026 import DEDUCAO_DEPENDENTE


def calcular_descontos_legais(
        valor_bruto: Decimal,
        dependentes: int = 0
) -> Tuple[Decimal, Decimal]:

    desconto_inss = calcular_inss(valor_bruto)

    base_irpf = valor_bruto - desconto_inss
    base_irpf -= Decimal(dependentes) * DEDUCAO_DEPENDENTE
    base_irpf = max(base_irpf, Decimal("0.00"))

    desconto_irpf = calcular_irpf(base_irpf)

    return desconto_inss, desconto_irpf