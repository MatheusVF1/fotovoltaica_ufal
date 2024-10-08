from photovoltaic_modeling.parameter.parameter_extraction import ParameterExtraction

# Dados do painel HiKu7 Mono PERC 605 W do datasheet
short_circuit_current = 18.52  # [A] Isc
open_circuit_voltage = 41.5  # [V] Voc
maximum_power_point_current = 17.25  # [A] Impp
maximum_power_point_voltage = 35.1  # [V] Vmpp
number_of_cells_in_series = 60  # Número de células em série

# Criando o objeto de extração de parâmetros
parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
                                           maximum_power_point_current, maximum_power_point_voltage, 
                                           number_of_cells_in_series = number_of_cells_in_series)

# Estimativas iniciais para Rs, Rsh e A
series_resistance_estimate = 1
shunt_resistance_estimate = 1000
diode_quality_factor_estimate = 1

# Lista com as estimativas iniciais
parameter_estimates = [series_resistance_estimate, shunt_resistance_estimate, diode_quality_factor_estimate]

# Calculando os parâmetros ideais baseados nos dados
parameter_extraction.calculate(parameter_estimates)

# Exibindo os valores obtidos
print('series_resistance=', parameter_extraction.series_resistance)
print('shunt_resistance=', parameter_extraction.shunt_resistance)
print('diode_quality_factor=', parameter_extraction.diode_quality_factor)