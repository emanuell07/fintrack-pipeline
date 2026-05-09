# seed.py — popula o banco fintrack com dados fictícios realistas
import sys
sys.stdout.reconfigure(encoding='utf-8')

import random
from datetime import date, timedelta
from faker import Faker
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(encoding='utf-8')
fake = Faker('pt_BR')

# Conecta ao banco diretamente
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="fintrack",
    user="postgres",
    password="laion123"
)
cur = conn.cursor()

# ── 1. Usuários ──────────────────────────────────────────────
usuarios = []
for _ in range(20):
    nome = fake.name()
    email = fake.unique.email()
    cidade = fake.city()
    cur.execute(
        "INSERT INTO usuarios (nome, email, cidade) VALUES (%s, %s, %s) RETURNING id",
        (nome, email, cidade)
    )
    usuarios.append(cur.fetchone()[0])

# ── 2. Contas ────────────────────────────────────────────────
tipos_conta = ['corrente', 'poupança', 'investimento']
contas = []
for usuario_id in usuarios:
    tipo = random.choice(tipos_conta)
    saldo = round(random.uniform(500, 15000), 2)
    cur.execute(
        "INSERT INTO contas (usuario_id, tipo, saldo_inicial) VALUES (%s, %s, %s) RETURNING id",
        (usuario_id, tipo, saldo)
    )
    contas.append(cur.fetchone()[0])

# ── 3. Categorias ────────────────────────────────────────────
categorias_data = [
    ('Salário', 'receita'),
    ('Freelance', 'receita'),
    ('Investimentos', 'receita'),
    ('Alimentação', 'despesa'),
    ('Transporte', 'despesa'),
    ('Moradia', 'despesa'),
    ('Saúde', 'despesa'),
    ('Lazer', 'despesa'),
    ('Educação', 'despesa'),
    ('Assinaturas', 'despesa'),
]
categorias = []
for nome, tipo in categorias_data:
    cur.execute(
        "INSERT INTO categorias (nome, tipo) VALUES (%s, %s) RETURNING id",
        (nome, tipo)
    )
    categorias.append((cur.fetchone()[0], tipo))

# ── 4. Transações ────────────────────────────────────────────
cat_receita = [c[0] for c in categorias if c[1] == 'receita']
cat_despesa = [c[0] for c in categorias if c[1] == 'despesa']

for conta_id in contas:
    # cada conta terá entre 30 e 60 transações nos últimos 6 meses
    for _ in range(random.randint(30, 60)):
        dias_atras = random.randint(0, 180)
        data_transacao = date.today() - timedelta(days=dias_atras)

        tipo = random.choices(['receita', 'despesa'], weights=[30, 70])[0]

        if tipo == 'receita':
            categoria_id = random.choice(cat_receita)
            valor = round(random.uniform(1000, 8000), 2)
            descricao = fake.bs().capitalize()
        else:
            categoria_id = random.choice(cat_despesa)
            valor = round(random.uniform(20, 1500), 2)
            descricao = fake.catch_phrase().capitalize()

        cur.execute(
            """INSERT INTO transacoes
               (conta_id, categoria_id, descricao, valor, tipo, data_transacao)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (conta_id, categoria_id, descricao, valor, tipo, data_transacao)
        )

conn.commit()
cur.close()
conn.close()
print("Banco populado com sucesso!")