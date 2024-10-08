import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from curves_plot import gerar_curvas
from single_diode_model import SingleDiodeModel
from table_data import obter_dados_data_hora
import matplotlib.pyplot as plt

# Função para desenhar o gráfico no canvas
def draw_figure(canvas, figure):
    for widget in canvas.winfo_children():
        widget.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Função para visualizar dados de irradiância e temperatura
def plot_hourly_data(selected_hour, selected_minute, canvas):
    data_selecionada = "11/01/2019"
    dados_hora = obter_dados_data_hora(data_selecionada, f"{selected_hour}:{selected_minute:02d}")

    if dados_hora is not None:
        temperatura_atual = dados_hora['Temp_Cel']
        irradiancia_atual = dados_hora['Radiação']

        # Plotando dados de radiação e temperatura
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        # Gráfico de Radiação
        axs[0].plot([selected_hour], [irradiancia_atual], 'bo-', label='Radiação')
        axs[0].scatter(selected_hour, irradiancia_atual, color='red')
        axs[0].annotate(f"{irradiancia_atual:.2f} W/m²", xy=(selected_hour, irradiancia_atual), 
                        xytext=(5, 5), textcoords='offset points', fontsize=10, color='red')
        axs[0].set_title('Radiação')
        axs[0].set_xlabel('Hora')
        axs[0].set_ylabel('Radiação (W/m²)')

        # Gráfico de Temperatura
        axs[1].plot([selected_hour], [temperatura_atual], 'bo-', label='Temperatura')
        axs[1].scatter(selected_hour, temperatura_atual, color='red')
        axs[1].annotate(f"{temperatura_atual:.2f} °C", xy=(selected_hour, temperatura_atual), 
                        xytext=(5, 5), textcoords='offset points', fontsize=10, color='red')
        axs[1].set_title('Temperatura')
        axs[1].set_xlabel('Hora')
        axs[1].set_ylabel('Temperatura (°C)')

        plt.tight_layout()
        draw_figure(canvas, fig)
        plt.close(fig)
    else:
        sg.popup('Dados não encontrados para a hora selecionada.')

# Função para realizar a simulação das curvas
def calculate_solar_parameters(data_hora, irradiancia_global, beta, gamma_p, lat, long_local, long_meridiano):
    # Usaremos sua função `calcular_angulos_irradiancia` para obter os parâmetros solares
    from table_data import calcular_angulos_irradiancia
    return calcular_angulos_irradiancia(data_hora, irradiancia_global, beta, gamma_p, lat, long_local, long_meridiano)

# Função para gerar as curvas de tensão, corrente e potência
def calcular_resultados(canvas, selected_hour, selected_minute):
    data_selecionada = "11/01/2019"
    dados_hora = obter_dados_data_hora(data_selecionada, f"{selected_hour}:{selected_minute:02d}")

    if dados_hora is not None:
        # Criar o modelo de diodo simples com base nos seus cálculos
        short_circuit_current = 18.52  # [A]
        open_circuit_voltage = 41.5  # [V]
        series_resistance = 0.167  # Estimado (panel series resistance)
        shunt_resistance = 9.619  # Estimado (panel parallel (shunt) resistance)
        diode_quality_factor = 0.85  # Estimado

        # Parâmetros para o modelo
        number_of_series_connected_cells = 60
        operating_temperature = dados_hora['Temp_Cel'] + 273  # Kelvin
        actual_irradiance = dados_hora['Radiação']

        single_diode_model = SingleDiodeModel(
            short_circuit_current,
            open_circuit_voltage,
            number_of_series_connected_cells,
            temperature_current_coefficient=0.05 / 100 * short_circuit_current,
            series_resistance=series_resistance,
            shunt_resistance=shunt_resistance,
            diode_quality_factor=diode_quality_factor
        )

        # Simular curvas
        single_diode_model.calculate(operating_temperature, actual_irradiance)

        # Chama a função que gera as curvas (usa seus valores)
        gerar_curvas(single_diode_model)

        sg.popup('Simulação concluída! Curvas geradas.')
    else:
        sg.popup('Dados não encontrados para a hora selecionada.')

# Função principal para a interface PySimpleGUI
def main_menu():
    layout = [
        [sg.Text('Simulação Fotovoltaica', font=('Helvetica', 16), justification='center')],
        [sg.Push(), sg.Button('Visualizar Dados de Irradiância e Temperatura', size=(30, 2)), sg.Push()],
        [sg.Push(), sg.Button('Simular Curvas I-V e P-V', size=(30, 2)), sg.Push()],
        [sg.Push(), sg.Button('Sair', size=(30, 2)), sg.Push()]
    ]

    window = sg.Window('Menu Principal', layout, size=(400, 300))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break
        elif event == 'Visualizar Dados de Irradiância e Temperatura':
            hour_selection(window)
        elif event == 'Simular Curvas I-V e P-V':
            simulate_curves_interface(window)

    window.close()

# Interface para a seleção de hora e minuto
def hour_selection(parent_window):
    layout = [
        [sg.Text('Selecione a Hora:', justification='center'),
         sg.Slider(range=(0, 23), default_value=0, orientation='h', key='-HOUR-', size=(40, 20))],
        [sg.Text('Selecione o Minuto:', justification='center'),
         sg.Slider(range=(0, 59), default_value=0, orientation='h', key='-MINUTE-', size=(40, 20))],
        [sg.Button('Voltar')],
        [sg.Canvas(key='-CANVAS-', size=(800, 600))]
    ]

    window = sg.Window('Dados de Irradiância e Temperatura', layout, size=(850, 700), finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Voltar'):
            window.close()
            parent_window.un_hide()
            break

        selected_hour = int(values['-HOUR-'])
        selected_minute = int(values['-MINUTE-'])
        plot_hourly_data(selected_hour, selected_minute, window['-CANVAS-'].TKCanvas)

# Interface para simulação das curvas
def simulate_curves_interface(parent_window):
    layout = [
        [sg.Text('Selecione a Hora:', justification='center'),
         sg.Slider(range=(0, 23), default_value=12, orientation='h', key='-HOUR-', size=(40, 20))],
        [sg.Text('Selecione o Minuto:', justification='center'),
         sg.Slider(range=(0, 59), default_value=0, orientation='h', key='-MINUTE-', size=(40, 20))],
        [sg.Button('Simular'), sg.Button('Voltar')],
        [sg.Canvas(key='-CANVAS-', size=(800, 600))]
    ]

    window = sg.Window('Simulação de Curvas I-V e P-V', layout, size=(850, 700), finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Voltar'):
            window.close()
            parent_window.un_hide()
            break

        selected_hour = int(values['-HOUR-'])
        selected_minute = int(values['-MINUTE-'])
        calcular_resultados(window['-CANVAS-'].TKCanvas, selected_hour, selected_minute)

# Iniciar a interface
main_menu()
