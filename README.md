# Projeto - Tolerância a Falhas 
Projeto desenvolvido para 
- obter um arquivo no formato .csv com os dados de um sensor de energia localizado em um servidor ([link](http://crdamke.cloud/extrator));
- converter esse arquivo em DataFrame via pandas;
- padronizar os tempos de leitura do sensor;
- coletar os tempos até a falha de energia, assim como os intervalos entre essas falhas, levando em consideração o status do sensor como 'SEM_ENERGIA'; 
- calcular, através da função de densidade de probabilidade gama e dos intervalos de falhas, a probabilidade de uma falha ocorrer e as probabilidades de falha simulando cenários de tempos.

## Pacotes/Módulos Requeridos
- pandas; 
- io;
- requests;
- scipy

## Uso
Em desenvolvimento