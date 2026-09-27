# Pipeline de Dados com IoT e Docker 🌡️

Este projeto é uma Prova de Conceito (PoC) de Engenharia de Dados desenvolvida para a disciplina **Disruptive Architectures: IoT, Big Data e IA**. 

O objetivo é extrair dados brutos gerados por sensores IoT, processá-los utilizando Python, armazená-los em um banco de dados relacional isolado em contêiner (Docker + PostgreSQL) e, finalmente, expor métricas de negócio através de um Dashboard interativo criado com Streamlit.

# Tecnologias:

* **Linguagem:** Python 3
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** PostgreSQL
* **Virtualização:** Docker
* **Conexão com Banco:** SQLAlchemy & psycopg2-binary
* **Visualização de Dados (Dashboard):** Streamlit & Plotly
* **Versionamento:** Git e GitHub

---

# Fonte de Dados

Os dados brutos utilizados neste projeto simulam milhares de leituras térmicas de sensores IoT. A base de dados foi extraída do Kaggle:
* **Dataset:** [Temperature Readings: IoT Devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)

> **Nota:** Para executar o projeto, o arquivo CSV deve ser baixado do Kaggle, descompactado e renomeado/movido para `data/IOT-temp.csv`.

---

# Arquitetura e Modelagem de Dados (Views SQL)

O pipeline segue uma lógica simplificada de camadas. Os dados são extraídos do CSV, formatados e inseridos na tabela base `temperature_readings`. Depois, foram criadas **3 Views Analíticas** no banco de dados para agregar as informações e otimizar o consumo pelo Dashboard:

### 1. View: `avg_temp_por_dispositivo`
* **Propósito:** Calcular a média térmica captada por cada sensor para avaliar o comportamento padrão dos ambientes monitorados. 
* **Decisão de Engenharia:** Na base original do Kaggle, a coluna `id` representa apenas um índice sequencial por linha. Para gerar real valor de negócio, utilizamos a coluna `out/in` (que identifica os sensores localizados nas áreas internas e externas) como a chave `device_id`. Isso evita a renderização de milhares de barras inúteis e entrega uma comparação direta entre a média de temperatura de "Dentro" vs "Fora".

### 2. View: `leituras_por_hora`
* **Propósito:** Entender o volume de tráfego de dados (atividade dos sensores) agrupado pelas horas do dia. O timestamp original é convertido e tem sua hora extraída para identificar em quais horários os sensores disparam mais registros de temperatura.

### 3. View: `temp_max_min_por_dia`
* **Propósito:** Isolar os extremos térmicos diários. O objetivo de negócio desta view é permitir a detecção de picos de calor ou quedas bruscas de temperatura no decorrer dos meses, facilitando auditorias climáticas de equipamentos ou galpões.

---

## 🚀 Instruções de Execução

Siga o passo a passo abaixo para reproduzir este ambiente na sua máquina local:

### 1. Clonar o Repositório
```bash
git clone URL_DO_SEU_REPOSITORIO
cd pipeline-iot

### 2. Configurar o Ambiente Python

vpython -m venv venv
# Ative o ambiente (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install pandas psycopg2-binary sqlalchemy streamlit plotly

### 3. Subir o Banco de Dados com Docker

docker run --name postgres-iot -e POSTGRES_PASSWORD=12345 -p 5432:5432 -d postgres

### 4. Processar os Dados
#Execute o script principal para ler o CSV, formatar as datas, inserir os dados no banco e criar as Views Analíticas:

python src/processamento.py

### 5. Iniciar o Dashboard Web
### Levante a interface visual interativa. O comando abaixo abrirá o dashboard automaticamente no seu navegador padrão:

streamlit run src/dashboard.py

## 📸 Capturas de Tela do Dashboard

### 1. Média de Temperatura por Dispositivo
![Média por Dispositivo](docs/Grafico1.png)

### 2. Leituras por Hora do Dia
![Leituras por Hora](docs/Grafico2.png)

### 3. Temperaturas Máximas e Mínimas Diárias
![Máximas e Mínimas](docs/Grafico3.png)
