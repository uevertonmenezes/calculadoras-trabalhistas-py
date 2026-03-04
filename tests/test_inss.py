import pytest
from decimal import Decimal, ROUND_HALF_UP

from descontos.inss import calcular_inss
from aliquotas.inss_2026 import TABELA_INSS_2026


ZERO = Decimal("0.00")
DUAS_CASAS = Decimal("0.01")

# BASES PADRÃO #

BASE_ZERO = Decimal("0.00")
BASE_NEGATIVA = Decimal("-1000.00")
BASE_ACIMA_TETO = Decimal("10000.00")


# LIMITES REAIS DA TABELA #

SALARIOS_LIMITE_FAIXA = [
    faixa["salario_ate"] for faixa in TABELA_INSS_2026
]

ULTIMA_FAIXA = TABELA_INSS_2026[-1]
TETO_INSS = ULTIMA_FAIXA["salario_ate"]


# CASOS BÁSICOS #

def test_inss_base_zero_deve_retornar_zero():
    assert calcular_inss(BASE_ZERO) == ZERO


def test_inss_base_negativa_deve_retornar_zero():
    assert calcular_inss(BASE_NEGATIVA) == ZERO


# FAIXAS SALARIAIS #

@pytest.mark.parametrize("salario", SALARIOS_LIMITE_FAIXA)
def test_inss_limites_exatos_de_faixa_devem_retornar_valor_valido(salario):
    desconto = calcular_inss(salario)
    assert desconto >= ZERO


def test_inss_primeira_faixa_calculo_exato():
    faixa = TABELA_INSS_2026[0]
    base = faixa["salario_ate"]

    esperado = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
    esperado = max(esperado, ZERO)
    esperado = esperado.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)

    desconto = calcular_inss(base)

    assert desconto == esperado


# TETO PREVIDENCIÁRIO #

def test_inss_acima_do_teto_deve_igualar_valor_do_teto():
    desconto_teto = calcular_inss(TETO_INSS)
    desconto_acima = calcular_inss(BASE_ACIMA_TETO)

    assert desconto_acima == desconto_teto


def test_inss_nunca_deve_retornar_valor_negativo():
    desconto = calcular_inss(Decimal("100"))
    assert desconto >= ZERO


# ROBUSTEZ NUMÉRICA #

def test_inss_base_decimal_deve_funcionar_corretamente():
    desconto = calcular_inss(Decimal("4321.78"))
    assert desconto >= ZERO
