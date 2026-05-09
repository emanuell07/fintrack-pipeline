-- FinTrack: Schema do banco de dados
-- Criado para demonstrar modelagem relacional em projeto de portfólio

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    cidade VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    tipo VARCHAR(50) NOT NULL,
    saldo_inicial NUMERIC(12,2) DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('receita', 'despesa'))
);

CREATE TABLE transacoes (
    id SERIAL PRIMARY KEY,
    conta_id INTEGER REFERENCES contas(id),
    categoria_id INTEGER REFERENCES categorias(id),
    descricao VARCHAR(200),
    valor NUMERIC(12,2) NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('receita', 'despesa')),
    data_transacao DATE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

