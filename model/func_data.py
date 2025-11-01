import requests
import pandas as pd
from io import StringIO

'''Funções para tratamento dos dados quando se tem apenas um sensor
e uma única URL'''

def request_data(sensor: str, url: str):
    """
    Requisição dos dados a partir da URL fornecida.

    Parâmetros:
    sensor (str): Nome do sensor.
    url (str): URL para requisitar os dados.

    Retorna:
    pd.DataFrame: DataFrame contendo os dados do sensor.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
         }
    print(f"Baixando dados do sensor '{sensor}' de {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status() # Checa se houve algum erro na requisição
    if response.status_code == 200:
        conteudo = response.content.decode('utf-8')
        csv_data = StringIO(conteudo)
        df = pd.read_csv(csv_data, sep=None, quotechar='"', 
                         na_values=['', ' ', '""', 'NaN', 'nan', 'NULL', 'null', 'None'],
                         keep_default_na=True, engine='python')
        df.columns = df.columns.str.strip().str.replace('"', '') # Remove espaços em branco dos nomes das colunas
        print(f"Dados do sensor '{sensor}' baixados com sucesso.")
        return df
    else:
        print(f"Falha ao baixar dados do sensor '{sensor}' de {url}. Status: {response.status_code}")

def check_time(data_frame: pd.DataFrame, col_timestamp: str) -> pd.DataFrame:
    """
    Verifica o nome da coluna do tempo, renomeia esta coluna para 'timestamp'
    e converte para o formato datetime retornando um DataFrame.

    Parâmetros:
    data_frames (pd.DataFrame): DataFrame contendo os dados do sensor.
    col_timestamp (str): Nome da coluna de timestamps.

    Retorna:
    pd.DataFrame: DataFrame com a coluna de timestamp convertida.
    """
    df = data_frame.copy()
    if col_timestamp != 'timestamp':
        df = df.rename(columns={col_timestamp: 'timestamp'})
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df    
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df
    
def failure_intervals(df: pd.DataFrame, status1: str):
    """
    Gera as listas com os tempos de falhas e os intervalos dos tempos de falhas 
    considerando um status específico como falha.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados do sensor.
    status1 (str): Valor do status que indica uma falha.

    Retorna:
    lista com os tempos de falhas e os intervalos entre os tempos de falhas encontrados.
    """
    # Ordena o DataFrame pelo timestamp
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    # Filtra as linhas onde o status indica falha
    falhas = df[df['status_energia'] == status1]
    # Calcula o tempo inicial para referência
    tempo_inicio = df['timestamp'].min()
    # Calcula a diferença em horas desde o início até cada linha com falha  
    tempos_desde_inicio = (falhas['timestamp'] - tempo_inicio).dt.total_seconds() / 3600
    # Converte para lista os tempos desde o início
    tempos_desde_inicio_lista = tempos_desde_inicio.tolist()
    # Calcula os tempos entre as falhas
    tempos_entre_falhas = falhas['timestamp'].diff().dt.total_seconds().dropna() / 3600
    # Converte para lista os tempos entre falhas
    tempos_entre_falhas_lista = tempos_entre_falhas.tolist()

    return tempos_desde_inicio_lista, tempos_entre_falhas_lista

    
