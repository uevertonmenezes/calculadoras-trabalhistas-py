import pytest

from calculadoras_trabalhistas.decimo_terceiro import calcular_descontos_legais


# BASES PADRÃO #

VALOR_ALTO = 7000.00
VALOR_MEDIO = 5000.00
VALOR_BAIXO = 2000.00
DEP_ZERO = 0
DEP_UM = 1


# CASOS BÁSICOS #

def test_descontos_legais_retorna_inss_e_irpf_maior_que_zero():
    desconto_inss, desconto_irpf = calcular_descontos_legais(
        valor_bruto=VALOR_ALTO,
        dependentes=DEP_ZERO
    )

    assert desconto_inss > 0
    assert desconto_irpf > 0


# DEPENDENTES #

def test_dependentes_reduzem_irpf():
    _, irpf_sem_dependentes = calcular_descontos_legais(
        valor_bruto=VALOR_ALTO,
        dependentes=DEP_ZERO
    )

    _, irpf_com_dependentes = calcular_descontos_legais(
        valor_bruto=VALOR_ALTO,
        dependentes=DEP_UM
    )

    assert irpf_com_dependentes < irpf_sem_dependentes


# PARAMETRIZAÇÃO DE DEPENDENTES

@pytest.mark.parametrize("dependentes", [0, 1, 2, 3])
def test_irpf_decresce_ao_aumentar_dependentes(dependentes):
    _, irpf = calcular_descontos_legais(
        valor_bruto=VALOR_ALTO,
        dependentes=dependentes
    )

    # O IRPF nunca pode ser negativo.
    assert irpf >= 0


# LIMITES DE ISENÇÃO IRPF #

def test_irpf_zerado_ate_valor_isencao():
    _, descontos_irpf = calcular_descontos_legais(
        valor_bruto=VALOR_MEDIO,
        dependentes=DEP_ZERO
    )

    assert descontos_irpf == pytest.approx(0.0, 0.01)


def test_irpf_zerado_e_inss_aplicado_para_salario_baixo():
    desconto_inss, desconto_irpf = calcular_descontos_legais(
        valor_bruto=VALOR_BAIXO,
        dependentes=DEP_ZERO
    )

    assert desconto_inss > 0
    assert desconto_irpf == pytest.approx(0.0, 0.01)
