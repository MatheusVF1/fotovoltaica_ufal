from multiple_modules_single_diode_model import MultipleModulesSingleDiodeModel
import report_helper as report_helper

# Dados do módulo solar HiKu7 Mono PERC 605 W
short_circuit_current = 18.52  # [A]
open_circuit_voltage = 41.5  # [V]
temperature_current_coefficient = 0.05 / 100 * short_circuit_current  # ([%/ºC] / [100%]) * [A/ºC]
temperature_voltage_coefficient = -0.26 / 100 * open_circuit_voltage # Conversão de [%/°C] para [V/°C]
series_resistance = 0.221  # Estimado (panel series resistance)
shunt_resistance = 415.405  # Estimado (panel parallel (shunt) resistance)
diode_quality_factor = 1.3  # Estimado

number_of_cells_in_series = 60  # 60 células em série por string
number_of_modules_in_series = 2  # Dois módulos conectados em série
number_of_voltage_decimal_digits = 1

# Criando o modelo com múltiplos módulos
multiple_modules_model = MultipleModulesSingleDiodeModel(
    short_circuit_current,
    open_circuit_voltage,
    number_of_cells_in_series,
    number_of_voltage_decimal_digits=number_of_voltage_decimal_digits,
    temperature_voltage_coefficient=temperature_voltage_coefficient,
    temperature_current_coefficient=temperature_current_coefficient,
    series_resistance=series_resistance,
    shunt_resistance=shunt_resistance,
    diode_quality_factor=diode_quality_factor,
    number_of_modules_in_series=number_of_modules_in_series
)

# Definir temperatura de operação e irradiância real
operating_temperature = 25 + 273  # Temperatura em Kelvin
actual_irradiance = 1000  # Irradiância padrão 1000 W/m²

# Simulação sem sombreamento
multiple_modules_model.calculate(operating_temperature, actual_irradiance)

# Gerar gráficos e relatório
report_helper.write_result_to_csv_file(multiple_modules_model, 'multiple_modules_single_diode_model_hiku7')
report_helper.plot_result(multiple_modules_model)
