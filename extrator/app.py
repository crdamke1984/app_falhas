from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'dados.csv'

# Guarda o último status conhecido
ultimo_status = None

@app.route('/dados', methods=['POST'])
def receber_dados():
    global ultimo_status

    data = request.form['data']
    tensao = request.form['tensao']
    status_energia = request.form['status_energia']
    
    # Verifica se o arquivo existe para adicionar cabeçalho
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write('timestamp,tensao_volts,status_energia\n')
    
    # Só grava se o status for diferente do anterior
    if status_energia != ultimo_status:
        with open(CSV_FILE, 'a') as f:
            f.write(f'{data},{tensao},{status_energia}\n')
        
        print(f'ALTERAÇÃO DETECTADA: {data} | {tensao}V | {status_energia}')
        ultimo_status = status_energia  # Atualiza o status anterior
    else:
        print(f'Sem mudança de status ({status_energia}), nada gravado.')

    return 'Dados processados', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

