import pandas as pd
import psycopg2
import os
import numpy as np

def importar_planilhas():
    # 🔥 Carregar os arquivos Excel
    df_pedidos = pd.read_excel("/data/data_01.xlsx", engine="openpyxl")
    df_report = pd.read_excel("/data/report_D-1.xlsx", engine="openpyxl")

    # 🔥 Renomear colunas para os nomes corretos
    df_pedidos.rename(columns={
        "Número de pedido JMS": "numero_pedido",
        "Base de entrega": "base_entrega",
        "Responsável pela entrega": "responsavel_entrega",
        "PDD de Entrega": "pdd_entrega",
        "Horário da entrega": "horario_entrega"
    }, inplace=True)

    df_report.rename(columns={
        "Remessa": "remessa",
        "Pedidos": "pedidos",
        "Regional Remetente": "regional_remetente",
        "Base de entrega": "base_entrega",
        "Data prevista de entrega": "data_prevista_entrega",
        "Entregador": "entregador",
        "Horário da entrega": "horario_entrega",
        "Entregue no prazo？": "status_entrega"
    }, inplace=True)

    # 🔥 Verificar se a coluna "status_entrega" existe
    if "status_entrega" not in df_report.columns:
        print("⚠️ Aviso: A coluna 'status_entrega' não foi encontrada no arquivo report_D-1.xlsx.")
        df_report["status_entrega"] = None  # Criar uma coluna vazia para evitar erros

    # 🔥 Converter colunas de data para datetime, tratando erros e evitando NaT
    for col in ["data_prevista_entrega", "horario_entrega", "pdd_entrega"]:
        if col in df_pedidos.columns:
            df_pedidos[col] = pd.to_datetime(df_pedidos[col], format="%Y-%m-%d", errors="coerce")
            df_pedidos[col] = df_pedidos[col].apply(lambda x: None if pd.isna(x) else x)
        if col in df_report.columns:
            df_report[col] = pd.to_datetime(df_report[col], errors="coerce")
            df_report[col] = df_report[col].apply(lambda x: None if pd.isna(x) else x)

    # 🔥 Substituir NaN por None para compatibilidade com PostgreSQL
    df_pedidos.replace({np.nan: None}, inplace=True)
    df_report.replace({np.nan: None}, inplace=True)

    # 🔥 Conectar ao PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "redvii_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "root"),
        host="REDVII-postgres_db",
        port="5432"
    )
    cursor = conn.cursor()

    # 🔥 Inserir os dados no banco de dados
    for _, row in df_pedidos.iterrows():
        cursor.execute("""
            INSERT INTO gestao_base (numero_pedido, base_entrega, responsavel_entrega, pdd_entrega, horario_entrega)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (numero_pedido) DO NOTHING;
        """, (
            row["numero_pedido"],
            row["base_entrega"],
            row["responsavel_entrega"],
            row["pdd_entrega"],
            row["horario_entrega"]
        ))

    for _, row in df_report.iterrows():
        cursor.execute("""
            INSERT INTO report_d1 (remessa, pedidos, regional_remetente, base_entrega, data_prevista_entrega, entregador, horario_entrega, status_entrega)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (remessa) DO NOTHING;
        """, (
            row["remessa"],
            row["pedidos"],
            row["regional_remetente"],
            row["base_entrega"],
            row["data_prevista_entrega"],
            row["entregador"],
            row["horario_entrega"],
            row["status_entrega"]
        ))

    # 🔥 Confirmar e fechar a conexão
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Dados importados com sucesso!")

if __name__ == "__main__":
    importar_planilhas()
