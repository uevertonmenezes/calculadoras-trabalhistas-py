import pytest

from descontos.irpf import calcular_irpf
from aliquotas.irpf_2026 import (
    TABELA_IRPF_2026,
    ABATIMENTO_ISENCAO_2026, LIMITE_ISENCAO_2026,
)


# BASES PADRÃO #

BASE_ZERO = 0
BASE_NEGATIVA = -1000
BASE_ISENCAO_FIXA = 5000
BASE_PRIMEIRA_FAIXA = 5500
BASE_ULTIMA_FAIXA = 12000
BASE_PROXIMA_ISENCAO = LIMITE_ISENCAO_2026 + 0.01
BASE_DECIMAL = 7324.87


# CASOS BÁSICOS #

def test_irpf_base_zero_deve_retornar_zero():
    assert calcular_irpf(BASE_ZERO) == pytest.approx(0.0, 0.01)


def test_irpf_base_negativa_deve_retornar_zero():
    assert calcular_irpf(BASE_NEGATIVA) == pytest.approx(0.0, 0.01)


def test_irpf_deve_zerar_na_faixa_de_isencao_2026():
    # Mesmo que a tabela gere imposto,o abatimento 2026 deve zerar.
    assert calcular_irpf(BASE_ISENCAO_FIXA) == pytest.approx(0.0, 0.01)


def test_irpf_no_limite_exato_de_isencao_deve_retornar_zero():
    assert calcular_irpf(LIMITE_ISENCAO_2026) == pytest.approx(0.0, 0.01)


# FAIXAS TRIBUTÁVEIS #

def test_irpf_primeira_faixa_tributavel_deve_ser_maior_que_zero():
    imposto = calcular_irpf(BASE_PRIMEIRA_FAIXA)
    assert imposto > 0


def test_irpf_limite_exato_primeira_faixa_deve_calcular_corretamente():
    faixa = TABELA_IRPF_2026[0]
    base = faixa["base_ate"]

    imposto = calcular_irpf(base)

    esperado = (base * faixa["aliquota"]) - faixa["parcela_deduzir"]
    esperado -= ABATIMENTO_ISENCAO_2026

    assert imposto == pytest.approx(max(esperado, 0), 0.01)


def test_irpf_ultima_faixa_deve_ser_maior_que_zero():
    imposto = calcular_irpf(BASE_ULTIMA_FAIXA)
    assert imposto > 0


def test_irpf_base_acima_da_ultima_faixa_deve_retornar_valor_valido():
    base = TABELA_IRPF_2026[-1]["base_ate"] + 1000
    imposto = calcular_irpf(base)
    assert imposto >= 0


# REGRA DE ISENÇÃO E ABATIMENTO #

def test_irpf_logo_acima_do_limite_deve_ser_maior_ou_igual_a_zero():
    imposto = calcular_irpf(BASE_PROXIMA_ISENCAO)
    assert imposto >= 0


def test_irpf_nunca_deve_retornar_valor_negativo():
    imposto = calcular_irpf(LIMITE_ISENCAO_2026 + 100)
    assert imposto >= 0


# ROBUSTEZ NUMÉRICA #

def test_irpf_base_decimal_deve_funcionar_corretamente():
    imposto = calcular_irpf(BASE_DECIMAL)
    assert imposto >= 0
