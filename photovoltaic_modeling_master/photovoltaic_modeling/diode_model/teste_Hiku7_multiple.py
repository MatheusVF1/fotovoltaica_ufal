from multiple_modules_single_diode_model import MultipleModulesSingleDiodeModel
from table_data import obter_dados_data_hora, calcular_angulos_irradiancia
from curves_plot import gerar_curvas
import report_helper as report_helper
import numpy as np

# Dados do módulo solar HiKu7 Mono PERC 605 W
short_circuit_current = 18.52  # [A]
open_circuit_voltage = 41.5  # [V]
temperature_current_coefficient = 0.05 / 100 * short_circuit_current  # ([%/ºC] / [100%]) * [A/ºC]
temperature_voltage_coefficient = -0.26 / 100 * open_circuit_voltage # Conversão de [%/°C] para [V/°C]
series_resistance = 0.167  # Estimado (resistência série do painel)
shunt_resistance = 9.619  # Estimado (resistência paralela do painel)
diode_quality_factor = 0.85  # Estimado

number_of_cells_in_series = 60  # Número de células em série por string
number_of_modules_in_series = 3  # Número de módulos conectados em série

number_of_voltage_decimal_digits = 1

# Obter dados da tabela
data_selecionada = "11/01/2019"  # Substituir por qualquer data de interesse
hora_selecionada = "12:00"  # Substituir por qualquer hora de interesse

dados_hora = obter_dados_data_hora(data_selecionada, hora_selecionada)

if dados_hora is not None:
    # Obtendo valores da planilha
    operating_temperature = dados_hora['Temp_Cel'] + 273  # Convertendo para Kelvin
    actual_irradiance = dados_hora['Radiação']  # Irradiância obtida da tabela

    print("Temperatura (ºC):", dados_hora['Temp_Cel'])
    print("Irradiância:", actual_irradiance)

    # Cálculo dos ângulos de irradiância
    angulos_irradiancia = calcular_angulos_irradiancia(
        data_hora_str="21/03/2019 12:00",
        irradiancia_global=dados_hora['Radiação'],
        beta=0,  # Inclinação do painel em relação ao plano horizontal (exemplo)
        gamma_p=0,  # Angulação do painel em relação ao norte ou sul
        lat=-9.55766947266527,  # Latitude da localização (exemplo)
        long_local=-35.78090672062049,  # Longitude da localização (exemplo)
        long_meridiano=-45  # Meridiano central do fuso horário (exemplo: UTC-3, Brasil)
    )

    # Exibir informações calculadas
    print("Ângulos e Irradiância:", angulos_irradiancia)

    # Criar o modelo de múltiplos módulos com base nos dados do HiKu7
    multiple_modules_model = MultipleModulesSingleDiodeModel(
        short_circuit_current=short_circuit_current,
        open_circuit_voltage=open_circuit_voltage,
        number_of_cells_in_series=number_of_cells_in_series,
        number_of_voltage_decimal_digits=number_of_voltage_decimal_digits,
        temperature_voltage_coefficient=temperature_voltage_coefficient,  # Usando o coeficiente correto do datasheet
        temperature_current_coefficient=temperature_current_coefficient,
        series_resistance=series_resistance,
        shunt_resistance=shunt_resistance,
        diode_quality_factor=diode_quality_factor,
        number_of_modules_in_series=number_of_modules_in_series
    )

    # Configuração de sombreamento parcial para módulos
    # Cada dicionário indica um módulo sombreado (pv_module_index) e a razão de sombreamento (partial_shading_ratio)
    # Por exemplo, módulo 1 tem 50% de sombreamento e módulo 2 tem 80% de sombreamento
    partial_shading_ratios = [
        {'pv_module_index': 1, 'partial_shading_ratio': 0.5},  # 50% de sombreamento no módulo 1
    ]

    # Calculando os parâmetros com base na irradiância e temperatura da tabela
    multiple_modules_model.calculate(operating_temperature, angulos_irradiancia['Irradiância Incidente'], partial_shading_ratios=partial_shading_ratios)

    # Gerar relatórios e gráficos para o modelo
    report_helper.write_result_to_csv_file(multiple_modules_model, 'multiple_modules_single_diode_model_hiku7')
    report_helper.plot_result(multiple_modules_model)

    # Calcular a quantidade de painéis necessários
    potencia_gerada_modulo = max(multiple_modules_model.powers)  # Potência máxima gerada pelos módulos em série
    potencia_desejada = dados_hora['Potencia_FV_Avg']  # Potência desejada obtida da tabela

    if potencia_gerada_modulo > 0:
        quantidade_paineis = potencia_desejada / potencia_gerada_modulo
        quantidade_paineis = np.ceil(quantidade_paineis)  # Arredonda para o próximo número inteiro
        print("--------------------------")
        print(f"Potência desejada: {potencia_desejada:.2f} W")
        print(f"Potência gerada por {number_of_modules_in_series} módulos em série: {potencia_gerada_modulo:.2f} W")
        print(f"Quantidade de conjuntos de {number_of_modules_in_series} módulos necessários: {int(quantidade_paineis)}")
    else:
        print("A potência gerada pelos módulos é zero ou negativa.")

    gerar_curvas(multiple_modules_model)

else:
    print("Dados não encontrados para a data e hora selecionadas.")
