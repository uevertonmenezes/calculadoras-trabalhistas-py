import pytest
from decimal import Decimal, ROUND_HALF_UP

from descontos.inss import calcular_inss
from aliquotas.inss_2026 import TABELA_INSS_2026, TETO_INSS_2026


ZERO = Decimal("0.00")
DUAS_CASAS = Decimal("0.01")

# BASES PADRÃO #

BASE_ZERO = Decimal("0.00")
BASE_NEGATIVA = Decimal("-1000.00")
BASE_ACIMA_TETO = Decimal("10000.00")


# CASOS BÁSICOS #

def test_inss_base_zero_deve_retornar_zero():
    assert calcular_inss(BASE_ZERO) == ZERO


def test_inss_base_negativa_deve_retornar_zero():
    assert calcular_inss(BASE_NEGATIVA) == ZERO


# PRIMEIRA FAIXA SALARIAL#

def test_inss_primeira_faixa_calculo_exato():
    primeira_faixa = TABELA_INSS_2026[0]
    base = primeira_faixa["limite_superior"]

    esperado = base * primeira_faixa["aliquota"]
    esperado = esperado.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)

    desconto = calcular_inss(base)

    assert desconto == esperado


# TESTE PROGRESSIVO REAL #

def test_inss_calculo_progressivo_exemplo_real():
    base = Decimal("3000.00")
    desconto = calcular_inss(base)

    assert desconto > ZERO


# TETO PREVIDENCIÁRIO #

def test_inss_acima_do_teto_deve_igualar_valor_do_teto():
    desconto_teto = calcular_inss(TETO_INSS_2026)
    desconto_acima = calcular_inss(BASE_ACIMA_TETO)

    assert desconto_acima == desconto_teto


def test_inss_nunca_deve_retornar_valor_negativo():
    desconto = calcular_inss(Decimal("100.00"))
    assert desconto >= ZERO


def test_inss_base_decimal_deve_funcionar_corretamente():
    desconto = calcular_inss(Decimal("4321.78"))
    assert desconto >= ZERO


# VALORES OFICIAIS DA TABELA INSS #

@pytest.mark.parametrize(
    "salario, desconto_esperado",
    [
        (Decimal("1621.00"), Decimal("121.58")),
        (Decimal("2902.84"), Decimal("236.94")),
        (Decimal("4354.27"), Decimal("411.11")),
        (Decimal("8475.55"), Decimal("988.09")),
        (Decimal("10000.00"), Decimal("988.09")),
    ],
)
def test_inss_valores_oficiais_devem_bater_exatamente(salario, desconto_esperado):
    resultado = calcular_inss(salario)
    assert resultado == desconto_esperado
