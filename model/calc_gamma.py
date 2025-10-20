from scipy.stats import gamma
import numpy as np
import pandas as pd

def probabilidade_de_falha(intervalo_horas: list, tempo_ate_falha: float):
    """
    Calcula a probabilidade de falha em um intervalo de horas usando a distribuição Gama.

    Parâmetros:
    intervalo_horas (list): Lista de intervalos de horas.

    Retorna:
    list: Probabilidades de falha correspondentes aos intervalos fornecidos.
    """
    # Estima os parâmetros da distribuição Gama a partir dos dados fornecidos
    shape, loc, scale = gamma.fit(intervalo_horas, floc=0)

    # Calcula a probabilidade acumulada para cada intervalo de horas
    probabilidades = gamma.cdf(tempo_ate_falha, a=shape, scale=scale)

    return probabilidades

def probabilidade_cenarios(intervalo_horas: list, tempos_ate_falha: list):
    """
    Calcula a probabilidade de falha para múltiplos cenários usando a distribuição Gama.

    Parâmetros:
    intervalo_horas (list): Lista de intervalos de horas.
    tempos_ate_falha (list): Lista de tempos até falha para os quais calcular a probabilidade.

    Retorna:
    list: Lista de probabilidades de falha para cada tempo até falha fornecido.
    """
    # Estima os parâmetros da distribuição Gama a partir dos dados fornecidos
    shape, loc, scale = gamma.fit(intervalo_horas, floc=0)

    probabilidades = []
    for tempo in tempos_ate_falha:
        prob = gamma.cdf(tempo, a=shape, scale=scale)
        probabilidades.append(prob)

    acoes = []
    for p in probabilidades:
        if p < 0.5:
            acoes.append("Sem ação")
        elif 0.5 <= p < 0.8:
            acoes.append("Monitorar de perto")
        elif 0.8 <= p < 0.9:
            acoes.append("Preparar plano de contingência")
        else:
            acoes.append("Ação Urgente")

    # Criar DataFrame para exibir os cenários
    df_cenarios = pd.DataFrame({
        "Horas desde última ação": tempos_ate_falha,
        "Probabilidade de falha (%)": np.round(np.array(probabilidades)*100, 2),
        "Ação recomendada": acoes
        })
    return shape, scale, probabilidades, df_cenarios