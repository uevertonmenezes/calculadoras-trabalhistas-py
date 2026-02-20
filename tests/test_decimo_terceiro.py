import pytest

from calculadoras_trabalhistas.decimo_terceiro import calcular_decimo_terceiro, ParcelaDecimo


# BASES PADRÃO #

SALARIO_BAIXO = 3000.00
SALARIO_ALTO = 7000.00
SALARIO_ISENTO = 4000.00

MESES_COMPLETO = 12
MESES_ZERO = 0
MESES_INVALIDO = 13

DEP_ZERO = 0
DEP_UM = 1
DEP_DOIS = 2


# CASOS BÁSICOS - PARCELAS #

def test_primeira_parcela_sem_descontos():
    resultado = calcular_decimo_terceiro(
        salario_bruto=SALARIO_BAIXO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.primeira
    )

    assert resultado["valor_bruto"] == pytest.approx(1500.00, 0.01)
    assert resultado["desconto_inss"] == 0.0
    assert resultado["desconto_irpf"] == 0.0
    assert resultado["valor_decimo_terceiro"] == pytest.approx(1500.00, 0.01)


def test_segunda_parcela_com_descontos():
    resultado = calcular_decimo_terceiro(
        salario_bruto=SALARIO_BAIXO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.segunda
    )

    assert resultado["valor_bruto"] == pytest.approx(1500.00, 0.01)
    assert resultado["desconto_inss"] > 0
    assert resultado["desconto_irpf"] >= 0
    assert resultado["valor_decimo_terceiro"] < resultado["valor_bruto"]


def test_parcela_unica_com_descontos():
    resultado = calcular_decimo_terceiro(
        salario_bruto=SALARIO_BAIXO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.unica
    )

    assert resultado["valor_bruto"] == pytest.approx(3000.00, 0.01)
    assert resultado["desconto_inss"] > 0
    assert resultado["desconto_irpf"] >= 0
    assert resultado["valor_decimo_terceiro"] < resultado["valor_bruto"]


# DEPENDENTES #

def test_dependentes_reduzem_irpf_quando_ha_imposto():
    sem_dependentes = calcular_decimo_terceiro(
        salario_bruto=SALARIO_ALTO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.unica,
        dependentes=DEP_ZERO
    )
    com_dependentes = calcular_decimo_terceiro(
        salario_bruto=SALARIO_ALTO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.unica,
        dependentes=DEP_UM
    )

    assert sem_dependentes["desconto_irpf"] > 0
    assert com_dependentes["desconto_irpf"] < sem_dependentes["desconto_irpf"]


def test_dependentes_nao_afetam_irpf_quando_isento():
    sem_dependentes = calcular_decimo_terceiro(
        salario_bruto=SALARIO_ISENTO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.unica,
        dependentes=DEP_ZERO
    )
    com_dependentes = calcular_decimo_terceiro(
        salario_bruto=SALARIO_ISENTO,
        meses_trabalhados=MESES_COMPLETO,
        parcela=ParcelaDecimo.unica,
        dependentes=DEP_DOIS
    )

    assert sem_dependentes["desconto_irpf"] == 0.0
    assert com_dependentes["desconto_irpf"] == 0.0


# VALORES ESPECIAIS #

def test_decimo_terceiro_com_zero_meses_trabalhados():
    resultado = calcular_decimo_terceiro(
        salario_bruto=SALARIO_ISENTO,
        meses_trabalhados=MESES_ZERO,
        parcela=ParcelaDecimo.unica
    )

    assert resultado["valor_decimo_terceiro"] == 0.0


# VALIDAÇÕES DE ERRO #

@pytest.mark.parametrize("parcela_invalida", ["terceira", 123, None])
def test_parcela_invalida_deve_gerar_erro(parcela_invalida):
    with pytest.raises(ValueError):
        calcular_decimo_terceiro(SALARIO_BAIXO, MESES_COMPLETO, parcela_invalida)


def test_salario_invalido_deve_gerar_erro():
    with pytest.raises(ValueError):
        calcular_decimo_terceiro(0, MESES_COMPLETO, ParcelaDecimo.unica)


def test_meses_trabalhados_invalidos_deve_gerar_erro():
    with pytest.raises(ValueError):
        calcular_decimo_terceiro(SALARIO_BAIXO, MESES_INVALIDO, ParcelaDecimo.unica)
