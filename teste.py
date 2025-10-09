from model.tratamento_dados import TratamentoDados
#import pandas as pd

sensor = ['temp', 'umid', 'ppf1']
urls = ['https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_temperature_20240315_0644.csv',
        'https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_humidity_20240315_0644.csv',
        'https://www.adrianobailao.com.br/mvc_simulador/dados/base_de_dados/topico_sc5_ppfd_total_ch1_20240315_0642.csv']

tratamento = TratamentoDados()
dict_urls = tratamento.dict_urls(sensor, urls)

df = tratamento.request_data(dict_urls)

df_final = tratamento.unify_data(df)

nome_arquivo = "dados_unificados.csv"
caminho = "/home/crdamke/Documentos/Python/app/app_falhas"

tratamento.salvar_csv(df_final, nome_arquivo, caminho)


relatorio = tratamento.relatorio_estatistico(df_final)
print(relatorio)

