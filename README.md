Projeto de Análise de Fatalidades de Bombeiros 

Este projeto é um dashboard web interativo para a análise de dados públicos sobre fatalidades de bombeiros.


Ferramentas e Bibliotecas Utilizadas

Linguagens e Plataformas

Linguagem de Tratamento : R

Linguagem do Dashboard : Python

Framework do Dashboard: Streamlit

Base de Dados: SQLite

Bibliotecas R (usadas no arquivo tratamento.R)

tidyverse: Para manipulação de dados (dplyr, readr) e visualização (ggplot2).

here: Para gestão de caminhos de ficheiros (paths).

lubridate: Para manipulação e extração de datas.

RSQLite: Para criar e escrever no banco de dados SQLite.

Bibliotecas Python (usadas no arquivo dash.py e dependências)

streamlit: Para a criação da interface web e do dashboard.

pandas: Para leitura de dados do SQLite e manipulação (filtros).

altair: Para a criação dos gráficos interativos.

Kaggle: Extração do dataset.

Como Executar o Projeto (Ambiente Ubuntu)

Este projeto foi construído para ser executado localmente. O repositório já inclui o banco de dados final (dados/bombeiros.db), então pode saltar os passos 1 e 2 se quiser apenas visualizar o dashboard.

1. (Opcional) Dependências do Tratamento em R e Criação do banco de dados

Este passo usa o script tratamento.R para descarregar os dados originais do Kaggle e realizar a limpeza.

Requer um ambiente R com as bibliotecas listadas acima instaladas. 

Requer credenciais Kaggle (kaggle.json) configuradas.


3. Instalar as Bibliotecas Python (para o Dashboard)

Certifique-se de que tem o Python 3.8+ e o pip instalados no seu sistema.

sudo apt update
sudo apt install python3-pip


Instale as bibliotecas Python necessárias para executar o dash.py:

# Instala as bibliotecas para o dashboard
# (Usar --break-system-packages apenas não funcione sem ele)
pip install --break-system-packages streamlit pandas altair


4. Executar o Dashboard

Na pasta principal do projeto (onde o dash.py está localizado), execute o seguinte comando no seu terminal:

streamlit run dash.py


O seu navegador abrirá automaticamente no endereço http://localhost:8501.

Estrutura do Repositório

tratamento.R: O script R que faz o download, limpeza e tratamento dos dados e gera o banco de dados.

dash.py: O código-fonte principal da aplicação web Streamlit.

dados/bombeiros.db: O banco de dados SQLite que armazena os dados tratados.

Documento de Requisitos.pdf: O documento de cumprimento de requisitos.