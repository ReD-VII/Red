-- 🔹 Estrutura do banco de dados.
-- 🔹 Tabela para "Gestão de Base" (data_01.xlsx)

CREATE TABLE IF NOT EXISTS gestao_base (
    id SERIAL PRIMARY KEY,
    numero_pedido VARCHAR(50) UNIQUE NOT NULL,
    base_entrega VARCHAR(100),
    responsavel_entrega VARCHAR(100),
    tempo_entrega TIMESTAMP,
    marca_assinatura VARCHAR(100),
    pdd_entrega VARCHAR(100),
    horario_entrega TIMESTAMP,
    tempo_criacao TIMESTAMP,
    marca_revisao VARCHAR(50),
    destino VARCHAR(100),
    uf_destino VARCHAR(2),
    destinatario VARCHAR(200),
    segmentos VARCHAR(100),
    marca_transferencia VARCHAR(100),
    pacote_problema VARCHAR(50),
    prazo_vencimento VARCHAR(50),
    codigo_entregador VARCHAR(50),
    cep_destino VARCHAR(20),
    tempo_atualizacao TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- DATA E HORA DA ATUALIZAÇÃO DOS DADOS
);

-- 🔹 Tabela para "Report D-1" (report_D-1.xlsx)
CREATE TABLE IF NOT EXISTS report_d1 (
    id SERIAL PRIMARY KEY,
    remessa VARCHAR(50) UNIQUE NOT NULL,
    pedidos INT,
    regional_remetente VARCHAR(50),
    base_entrega VARCHAR(100),
    data_prevista_entrega TIMESTAMP,
    entregador VARCHAR(100),
    horario_entrega TIMESTAMP,
    status_entrega VARCHAR(50),
    estacao_origem VARCHAR(100),
    codigo_base_remetente VARCHAR(50),
    nome_destino_hub VARCHAR(100),
    codigo_sc_destino_hub VARCHAR(50),
    cidade_destino VARCHAR(100),
    uf_destino VARCHAR(2),
    cep_destino VARCHAR(20),
    prazo_pdd_destino INT,
    origem_pedido VARCHAR(50),
    tipo_produto VARCHAR(50),
    codigo_cliente VARCHAR(50),
    nome_cliente VARCHAR(200),
    codigo_segmentos VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);