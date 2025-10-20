import pandas as pd

def encontrar_intervalos_falhas(df: pd.DataFrame, sensor_col: str, timestamp_col: str, limiar_tempo: int) -> list:
    """
    Encontra intervalos de falhas nos dados do sensor.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados do sensor.
    sensor_col (str): Nome da coluna do sensor.
    timestamp_col (str): Nome da coluna de timestamps.
    limiar_tempo (int): Limiar de tempo em segundos para considerar uma falha.

    Retorna:
    lista com os tempos de falhas e os intervalos entre os tempos de falhas encontrados.
    """
    # Converter a coluna 'timestamp' para datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')

    # Ordena o DataFrame pelo timestamp
    df = df.sort_values(by=timestamp_col).reset_index(drop=True)

    # Calcula a diferença de tempo entre timestamps consecutivos
    df['delta'] = df[timestamp_col].diff().dt.total_seconds().fillna(0)

    # Identifica os pontos onde a diferença excede o limiar
    falhas = df[df['delta'] > limiar_tempo]

    # Calcula o tempo inicial para referência
    tempo_inicio = df[timestamp_col].min()

    # Calcula a diferença em horas desde o início até cada linha com falha  
    tempos_desde_inicio = (falhas[timestamp_col] - tempo_inicio).dt.total_seconds() / 3600

    # Converte para lista os tempos desde o início
    tempos_desde_inicio_lista = tempos_desde_inicio.tolist()

    # Calcula os tempos entre as falhas
    tempos_entre_falhas = falhas[timestamp_col].diff().dt.total_seconds().dropna() / 3600

    # Converte para lista os tempos entre falhas
    tempos_entre_falhas_lista = tempos_entre_falhas.tolist()

    return tempos_desde_inicio_lista, tempos_entre_falhas_lista

def encontrar_intervalos_falhas_nan(df: pd.DataFrame, sensor_col: str, timestamp_col: str) -> list:
    """
    Encontra intervalos de falhas nos dados do sensor considerando valores NaN como falhas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados do sensor.
    sensor_col (str): Nome da coluna do sensor.
    timestamp_col (str): Nome da coluna de timestamps.

    Retorna:
    lista com os tempos de falhas e os intervalos entre os tempos de falhas encontrados.
    """
    # Converter a coluna 'timestamp' para datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')

    # Ordena o DataFrame pelo timestamp
    df = df.sort_values(by=timestamp_col).reset_index(drop=True)

    # Marca os valores NaN como falhas
    df['is_nan'] = df[sensor_col].isna().astype(int)

    # Filtra apenas as linhas onde há falhas (NaN)
    falhas = df[df['is_nan'] == 1]

    # Calcula o tempo inicial para referência
    tempo_inicio = df[timestamp_col].min()

    # Calcula a diferença em horas desde o início até cada linha com falha  
    tempos_desde_inicio = (falhas[timestamp_col] - tempo_inicio).dt.total_seconds() / 3600

    # Converte para lista os tempos desde o início
    tempos_desde_inicio_lista = tempos_desde_inicio.tolist()

    # Calcula os tempos entre as falhas
    tempos_entre_falhas = falhas[timestamp_col].diff().dt.total_seconds().dropna() / 3600

    # Converte para lista os tempos entre falhas
    tempos_entre_falhas_lista = tempos_entre_falhas.tolist()

    return tempos_desde_inicio_lista, tempos_entre_falhas_lista

