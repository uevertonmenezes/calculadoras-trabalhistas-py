from descontos.inss import calcular_inss
from descontos.irpf import calcular_irpf
from aliquotas.irpf_2026 import DEDUCAO_DEPENDENTE
from typing import Tuple


def calcular_descontos_legais(
        valor_bruto: float,
        dependentes: int = 0
) -> Tuple[float, float]:

    desconto_inss = calcular_inss(valor_bruto)

    base_irpf = valor_bruto - desconto_inss
    base_irpf -= dependentes * DEDUCAO_DEPENDENTE
    base_irpf = max(base_irpf, 0.0)

    desconto_irpf = calcular_irpf(base_irpf)

    return desconto_inss, desconto_irpf
