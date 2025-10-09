import pandas as pd
import requests
from io import StringIO

'''
Classe para tratamento dos dados para tolerância a falhas
'''
class TratamentoDados:
    def __init__(self):
        pass

    '''
    Dicionarios de sensores e urls em um único dicionário
    '''
    def dict_urls(self, sensor: list, url: list):
        files_url = {}
        for i in range(len(sensor)):
            files_url[sensor[i]] = url[i]
        return files_url

    '''
    Requisição dos dados a partir do dicionário de urls
    '''
    def request_data(self, dict_urls: dict):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        data_frames = {}
        for key, url in dict_urls.items():
            print(f"Downloading data for {key} from {url}")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status() # Checa se houve algum erro na requisição
            if response.status_code == 200:
                text = response.content.decode('utf-8')
                csv_data = StringIO(text)
                df = pd.read_csv(csv_data, sep=';', quotechar='"', na_values=['', ' ', '""', 'NaN', 'nan', 'NULL', 'null', 'None'] ,keep_default_na=True)
                df.columns = df.columns.str.strip().str.replace('"', '') # Remove espaços em branco dos nomes das colunas
                if ('Received At' in df.columns) and ('Numeric Value' in df.columns):
                    df = df.rename(columns={"Received At": "timestamp",
                                        "Numeric Value": "valor"
                                        })
                    df['sensor'] = key
                    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
                    data_frames[key] = df
                    print(f"Data for {key} downloaded successfully with {len(df)} records.")
                else:
                    print(f"Received at or Numeric Value columns missing in data for {key}")
            else:
                print(f"Failed to download data for {key}. Status code: {response.status_code}")
        return data_frames
    
    '''
    Unificação dos dados em um único DataFrame contendo o timestamp 
    e os valores de todos os sensores
    '''
    def unify_data(self, data_frames: dict):
        df_final = None
        for key, df in data_frames.items():
            if df_final is None:
                df_final = df[['timestamp', 'valor']].rename(columns={'valor': key})
            else:
                df_final = pd.merge(df_final, df[['timestamp', 'valor']].rename(columns={'valor': key}), on='timestamp', how='outer')
        df_final = df_final.sort_values('timestamp').reset_index(drop=True)
        return df_final
    
    '''
    Relatório Estatístico dos dados
    '''
    def relatorio_estatistico(self, df: pd.DataFrame):
        numero_linhas = len(df)

        if 'timestamp' in df.columns:
            primeiro_timestamp = df['timestamp'].min()
            ultimo_timestamp = df['timestamp'].max()
            minimos = {
                sensor: df.loc[df[sensor].idxmin(), ["timestamp", sensor]].to_dict()
                for sensor in df.columns if sensor != "timestamp"
            }
            maximos = {
                sensor: df.loc[df[sensor].idxmax(), ["timestamp", sensor]].to_dict()
                for sensor in df.columns if sensor != "timestamp"
            }
            valores_ausentes_coluna = df.isna().sum()
            total_valores_ausentes = df.isna().sum().sum()
            relatorio_estatistico = {
                "Número total de linhas": numero_linhas,
                "Primeiro timestamp": primeiro_timestamp,
                "Último timestamp": ultimo_timestamp,
                "Valores mínimos por sensor": minimos,
                "Valores máximos por sensor": maximos,
                "Valores ausentes por coluna": valores_ausentes_coluna.to_dict(),
                "Total de valores ausentes": total_valores_ausentes
            }
            
        else:
            relatorio_estatistico = {
                "Número total de linhas": numero_linhas,
                "Erro": "Coluna 'timestamp' não encontrada no DataFrame"
            }
        return relatorio_estatistico
    
    '''
    Função para salvar o DataFrame em um arquivo CSV
    '''
    def salvar_csv(self, df: pd.DataFrame, nome_arquivo: str, caminho: str):
        caminho_completo = f"{caminho}/{nome_arquivo}"
        df.to_csv(caminho_completo, index=False)
        print(f"DataFrame salvo em {caminho_completo}")
        