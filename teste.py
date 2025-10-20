from model.tratamento_dados import TratamentoDados
from model.intervalos_falhas import encontrar_intervalos_falhas, encontrar_intervalos_falhas_nan
#import pandas as pd

sensor = ['temp', 'umid', 'ppf1']
urls = ['https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_temperature_20240315_0644.csv',
        'https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_humidity_20240315_0644.csv',
        'https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_ppfd_total_ch1_20240315_0642.csv']

tratamento = TratamentoDados()

# Chama a função para criar o dicionário de URLs
dict_urls = tratamento.dict_urls(sensor, urls)

# Chama a função para requisitar os dados
df = tratamento.request_data(dict_urls)

# Unifica os dados em um único DataFrame
df_final = tratamento.unify_data(df)

# Salva o DataFrame unificado em um arquivo CSV
nome_arquivo = "dados_unificados.csv"
caminho = "/home/crdamke/Documentos/Python/app/app_falhas"
tratamento.salvar_csv(df_final, nome_arquivo, caminho)

# Gera o relatório estatístico dos dados
relatorio = tratamento.relatorio_estatistico(df_final)

# Gera as listas com os tempos de falhase os intervalos dos tempos de falhas 
# maiores que 10 segundos
lista = encontrar_intervalos_falhas(df_final, sensor_col='temp', timestamp_col='timestamp', limiar_tempo=10)

# Gera as listas com os tempos de falhas e os intervalos dos tempos de falhas 
# considerando valores NaN como falhas para o sensor 'temp'
lista_nan = encontrar_intervalos_falhas_nan(df_final, sensor_col='temp', timestamp_col='timestamp')



