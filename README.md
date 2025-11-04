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

## Modelo Matemático  
O aplicativo utiliza-se do método da Máxima Verossimilhança para obter os parâmetros da Função de Densidade de Probabilidade (FDP) Gama. Com esses parâmetros torna-se possível modelar a FDP Gama e, consequentemente, calcular as probabilidades de falhas dado um cenário de tempo. 

Em termos matemáticos, temos que a FDP Gama (1), nos parâmetros $\alpha$ (forma) e $\beta$ (escala), é definida como: 
$$ 
\begin{equation}
   f(x, \alpha, \beta) = \frac{\beta^{\alpha}x^{\alpha -1}e^{\beta x}}{\Gamma(\alpha)}
\end{equation} 
$$
onde $\Gamma(\alpha)$ é a função Gama completa dada por: 
$$
\begin{equation}
    \Gamma(\alpha) = \int_{0}^{\infty} x^{\alpha -1}e^{-\alpha} dx
\end{equation}
$$

Sabe-se que a Função de Densidade Acumulada (FDA) de uma FDP (que é a primitiva da FDP)  calcula a probabilidade de um evento ocorrer antes de um valor pré estabelecido. Dentro do contexto abordado, a probabilidade de uma falha ocorrer até um certo tempo fornecido $t$, pode ser expressa por: 
$$ 
\begin{equation}
F(t,\alpha,\beta) = P(T \leq t) = \int_{0}^{t} f(x,\alpha,\beta) dx
\end{equation}
$$
onde $f(x,\alpha,\beta)$ é a FDP Gama (1). Em outras palavras, se os parâmetros $\alpha$ e $\beta$ são conhecidos, então é possível obter a probabilidade de que ocorra uma falha até um tempo dado. 

Sendo assim, escolhe-se o método da Máxima Verossimilhança para descobrir os parâmetros $\alpha$ e $\beta$. Tal método resume-se em resolver a seguinte Equação Diferencial Parcial (EDP):
$$
\begin{equation}
\left\{
    \begin{array}{l}
        \frac{\partial \Lambda}{\partial \alpha}  = 0\\
        \frac{\partial \Lambda}{\partial \beta} = 0 
    \end{array}
\right.
\end{equation}
$$
onde 
$$
\begin{equation}
    \Lambda(\alpha,\beta) = \ln(L(\alpha,\beta))
\end{equation}
$$
é denotada por Log-Verossimilhança e 
$$
\begin{equation}
    L(\alpha,\beta) = \frac{\beta^{\alpha \cdot n_f}}{\Gamma(\alpha)}\prod_{i=1}^{n_f}t_{i}^{\alpha -1}e^{-\alpha t_i}
\end{equation}
$$
com $n_f$ sendo o número de falhas é conhecida como Função de Verossimilhança da FDP Gama (1). 

Para resolver a EDP (4) e estimar os parâmetros $\alpha$ e $\beta$, utilizam-se métodos numéricos. Com o comando **gamma.fit()** da biblioteca *scipy* no Python, é possível obter os parâmetros e ele é utilizado neste projeto.

Logo, conhecidos os parâmetros da FDP Gama (1) e substituindo-os na equação (3), pode-se obter a probabilidade de uma falha ocorrer até um certo tempo dado. Este cálculo é feito utilizando o comando **gamma.cdf()** da biblioteca acima citada. 
