import numpy as np
import matplotlib.pyplot as plt

def gerar_curvas(single_diode_model):
    # Definindo variáveis
    f = 60  # Frequência da rede
    w = 2 * np.pi * f
    t = np.linspace(0, 2 * (1 / f), 200)

    potRede = 220 * 17.25 # Corrende máxima do painel
    Vp = 220 * np.sqrt(2)
    Ip = (potRede*2) / Vp

    # Tensão e corrente (usando valores de pico)
    vt = Vp * np.cos(w * t)  # Tensão como função do tempo
    ph = np.radians(180)  # Fase de 180 graus
    it = Ip * np.cos(w * t + ph)  # Corrente como função do tempo

    # Potências
    pt = vt * it  # Potência total

    pt_max = np.max(pt)
    pt_media = np.mean(pt)
    pt_min = np.min(pt)
    
    print("Potência total máxima:", pt_max)
    print("Potência total mínima:", pt_min)
    print("Potência total (media):", pt_media)

    # Potência ativa e reativa
    pa = Vp * Ip / 2 * np.cos(2 * w * t) * np.cos(ph) + Vp * Ip / 2 * np.cos(ph)
    pr = -Vp * Ip / 2 * np.sin(2 * w * t) * np.sin(ph)
    
    print("--------------------------")
    print("Média da potência reativa:", np.mean(pr))

    # Figura 1: Tensões, correntes e potências
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Subplot 1: Tensões e correntes
    ax1.plot(t * 1e3, vt, 'blue', label='Tensão [V]')
    ax1.set_xlabel('tempo [ms]')
    ax1.set_ylabel('Tensão [V]', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)

    # Criar um segundo eixo y para a corrente (eixo da direita)
    ax1_corrente = ax1.twinx()
    ax1_corrente.plot(t * 1e3, it, 'orange', label='Corrente [A]')
    ax1_corrente.set_ylabel('Corrente [A]', color='orange')
    ax1_corrente.tick_params(axis='y', labelcolor='orange')

    # Adicionar as legendas para ambos os eixos
    ax1.legend(loc='upper left')
    ax1_corrente.legend(loc='upper right')

    # Subplot 2: Potências
    ax2.plot(t * 1e3, pa + pr, 'y', label='pa+pr (pt)')
    ax2.plot(t * 1e3, pt, 'k', label='Pt')
    ax2.plot(t * 1e3, pa, 'b', label='P_at')
    ax2.plot(t * 1e3, pr, 'r', label='P_re')
    ax2.grid(True)
    ax2.set_xlabel('tempo [ms]')
    ax2.set_ylabel('Potência total, ativa e reativa')
    ax2.legend()

    plt.tight_layout()
    ###############################  plt.show()

    #------------------------------------------------------------------------------------------------------------------------
    # Parte 2
    #------------------------------------------------------------------------------------------------------------------------

    # Cálculo da tensão e corrente para fontes em paralelo
    L = 1e-3  # Indutância 10e-3
    VL = -np.max(it) * (w * L) * np.sin(w * t)
    Vfv = vt + VL  # Tensão fotovoltaica

    # Cálculo da potência fotovoltaica
    pfv = Vfv * (-it)  # Potência fotovoltaica

    # Potência fotovoltaica
    pfv_max = np.max(pfv)
    pfv_min = np.min(pfv)
    pfv_media = np.mean(pfv)

    print("--------------------------")
    print("Potência fotovoltaica máxima:", pfv_max)
    print("Potência fotovoltaica mínima:", pfv_min)
    print("Média da potência fotovoltaica:", pfv_media)
    print("--------------------------")

    # Figura 2: Potência fotovoltaica e corrente
    fig2, (ax5, ax6) = plt.subplots(1, 2, figsize=(16, 8))

    # Subplot 1: Tensão e corrente fotovoltaica
    ax5.plot(t * 1e3, Vfv, 'b', label='Vfv [V]')
    ax5.set_xlabel('tempo [ms]')
    ax5.set_ylabel('Tensão [V]', color='b')
    ax5.tick_params(axis='y', labelcolor='b')
    ax5.grid(True)

    # Criar um segundo eixo y para a corrente (eixo da direita)
    ax5_corrente = ax5.twinx()
    ax5_corrente.plot(t * 1e3, -it, 'orange', label='Corrente [A]')
    ax5_corrente.set_ylabel('Corrente [A]', color='orange')
    ax5_corrente.tick_params(axis='y', labelcolor='orange')

    # Adicionar as legendas para ambos os eixos
    ax5.legend(loc='upper left')
    ax5_corrente.legend(loc='upper right')

    # Subplot 2: Potência fotovoltaica
    ax6.plot(t * 1e3, pfv, 'k', label='Pfv')
    ax6.grid(True)
    ax6.set_xlabel('tempo [ms]')
    ax6.set_ylabel('Potência fotovoltaica [W]')
    ax6.legend()

    plt.tight_layout()
    plt.show()

    amplitude_tensao_fotovoltaico = np.max(np.abs(Vfv))
    amplitude_corrente_fotovoltaico = np.max(np.abs(-it))
    
    print("--------------------------")
    print("Amplitude máxima da tensão fotovoltaica:", amplitude_tensao_fotovoltaico)
    print("Amplitude máxima da corrente fotovoltaica:", amplitude_corrente_fotovoltaico)
    print("--------------------------")
