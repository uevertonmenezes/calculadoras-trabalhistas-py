from calculadoras_trabalhistas.ferias import calcular_ferias, AbonoPecuniario, AdiantarDecimo

def test_calculo_basico_sem_abono():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0.0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["valor_proporcional"] > 0.0
    assert resultado["desconto_inss"] >= 0.0
    assert resultado["desconto_irpf"] >= 0.0