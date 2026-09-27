import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco de dados
engine = create_engine('postgresql://postgres:12345@localhost:5432/postgres')

def processar_dados():
    print("1. Lendo o arquivo CSV...")
    df = pd.read_csv('data/IOT-temp.csv') 

    df = df.rename(columns={
        'out/in': 'device_id',  # Substituímos o ID único pela indicação de sensor Interno/Externo
        'temp': 'temperature', 
        'noted_date': 'timestamp'
    })

    # Converte o texto para Data/Hora no formato correto
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')

    print("2. Limpando estrutura antiga e inserindo novos dados no PostgreSQL...")
    
    # --- SOLUÇÃO: Força a exclusão da tabela antiga e de suas dependências (Views)
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS temperature_readings CASCADE;"))
        conn.commit()

    # Salva o DataFrame corrigido no banco de dados
    df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
    print("Dados inseridos com sucesso na Camada Prata!")

def criar_views():
    print("3. Criando as 3 Views Analíticas no banco de dados (Camada Ouro)...")
    
    with engine.connect() as conn:
        # VIEW 1
        conn.execute(text("""
        CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
        SELECT device_id, AVG(temperature) as avg_temp
        FROM temperature_readings
        GROUP BY device_id;
        """))

        # VIEW 2
        conn.execute(text("""
        CREATE OR REPLACE VIEW leituras_por_hora AS
        SELECT EXTRACT(HOUR FROM CAST(timestamp AS TIMESTAMP)) as hora, COUNT(*) as contagem
        FROM temperature_readings
        GROUP BY hora
        ORDER BY hora;
        """))

        # VIEW 3
        conn.execute(text("""
        CREATE OR REPLACE VIEW temp_max_min_por_dia AS
        SELECT CAST(timestamp AS DATE) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
        FROM temperature_readings
        GROUP BY data
        ORDER BY data;
        """))
        
        conn.commit()
        
    print("Views criadas com sucesso!")

if __name__ == "__main__":
    processar_dados()
    criar_views()
    print("Pipeline de processamento concluído!")