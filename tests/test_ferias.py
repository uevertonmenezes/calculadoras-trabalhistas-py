from calculadoras_trabalhistas.ferias import calcular_ferias, AbonoPecuniario, AdiantarDecimo
import pytest


def test_calculo_basico_sem_abono():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["valor_proporcional"] > 0
    assert resultado["terco_ferias"] == resultado["valor_proporcional"] / 3
    assert resultado["desconto_inss"] >= 0
    assert resultado["desconto_irpf"] >= 0


def test_com_abono_pecuniario():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.sim,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["abono_pecuniario"] > 0
    assert resultado["terco_abono_pecuniario"] == round(resultado["abono_pecuniario"] / 3, 2)


def test_com_adiantamento_decimo():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.sim,
        dependentes=0
    )

    assert resultado["adiantamento_parcela_decimo"] == 1500


def test_salario_negativo():
    with pytest.raises(ValueError):
        calcular_ferias(
            salario_bruto=-1000,
            media_horas_extras=0,
            dias_ferias=30,
            abono_pecuniario=AbonoPecuniario.nao,
            adiantar_decimo=AdiantarDecimo.nao,
            dependentes=0
        )


def test_dias_invalidos():
    with pytest.raises(ValueError):
        calcular_ferias(
            salario_bruto=3000,
            media_horas_extras=0,
            dias_ferias=40,
            abono_pecuniario=AbonoPecuniario.nao,
            adiantar_decimo=AdiantarDecimo.nao,
            dependentes=0
        )


def test_ferias_proporcional():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=15,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["valor_proporcional"] == 1500
