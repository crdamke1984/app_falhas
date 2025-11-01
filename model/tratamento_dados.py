# import pandas as pd
# import requests
# from io import StringIO
'''
Funções para tratamento dos dados quando se tem múltiplos sensores
e múltiplas URLs'''

    
# '''
# Dicionarios de sensores e urls em um único dicionário
# '''
# def dict_urls(sensor: list, url: list):
#     # Verifica se as listas têm o mesmo tamanho
#     if len(sensor) != len(url):
#         raise ValueError("As listas 'sensor' e 'url' devem ter o mesmo tamanho.")
#     else:
#         files_url = {}
#         for i in range(len(sensor)):
#             files_url[sensor[i]] = url[i]
#         return files_url

# '''
# Requisição dos dados a partir do dicionário de urls
# '''
# def request_data(dict_urls:dict):
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#          }
#     text = {}
#     for key, url in dict_urls.items():
#         print(f"Baixando dados de '{key}' de {url}")
#         response = requests.get(url, headers=headers, timeout=30)
#         response.raise_for_status() # Checa se houve algum erro na requisição
#         if response.status_code == 200:
#             conteudo = response.content.decode('utf-8')
#             text[key] = conteudo
#             print(f"Dados de '{key}' baixados com sucesso.")
        
#         else:
#             print(f"Falha ao baixar dados de '{key}' de {url}. Status: {response.status_code}")
#     return text

# '''
# Converte o conteúdo dos dados em DataFrames e armazena em um dicionário
# '''
# def convert_to_dataframes(text: dict):
#     data_frames = {}
#     for key, conteudo in text.items():
#         csv_data = StringIO(conteudo)
#         df = pd.read_csv(csv_data, sep=None, quotechar='"', 
#                          na_values=['', ' ', '""', 'NaN', 'nan', 'NULL', 'null', 'None'],
#                          keep_default_na=True, engine='python')
#         df.columns = df.columns.str.strip().str.replace('"', '') # Remove espaços em branco dos nomes das colunas
#         data_frames[key] = df
#     return data_frames

# '''
# Verifica que tipo de dado está em uma coluna específica
# '''
# def check_column_dtype(data_frames: dict, column_name: str):
#     for key, df in data_frames.items():
#         if column_name in df.columns:
#             dtype = df[column_name].dtype
#             type_col = pd.api.types.is_string_dtype(dtype)
#             return type_col
#         elif column_name in df.columns:
#             dtype = df[column_name].dtype
#             type_col = pd.api.types.is_numeric_dtype(dtype)
#             return type_col
#         else:
#             raise ValueError(f"Coluna '{column_name}' não encontrada no DataFrame.")

# '''
# Verifica o nome da coluna do tempo, renomeia esta coluna para 'timestamp'
# e converte para o formato datetime retornando um dicionário de DataFrames
# '''
# def check_time(text: dict, col_timestamp: str):
#     data_frames = {}
#     for key, df in text.items():
#         if col_timestamp != 'timestamp':
#             df = df.rename(columns={col_timestamp: 'timestamp'})
#             df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
#             data_frames[key] = df
#         else:
#             df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
#             data_frames[key] = df
#     return data_frames

# def request_data(dict_urls: dict):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
#     data_frames = {}
#     for key, url in dict_urls.items():
#         print(f"Downloading data for {key} from {url}")
#         response = requests.get(url, headers=headers, timeout=30)
#         response.raise_for_status() # Checa se houve algum erro na requisição
#         if response.status_code == 200:
#             text = response.content.decode('utf-8')
#             csv_data = StringIO(text)
#             df = pd.read_csv(csv_data, sep=';', quotechar='"', na_values=['', ' ', '""', 'NaN', 'nan', 'NULL', 'null', 'None'] ,keep_default_na=True)
#             df.columns = df.columns.str.strip().str.replace('"', '') # Remove espaços em branco dos nomes das colunas
#             if ('Received At' in df.columns) and ('Numeric Value' in df.columns):
#                 df = df.rename(columns={"Received At": "timestamp",
#                                         "Numeric Value": "valor"
#                                         })
#                 df['sensor'] = key
#                 df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
#                 df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
#                 data_frames[key] = df
#                 print(f"Data for {key} downloaded successfully with {len(df)} records.")
#             else:
#                 print(f"Received at or Numeric Value columns missing in data for {key}")
#         else:
#             print(f"Failed to download data for {key}. Status code: {response.status_code}")
#     return data_frames
    
# '''
# Unificação dos dados em um único DataFrame contendo o timestamp 
# e os valores de todos os sensores
# '''
# def unify_data(data_frames: dict):
#     df_final = None
#     for key, df in data_frames.items():
#         if df_final is None:
#             df_final = df[['timestamp', 'valor']].rename(columns={'valor': key})
#         else:
#             df_final = pd.merge(df_final, df[['timestamp', 'valor']].rename(columns={'valor': key}), on='timestamp', how='outer')
#     df_final = df_final.sort_values('timestamp').reset_index(drop=True)
#     return df_final
    
# '''
# Relatório Estatístico dos dados
# '''
# def relatorio_estatistico(df: pd.DataFrame):
#     numero_linhas = len(df)

#     if 'timestamp' in df.columns:
#         primeiro_timestamp = df['timestamp'].min()
#         ultimo_timestamp = df['timestamp'].max()
#         minimos = {
#             sensor: df.loc[df[sensor].idxmin(), ["timestamp", sensor]].to_dict()
#             for sensor in df.columns if sensor != "timestamp"
#         }
#         maximos = {
#             sensor: df.loc[df[sensor].idxmax(), ["timestamp", sensor]].to_dict()
#             for sensor in df.columns if sensor != "timestamp"
#         }
#         valores_ausentes_coluna = df.isna().sum()
#         total_valores_ausentes = df.isna().sum().sum()
#         relatorio_estatistico = {
#             "Número total de linhas": numero_linhas,
#             "Primeiro timestamp": primeiro_timestamp,
#             "Último timestamp": ultimo_timestamp,
#             "Valores mínimos por sensor": minimos,
#             "Valores máximos por sensor": maximos,
#             "Valores ausentes por coluna": valores_ausentes_coluna.to_dict(),
#             "Total de valores ausentes": total_valores_ausentes
#         }
            
#     else:
#         relatorio_estatistico = {
#             "Número total de linhas": numero_linhas,
#             "Erro": "Coluna 'timestamp' não encontrada no DataFrame"
#         }
#     return relatorio_estatistico
    
# '''
# Função para salvar o DataFrame em um arquivo CSV
# '''
# def salvar_csv(df: pd.DataFrame, nome_arquivo: str, caminho: str):
#     caminho_completo = f"{caminho}/{nome_arquivo}"
#     df.to_csv(caminho_completo, index=False)
#     print(f"DataFrame salvo em {caminho_completo}")
        