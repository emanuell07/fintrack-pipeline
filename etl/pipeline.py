from etl.extract import extract_transacoes
from etl.transform import transform
from etl.load import load_summary

def run_pipeline():
    print("🔄 Iniciando pipeline...")

    print("📥 Extraindo dados...")
    df_transacoes = extract_transacoes()
    print(f"   {len(df_transacoes)} transações extraídas.")

    print("⚙️  Transformando dados...")
    df_resumo = transform(df_transacoes)
    print(f"   {len(df_resumo)} registros de resumo gerados.")

    print("💾 Carregando no banco...")
    load_summary(df_resumo)

    print("✅ Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    run_pipeline()