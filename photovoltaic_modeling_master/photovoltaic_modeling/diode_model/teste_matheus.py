from single_diode_model import SingleDiodeModel
import report_helper as report_helper

# Dados do módulo solar HiKu7 Mono PERC 605 W do datasheet
short_circuit_current = 18.52  # [A]
open_circuit_voltage = 41.5  # [V]
temperature_current_coefficient = 0.05 / 100 * short_circuit_current  # ([%/ºC] / [100%]) * [A] = [A/ºC]
series_resistance = 0.221  # Estimado (panel series resistance) 0.221
shunt_resistance = 415.405  # Estimado (panel parallel (shunt) resistance) 415.405
diode_quality_factor = 1.3  # Estimado 1.3

number_of_series_connected_cells = 60  # Número de células em série

number_of_voltage_decimal_digits = 1

# Criando o modelo de diodo simples com os dados do HiKu7
single_diode_model = SingleDiodeModel(
    short_circuit_current, 
    open_circuit_voltage, 
    number_of_series_connected_cells, 
    number_of_voltage_decimal_digits=number_of_voltage_decimal_digits,
    temperature_current_coefficient=temperature_current_coefficient, 
    series_resistance=series_resistance, 
    shunt_resistance=shunt_resistance, 
    diode_quality_factor=diode_quality_factor
)

# Temperatura de operação e irradiância real (ajustar conforme necessário)
operating_temperature = 25 + 273  # Temperatura em Kelvin
actual_irradiance = 1000  # Irradiância padrão 1000 W/m²

# Calculando os parâmetros baseados na irradiância e temperatura
single_diode_model.calculate(operating_temperature, actual_irradiance)

# Gerando relatórios e gráficos para o modelo
report_helper.write_result_to_csv_file(single_diode_model, 'single_diode_model_hiku7_605W')
report_helper.plot_result(single_diode_model)
